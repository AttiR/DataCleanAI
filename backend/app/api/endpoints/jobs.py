from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.processing_job import ProcessingJob
from app.models.dataset import Dataset

router = APIRouter()


@router.get("/")
async def list_jobs(db: Session = Depends(get_db)):
    """
    List all processing jobs
    """
    jobs = db.query(ProcessingJob).order_by(ProcessingJob.created_at.desc()).all()

    return {
        "jobs": [
            {
                "id": job.id,
                "dataset_id": job.dataset_id,
                "job_type": job.job_type,
                "status": job.status,
                "progress": job.progress,
                "created_at": job.created_at,
                "started_at": job.started_at,
                "completed_at": job.completed_at
            }
            for job in jobs
        ]
    }


@router.get("/{job_id}")
async def get_job(job_id: int, db: Session = Depends(get_db)):
    """
    Get job details
    """
    job = db.query(ProcessingJob).filter(ProcessingJob.id == job_id).first()

    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    # Get dataset info
    dataset = db.query(Dataset).filter(Dataset.id == job.dataset_id).first()

    return {
        "id": job.id,
        "dataset_id": job.dataset_id,
        "dataset_name": dataset.original_filename if dataset else None,
        "job_type": job.job_type,
        "status": job.status,
        "progress": job.progress,
        "configuration": job.configuration,
        "results": job.results,
        "metrics": job.metrics,
        "output_file_path": job.output_file_path,
        "error_message": job.error_message,
        "error_traceback": job.error_traceback,
        "created_at": job.created_at,
        "started_at": job.started_at,
        "completed_at": job.completed_at
    }


@router.get("/dataset/{dataset_id}")
async def get_dataset_jobs(dataset_id: int, db: Session = Depends(get_db)):
    """
    Get all jobs for a specific dataset
    """
    dataset = db.query(Dataset).filter(Dataset.id == dataset_id).first()

    if not dataset:
        raise HTTPException(status_code=404, detail="Dataset not found")

    jobs = db.query(ProcessingJob).filter(
        ProcessingJob.dataset_id == dataset_id
    ).order_by(ProcessingJob.created_at.desc()).all()

    return {
        "dataset_id": dataset_id,
        "dataset_name": dataset.original_filename,
        "jobs": [
            {
                "id": job.id,
                "job_type": job.job_type,
                "status": job.status,
                "progress": job.progress,
                "created_at": job.created_at,
                "started_at": job.started_at,
                "completed_at": job.completed_at
            }
            for job in jobs
        ]
    }


@router.delete("/{job_id}")
async def cancel_job(job_id: int, db: Session = Depends(get_db)):
    """
    Cancel a running job
    """
    job = db.query(ProcessingJob).filter(ProcessingJob.id == job_id).first()

    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    if job.status not in ["pending", "running"]:
        raise HTTPException(
            status_code=400,
            detail="Can only cancel pending or running jobs"
        )

    job.status = "cancelled"
    db.commit()

    return {"message": "Job cancelled successfully"}
