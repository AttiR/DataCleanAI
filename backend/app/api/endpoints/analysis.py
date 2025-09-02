from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks
from sqlalchemy.orm import Session
from typing import Dict, Any

from app.core.database import get_db
from app.models.dataset import Dataset
from app.models.processing_job import ProcessingJob
from app.services.analysis_service import AnalysisService
from app.ml.data_analyzer import DataQualityAnalyzer

router = APIRouter()


@router.post("/{dataset_id}/analyze")
async def analyze_dataset(
    dataset_id: int,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """
    Analyze dataset quality and generate comprehensive report
    """
    dataset = db.query(Dataset).filter(Dataset.id == dataset_id).first()

    if not dataset:
        raise HTTPException(status_code=404, detail="Dataset not found")

    # Create processing job
    job = ProcessingJob(
        dataset_id=dataset_id,
        job_type="analyze",
        status="pending"
    )

    db.add(job)
    db.commit()
    db.refresh(job)

    # Start analysis in background
    background_tasks.add_task(
        AnalysisService.run_analysis,
        dataset_id,
        job.id,
        db
    )

    return {
        "message": "Analysis started",
        "job_id": job.id,
        "status": "pending"
    }


@router.get("/{dataset_id}/analysis")
async def get_analysis_results(
    dataset_id: int,
    db: Session = Depends(get_db)
):
    """
    Get analysis results for a dataset
    """
    dataset = db.query(Dataset).filter(Dataset.id == dataset_id).first()

    if not dataset:
        raise HTTPException(status_code=404, detail="Dataset not found")

    # Get latest analysis job
    job = db.query(ProcessingJob).filter(
        ProcessingJob.dataset_id == dataset_id,
        ProcessingJob.job_type == "analyze"
    ).order_by(ProcessingJob.created_at.desc()).first()

    if not job:
        raise HTTPException(status_code=404, detail="No analysis found")

    if job.status == "pending" or job.status == "running":
        return {
            "status": job.status,
            "progress": job.progress,
            "message": "Analysis in progress"
        }

    if job.status == "failed":
        return {
            "status": "failed",
            "error": job.error_message,
            "traceback": job.error_traceback
        }

    # Return analysis results
    return {
        "status": "completed",
        "results": job.results,
        "metrics": job.metrics,
        "completed_at": job.completed_at
    }


@router.post("/{dataset_id}/analyze/sync")
async def analyze_dataset_sync(
    dataset_id: int,
    db: Session = Depends(get_db)
):
    """
    Analyze dataset synchronously (for smaller datasets)
    """
    dataset = db.query(Dataset).filter(Dataset.id == dataset_id).first()

    if not dataset:
        raise HTTPException(status_code=404, detail="Dataset not found")

    try:
        # Run analysis synchronously
        results = AnalysisService.analyze_dataset_sync(dataset.file_path)

        # Update dataset with quality metrics
        dataset.quality_score = results.get("quality_score", 0.0)
        dataset.missing_values_count = results.get("missing_data", {}).get("total_missing", 0)
        dataset.duplicate_rows_count = results.get("duplicates", {}).get("exact_duplicates", 0)
        dataset.outlier_count = results.get("outliers", {}).get("combined", {}).get("total_outliers", 0)
        dataset.status = "analyzed"

        db.commit()

        return {
            "message": "Analysis completed",
            "results": results,
            "quality_score": dataset.quality_score
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{dataset_id}/analysis/visualizations")
async def get_analysis_visualizations(
    dataset_id: int,
    db: Session = Depends(get_db)
):
    """
    Get visualization data for analysis results
    """
    dataset = db.query(Dataset).filter(Dataset.id == dataset_id).first()

    if not dataset:
        raise HTTPException(status_code=404, detail="Dataset not found")

    # Get latest analysis job
    job = db.query(ProcessingJob).filter(
        ProcessingJob.dataset_id == dataset_id,
        ProcessingJob.job_type == "analyze",
        ProcessingJob.status == "completed"
    ).order_by(ProcessingJob.created_at.desc()).first()

    if not job:
        raise HTTPException(status_code=404, detail="No completed analysis found")

    try:
        # Generate visualizations
        analyzer = DataQualityAnalyzer()
        visualizations = analyzer.generate_visualizations()

        return {
            "visualizations": visualizations,
            "analysis_results": job.results
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{dataset_id}/analysis/recommendations")
async def get_analysis_recommendations(
    dataset_id: int,
    db: Session = Depends(get_db)
):
    """
    Get data quality improvement recommendations
    """
    dataset = db.query(Dataset).filter(Dataset.id == dataset_id).first()

    if not dataset:
        raise HTTPException(status_code=404, detail="Dataset not found")

    # Get latest analysis job
    job = db.query(ProcessingJob).filter(
        ProcessingJob.dataset_id == dataset_id,
        ProcessingJob.job_type == "analyze",
        ProcessingJob.status == "completed"
    ).order_by(ProcessingJob.created_at.desc()).first()

    if not job:
        raise HTTPException(status_code=404, detail="No completed analysis found")

    results = job.results

    # Generate recommendations
    recommendations = []

    # Missing data recommendations
    missing_data = results.get("missing_data", {})
    missing_pct = missing_data.get("missing_percentage", 0)

    if missing_pct > 5:
        recommendations.append({
            "type": "missing_data",
            "severity": "high" if missing_pct > 20 else "medium",
            "message": f"High missing data ({missing_pct:.1f}%). Consider imputation strategies.",
            "suggestions": [
                "Use mean/median imputation for numeric columns",
                "Use mode imputation for categorical columns",
                "Consider KNN imputation for complex patterns"
            ]
        })

    # Duplicate recommendations
    duplicates = results.get("duplicates", {})
    duplicate_pct = duplicates.get("exact_duplicate_pct", 0)

    if duplicate_pct > 1:
        recommendations.append({
            "type": "duplicates",
            "severity": "high" if duplicate_pct > 10 else "medium",
            "message": f"Duplicate data detected ({duplicate_pct:.1f}%).",
            "suggestions": [
                "Remove exact duplicate rows",
                "Review near-duplicate rows",
                "Implement data validation rules"
            ]
        })

    # Outlier recommendations
    outliers = results.get("outliers", {})
    if "combined" in outliers:
        total_outliers = outliers["combined"].get("total_outliers", 0)
        if total_outliers > 0:
            recommendations.append({
                "type": "outliers",
                "severity": "medium",
                "message": f"Outliers detected ({total_outliers} points).",
                "suggestions": [
                    "Review outliers for data entry errors",
                    "Consider capping outliers using IQR method",
                    "Use robust statistical methods"
                ]
            })

    # Data type recommendations
    data_types = results.get("data_types", {})
    for col, analysis in data_types.items():
        if analysis.get("mixed_types"):
            recommendations.append({
                "type": "data_types",
                "severity": "medium",
                "message": f"Column '{col}' has mixed data types.",
                "suggestions": [
                    "Standardize data format",
                    "Convert to appropriate data type",
                    "Handle mixed numeric/string values"
                ]
            })

    return {
        "recommendations": recommendations,
        "total_recommendations": len(recommendations),
        "quality_score": results.get("quality_score", 0.0)
    }
