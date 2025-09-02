from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks
from sqlalchemy.orm import Session
from typing import Dict, Any

from app.core.database import get_db
from app.models.dataset import Dataset
from app.models.processing_job import ProcessingJob
from app.services.cleaning_service import CleaningService

router = APIRouter()


@router.post("/{dataset_id}/clean")
async def clean_dataset(
    dataset_id: int,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """
    Clean dataset using AI-powered cleaning pipeline
    """
    dataset = db.query(Dataset).filter(Dataset.id == dataset_id).first()

    if not dataset:
        raise HTTPException(status_code=404, detail="Dataset not found")

    # Create processing job
    job = ProcessingJob(
        dataset_id=dataset_id,
        job_type="clean",
        status="pending"
    )

    db.add(job)
    db.commit()
    db.refresh(job)

    # Start cleaning in background
    background_tasks.add_task(
        CleaningService.run_cleaning,
        dataset_id,
        job.id,
        db
    )

    return {
        "message": "Data cleaning started",
        "job_id": job.id,
        "status": "pending"
    }


@router.get("/{dataset_id}/cleaning")
async def get_cleaning_results(
    dataset_id: int,
    db: Session = Depends(get_db)
):
    """
    Get cleaning results for a dataset
    """
    dataset = db.query(Dataset).filter(Dataset.id == dataset_id).first()

    if not dataset:
        raise HTTPException(status_code=404, detail="Dataset not found")

    # Get latest cleaning job
    job = db.query(ProcessingJob).filter(
        ProcessingJob.dataset_id == dataset_id,
        ProcessingJob.job_type == "clean"
    ).order_by(ProcessingJob.created_at.desc()).first()

    if not job:
        raise HTTPException(status_code=404, detail="No cleaning job found")

    if job.status == "pending" or job.status == "running":
        return {
            "status": job.status,
            "progress": job.progress,
            "message": "Cleaning in progress"
        }

    if job.status == "failed":
        return {
            "status": "failed",
            "error": job.error_message,
            "traceback": job.error_traceback
        }

    # Return cleaning results
    return {
        "status": "completed",
        "results": job.results,
        "output_file": job.output_file_path,
        "completed_at": job.completed_at
    }


@router.post("/{dataset_id}/clean/sync")
async def clean_dataset_sync(
    dataset_id: int,
    db: Session = Depends(get_db)
):
    """
    Clean dataset synchronously (for smaller datasets)
    """
    dataset = db.query(Dataset).filter(Dataset.id == dataset_id).first()

    if not dataset:
        raise HTTPException(status_code=404, detail="Dataset not found")

    try:
        # Run cleaning synchronously
        results = CleaningService.clean_dataset_sync(dataset.file_path)

        return {
            "message": "Data cleaning completed",
            "results": results,
            "cleaned_data_preview": results.get("cleaned_data_preview", [])
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{dataset_id}/cleaning/summary")
async def get_cleaning_summary(
    dataset_id: int,
    db: Session = Depends(get_db)
):
    """
    Get summary of cleaning operations
    """
    dataset = db.query(Dataset).filter(Dataset.id == dataset_id).first()

    if not dataset:
        raise HTTPException(status_code=404, detail="Dataset not found")

    # Get latest cleaning job
    job = db.query(ProcessingJob).filter(
        ProcessingJob.dataset_id == dataset_id,
        ProcessingJob.job_type == "clean",
        ProcessingJob.status == "completed"
    ).order_by(ProcessingJob.created_at.desc()).first()

    if not job:
        raise HTTPException(status_code=404, detail="No completed cleaning job found")

    results = job.results

    # Generate summary
    summary = {
        "original_shape": results.get("original_shape", (0, 0)),
        "final_shape": results.get("final_shape", (0, 0)),
        "rows_removed": results.get("rows_removed", 0),
        "cleaning_steps": results.get("cleaning_steps", []),
        "imputation_summary": results.get("imputation_summary", {}),
        "outlier_treatment": results.get("outlier_treatment", {}),
        "transformation_summary": results.get("transformation_summary", {})
    }

    return summary
