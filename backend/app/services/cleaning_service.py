import pandas as pd
import numpy as np
import os
from sqlalchemy.orm import Session
from datetime import datetime

from app.models.dataset import Dataset
from app.models.processing_job import ProcessingJob
from app.services.dataset_service import DatasetService
from app.ml.data_cleaner import AutoDataCleaner
from app.ml.data_analyzer import DataQualityAnalyzer


class CleaningService:
    """Service for running data cleaning operations."""

    @staticmethod
    def _make_json_serializable(obj):
        """Convert numpy types to Python native types for JSON serialization."""
        if isinstance(obj, dict):
            return {key: CleaningService._make_json_serializable(value) for key, value in obj.items()}
        elif isinstance(obj, list):
            return [CleaningService._make_json_serializable(item) for item in obj]
        elif isinstance(obj, tuple):
            return tuple(CleaningService._make_json_serializable(item) for item in obj)
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
    def run_cleaning(dataset_id: int, job_id: int, db: Session):
        """Run cleaning in background."""
        try:
            # Update job status
            job = db.query(ProcessingJob).filter(ProcessingJob.id == job_id).first()
            job.status = "running"
            job.started_at = datetime.now()
            db.commit()

            # Get dataset
            dataset = db.query(Dataset).filter(Dataset.id == dataset_id).first()

            # Check if dataset has been analyzed first
            if dataset.status not in ["analyzed", "cleaned"]:
                raise ValueError("Dataset must be analyzed before cleaning. Please run analysis first.")

            # Read dataset
            df = DatasetService.read_file(dataset.file_path)

            # Run analysis first to get context
            analyzer = DataQualityAnalyzer()
            analysis_results = analyzer.analyze_dataset(df)

            # Run cleaning
            cleaner = AutoDataCleaner()
            cleaned_df = cleaner.clean_dataset(df, analysis_results)

            # Save cleaned dataset
            from app.core.config import settings
            output_filename = f"cleaned_{dataset.filename}"
            output_path = os.path.join(settings.UPLOAD_DIR, output_filename)

            # Ensure directory exists
            os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
            DatasetService.save_file(cleaned_df, output_path)

            # Get cleaning summary
            cleaning_summary = cleaner.get_cleaning_summary()
            cleaning_summary["cleaned_data_preview"] = cleaned_df.head(10).to_dict('records')

            # Convert results to JSON-serializable format
            serializable_summary = CleaningService._make_json_serializable(cleaning_summary)

            # Update job with results
            job.status = "completed"
            job.completed_at = datetime.now()
            job.results = serializable_summary
            job.output_file_path = output_path
            job.progress = 100

            # Update dataset status
            dataset.status = "cleaned"

            db.commit()

        except Exception as e:
            import traceback
            error_trace = traceback.format_exc()
            print(f"Cleaning error: {e}")
            print(f"Traceback: {error_trace}")

            # Rollback transaction on error
            db.rollback()
            try:
                # Update job with error
                job = db.query(ProcessingJob).filter(ProcessingJob.id == job_id).first()
                if job:
                    job.status = "failed"
                    job.error_message = str(e)
                    job.error_traceback = error_trace
                    db.commit()
            except Exception as ex:
                print(f"Failed to update job error: {ex}")
                db.rollback()

    @staticmethod
    def clean_dataset_sync(file_path: str):
        """Run cleaning synchronously."""
        # Read dataset
        df = DatasetService.read_file(file_path)

        # Run analysis first
        analyzer = DataQualityAnalyzer()
        analysis_results = analyzer.analyze_dataset(df)

        # Run cleaning
        cleaner = AutoDataCleaner()
        cleaned_df = cleaner.clean_dataset(df, analysis_results)

        # Get cleaning summary
        cleaning_summary = cleaner.get_cleaning_summary()
        cleaning_summary["cleaned_data_preview"] = cleaned_df.head(10).to_dict('records')

        return cleaning_summary
