import pandas as pd
import numpy as np
import json
from sqlalchemy.orm import Session
from datetime import datetime

from app.models.dataset import Dataset
from app.models.processing_job import ProcessingJob
from app.services.dataset_service import DatasetService
from app.ml.data_analyzer import DataQualityAnalyzer


class AnalysisService:
    """Service for running data quality analysis."""

    @staticmethod
    def _make_json_serializable(obj):
        """Convert numpy types to Python native types for JSON serialization."""
        if isinstance(obj, dict):
            return {key: AnalysisService._make_json_serializable(value) for key, value in obj.items()}
        elif isinstance(obj, list):
            return [AnalysisService._make_json_serializable(item) for item in obj]
        elif isinstance(obj, tuple):
            return tuple(AnalysisService._make_json_serializable(item) for item in obj)
        elif isinstance(obj, (np.integer, np.int64, np.int32)):
            return int(obj)
        elif isinstance(obj, (np.floating, np.float64, np.float32)):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        elif isinstance(obj, (np.dtype, pd.core.dtypes.base.ExtensionDtype)):
            return str(obj)
        elif pd.isna(obj):
            return None
        elif hasattr(obj, 'dtype'):  # Catch any pandas/numpy objects with dtype
            if hasattr(obj, 'item'):  # Single values
                return obj.item()
            else:
                return str(obj)
        else:
            return obj

    @staticmethod
    def run_analysis(dataset_id: int, job_id: int, db: Session):
        """Run analysis in background."""
        try:
            # Update job status
            job = db.query(ProcessingJob).filter(ProcessingJob.id == job_id).first()
            job.status = "running"
            job.started_at = datetime.now()
            db.commit()

            # Get dataset
            dataset = db.query(Dataset).filter(Dataset.id == dataset_id).first()

            # Read dataset
            df = DatasetService.read_file(dataset.file_path)

            # Run analysis
            analyzer = DataQualityAnalyzer()
            results = analyzer.analyze_dataset(df)

            # Convert results to JSON-serializable format
            serializable_results = AnalysisService._make_json_serializable(results)

            # Update job with results
            job.status = "completed"
            job.completed_at = datetime.now()
            job.results = serializable_results
            job.progress = 100

            # Update dataset metrics
            dataset.quality_score = results.get("quality_score", 0.0)
            dataset.missing_values_count = results.get("missing_data", {}).get("total_missing", 0)
            dataset.duplicate_rows_count = results.get("duplicates", {}).get("exact_duplicates", 0)
            dataset.outlier_count = results.get("outliers", {}).get("combined", {}).get("total_outliers", 0)
            dataset.status = "analyzed"

            db.commit()

        except Exception as e:
            # Rollback transaction on error
            db.rollback()
            try:
                # Update job with error
                job = db.query(ProcessingJob).filter(ProcessingJob.id == job_id).first()
                if job:
                    job.status = "failed"
                    job.error_message = str(e)
                    job.error_traceback = str(e)
                    db.commit()
            except Exception:
                db.rollback()

    @staticmethod
    def analyze_dataset_sync(file_path: str):
        """Run analysis synchronously."""
        # Read dataset
        df = DatasetService.read_file(file_path)

        # Run analysis
        analyzer = DataQualityAnalyzer()
        results = analyzer.analyze_dataset(df)

        return results
