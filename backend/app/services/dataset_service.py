import pandas as pd
import os
from typing import Dict, Any


class DatasetService:
    """Service for handling dataset operations."""

    @staticmethod
    def read_file(file_path: str) -> pd.DataFrame:
        """Read dataset file based on extension."""
        file_extension = os.path.splitext(file_path)[1].lower()

        if file_extension == '.csv':
            return pd.read_csv(file_path)
        elif file_extension in ['.xlsx', '.xls']:
            return pd.read_excel(file_path)
        elif file_extension == '.parquet':
            return pd.read_parquet(file_path)
        else:
            raise ValueError(f"Unsupported file type: {file_extension}")

    @staticmethod
    def save_file(df: pd.DataFrame, file_path: str, file_type: str = None):
        """Save dataset to file."""
        if file_type is None:
            file_type = os.path.splitext(file_path)[1].lower()

        if file_type == '.csv':
            df.to_csv(file_path, index=False)
        elif file_type in ['.xlsx', '.xls']:
            df.to_excel(file_path, index=False)
        elif file_type == '.parquet':
            df.to_parquet(file_path, index=False)
        else:
            raise ValueError(f"Unsupported file type: {file_type}")

    @staticmethod
    def get_file_info(file_path: str) -> Dict[str, Any]:
        """Get basic file information."""
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")

        file_size = os.path.getsize(file_path)
        file_extension = os.path.splitext(file_path)[1].lower()

        # Read file to get basic info
        df = DatasetService.read_file(file_path)

        return {
            "file_path": file_path,
            "file_size": file_size,
            "file_extension": file_extension,
            "row_count": len(df),
            "column_count": len(df.columns),
            "columns": list(df.columns),
            "dtypes": df.dtypes.to_dict()
        }
