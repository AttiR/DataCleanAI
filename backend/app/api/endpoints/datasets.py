from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
import pandas as pd
import os
from datetime import datetime

from app.core.database import get_db
from app.models.dataset import Dataset
from app.models.processing_job import ProcessingJob
from app.services.dataset_service import DatasetService
from app.core.config import settings

router = APIRouter()


@router.post("/upload")
async def upload_dataset(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """
    Upload a dataset file (CSV, Excel, etc.)
    """
    # Validate file type
    allowed_extensions = ['.csv', '.xlsx', '.xls', '.parquet']
    file_extension = os.path.splitext(file.filename)[1].lower()

    if file_extension not in allowed_extensions:
        raise HTTPException(
            status_code=400,
            detail=f"File type not supported. Allowed: {allowed_extensions}"
        )

    # Validate file size
    if file.size > settings.MAX_FILE_SIZE:
        raise HTTPException(
            status_code=400,
            detail=f"File too large. Max size: {settings.MAX_FILE_SIZE / (1024*1024)}MB"
        )

    try:
        # Save file
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{timestamp}_{file.filename}"
        file_path = os.path.join(settings.UPLOAD_DIR, filename)

        with open(file_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)

        # Read and analyze file
        df = DatasetService.read_file(file_path)

        # Create dataset record
        dataset = Dataset(
            filename=filename,
            original_filename=file.filename,
            file_path=file_path,
            file_size=file.size,
            file_type=file_extension,
            row_count=len(df),
            column_count=len(df.columns),
            column_info={col: str(dtype) for col, dtype in df.dtypes.to_dict().items()},
            status="uploaded"
        )

        db.add(dataset)
        db.commit()
        db.refresh(dataset)

        return {
            "message": "Dataset uploaded successfully",
            "dataset_id": dataset.id,
            "filename": dataset.filename,
            "shape": (dataset.row_count, dataset.column_count),
            "columns": list(df.columns)
        }

    except Exception as e:
        # Clean up file if error occurs
        if os.path.exists(file_path):
            os.remove(file_path)
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/")
async def list_datasets(db: Session = Depends(get_db)):
    """
    List all uploaded datasets
    """
    datasets = db.query(Dataset).order_by(Dataset.created_at.desc()).all()

    return {
        "datasets": [
            {
                "id": dataset.id,
                "filename": dataset.original_filename,
                "file_type": dataset.file_type,
                "shape": (dataset.row_count, dataset.column_count),
                "quality_score": dataset.quality_score,
                "status": dataset.status,
                "created_at": dataset.created_at,
                "updated_at": dataset.updated_at
            }
            for dataset in datasets
        ]
    }


@router.get("/{dataset_id}")
async def get_dataset(dataset_id: int, db: Session = Depends(get_db)):
    """
    Get dataset details and preview
    """
    dataset = db.query(Dataset).filter(Dataset.id == dataset_id).first()

    if not dataset:
        raise HTTPException(status_code=404, detail="Dataset not found")

    try:
        # Read file and get preview
        df = DatasetService.read_file(dataset.file_path)
        preview = df.head(10).to_dict('records')

        return {
            "id": dataset.id,
            "filename": dataset.original_filename,
            "file_type": dataset.file_type,
            "shape": (dataset.row_count, dataset.column_count),
            "columns": list(df.columns),
            "dtypes": df.dtypes.to_dict(),
            "quality_score": dataset.quality_score,
            "status": dataset.status,
            "preview": preview,
            "created_at": dataset.created_at,
            "updated_at": dataset.updated_at
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{dataset_id}")
async def delete_dataset(dataset_id: int, db: Session = Depends(get_db)):
    """
    Delete a dataset
    """
    dataset = db.query(Dataset).filter(Dataset.id == dataset_id).first()

    if not dataset:
        raise HTTPException(status_code=404, detail="Dataset not found")

    try:
        # Delete associated processing jobs first
        jobs = db.query(ProcessingJob).filter(ProcessingJob.dataset_id == dataset_id).all()
        for job in jobs:
            # Delete cleaned files if they exist
            if job.output_file_path and os.path.exists(job.output_file_path):
                os.remove(job.output_file_path)
            db.delete(job)

        # Delete dataset file
        if os.path.exists(dataset.file_path):
            os.remove(dataset.file_path)

        # Delete dataset from database
        db.delete(dataset)
        db.commit()

        return {"message": "Dataset and associated jobs deleted successfully"}

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{dataset_id}/download")
async def download_dataset(dataset_id: int, db: Session = Depends(get_db)):
    """
    Download the cleaned dataset file
    """
    from fastapi.responses import FileResponse

    dataset = db.query(Dataset).filter(Dataset.id == dataset_id).first()
    if not dataset:
        raise HTTPException(status_code=404, detail="Dataset not found")

    # Get the latest cleaning job to find the cleaned file
    job = db.query(ProcessingJob).filter(
        ProcessingJob.dataset_id == dataset_id,
        ProcessingJob.job_type == "clean",
        ProcessingJob.status == "completed"
    ).order_by(ProcessingJob.created_at.desc()).first()

    if job and job.output_file_path and os.path.exists(job.output_file_path):
        # Return cleaned file
        filename = f"cleaned_{dataset.original_filename}"
        return FileResponse(
            path=job.output_file_path,
            filename=filename,
            media_type='application/octet-stream'
        )
    elif os.path.exists(dataset.file_path):
        # Return original file if no cleaned version exists
        return FileResponse(
            path=dataset.file_path,
            filename=dataset.original_filename,
            media_type='application/octet-stream'
        )
    else:
        raise HTTPException(status_code=404, detail="File not found")


@router.delete("/")
async def delete_all_datasets(db: Session = Depends(get_db)):
    """
    Delete all datasets and their associated jobs
    """
    try:
        # Get all datasets
        datasets = db.query(Dataset).all()

        # Delete all processing jobs first
        all_jobs = db.query(ProcessingJob).all()
        for job in all_jobs:
            # Delete cleaned files if they exist
            if job.output_file_path and os.path.exists(job.output_file_path):
                os.remove(job.output_file_path)
            db.delete(job)

        # Delete all dataset files and records
        for dataset in datasets:
            # Delete dataset file
            if os.path.exists(dataset.file_path):
                os.remove(dataset.file_path)
            db.delete(dataset)

        db.commit()

        return {"message": f"Successfully deleted {len(datasets)} datasets and {len(all_jobs)} jobs"}

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
