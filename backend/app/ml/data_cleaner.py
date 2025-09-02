import pandas as pd
import numpy as np
from typing import Dict, List, Any, Optional
from sklearn.impute import SimpleImputer, KNNImputer
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import cross_val_score
import warnings
warnings.filterwarnings('ignore')


class AutoDataCleaner:
    """
    Advanced data cleaning pipeline with intelligent imputation and transformation.
    """

    def __init__(self, config: Optional[Dict] = None):
        self.config = config or {}
        self.cleaning_results = {}
        self.imputers = {}
        self.encoders = {}
        self.scalers = {}

    def clean_dataset(self, df: pd.DataFrame,
                     analysis_results: Optional[Dict] = None) -> pd.DataFrame:
        """
        Comprehensive data cleaning pipeline.
        """
        self.cleaning_results = {
            "original_shape": df.shape,
            "cleaning_steps": [],
            "imputation_summary": {},
            "outlier_treatment": {},
            "transformation_summary": {}
        }

        # Create a copy to avoid modifying original
        cleaned_df = df.copy()

        # Step 1: Handle missing data
        cleaned_df = self._handle_missing_data(cleaned_df, analysis_results)

        # Step 2: Handle outliers
        cleaned_df = self._handle_outliers(cleaned_df, analysis_results)

        # Step 3: Remove duplicates
        cleaned_df = self._remove_duplicates(cleaned_df)

        # Step 4: Standardize data types
        cleaned_df = self._standardize_data_types(cleaned_df)

        # Step 5: Handle inconsistencies
        cleaned_df = self._handle_inconsistencies(cleaned_df)

        # Step 6: Feature scaling and encoding
        cleaned_df = self._apply_transformations(cleaned_df)

        self.cleaning_results["final_shape"] = cleaned_df.shape
        self.cleaning_results["rows_removed"] = (
            self.cleaning_results["original_shape"][0] -
            self.cleaning_results["final_shape"][0]
        )

        return cleaned_df

    def _handle_missing_data(self, df: pd.DataFrame,
                           analysis_results: Optional[Dict]) -> pd.DataFrame:
        """Intelligent missing data handling."""
        if analysis_results and "missing_data" in analysis_results:
            missing_data = analysis_results["missing_data"]
        else:
            # Analyze missing data if not provided
            missing_data = self._analyze_missing_data(df)

        self.cleaning_results["imputation_summary"] = {
            "columns_imputed": [],
            "methods_used": {},
            "imputation_stats": {}
        }

        for col in df.columns:
            missing_count = df[col].isnull().sum()
            if missing_count > 0:
                imputation_method = self._select_imputation_method(
                    df, col, missing_count, missing_data
                )

                df[col] = self._apply_imputation(df, col, imputation_method)

                self.cleaning_results["imputation_summary"]["columns_imputed"].append(col)
                self.cleaning_results["imputation_summary"]["methods_used"][col] = imputation_method

                self.cleaning_results["cleaning_steps"].append(
                    f"Imputed {missing_count} missing values in '{col}' using {imputation_method}"
                )

        return df

    def _analyze_missing_data(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Analyze missing data patterns."""
        missing_data = {}

        # Overall missing data
        total_missing = df.isnull().sum().sum()
        total_cells = df.size
        missing_percentage = (total_missing / total_cells) * 100

        # Per column missing data
        column_missing = df.isnull().sum()
        column_missing_pct = (column_missing / len(df)) * 100

        missing_data = {
            "total_missing": total_missing,
            "total_cells": total_cells,
            "missing_percentage": missing_percentage,
            "column_missing": column_missing.to_dict(),
            "column_missing_pct": column_missing_pct.to_dict()
        }

        return missing_data

    def _select_imputation_method(self, df: pd.DataFrame, col: str,
                                missing_count: int, missing_data: Dict) -> str:
        """Intelligently select the best imputation method."""
        missing_pct = missing_data["column_missing_pct"][col]

        # If too much missing data (>50%), use simple methods
        if missing_pct > 50:
            return "drop_column"

        # Check data type
        dtype = df[col].dtype

        if pd.api.types.is_numeric_dtype(dtype):
            # For numeric columns
            if missing_pct < 5:
                return "mean"
            elif missing_pct < 20:
                return "median"
            else:
                return "knn"
        else:
            # For categorical/text columns
            if missing_pct < 10:
                return "mode"
            else:
                return "constant"

    def _apply_imputation(self, df: pd.DataFrame, col: str, method: str) -> pd.Series:
        """Apply the selected imputation method."""
        if method == "drop_column":
            df.drop(columns=[col], inplace=True)
            return df[col] if col in df.columns else pd.Series()

        elif method == "mean":
            imputer = SimpleImputer(strategy='mean')
            imputed_values = imputer.fit_transform(df[[col]]).flatten()
            self.imputers[col] = imputer
            return imputed_values

        elif method == "median":
            imputer = SimpleImputer(strategy='median')
            imputed_values = imputer.fit_transform(df[[col]]).flatten()
            self.imputers[col] = imputer
            return imputed_values

        elif method == "mode":
            imputer = SimpleImputer(strategy='most_frequent')
            imputed_values = imputer.fit_transform(df[[col]]).flatten()
            self.imputers[col] = imputer
            return imputed_values

        elif method == "knn":
            # Use KNN imputation for numeric columns
            numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
            if col in numeric_cols and len(numeric_cols) > 1:
                # Remove the target column from features
                feature_cols = [c for c in numeric_cols if c != col]
                if feature_cols:
                    imputer = KNNImputer(n_neighbors=min(5, len(df)))
                    temp_df = df[feature_cols + [col]].copy()
                    temp_df = pd.DataFrame(
                        imputer.fit_transform(temp_df),
                        columns=temp_df.columns,
                        index=temp_df.index
                    )
                    df[col] = temp_df[col]
                    self.imputers[col] = imputer
                    return df[col]

            # Fallback to median if KNN fails
            imputer = SimpleImputer(strategy='median')
            imputed_values = imputer.fit_transform(df[[col]]).flatten()
            self.imputers[col] = imputer
            return imputed_values

        elif method == "constant":
            # Use a placeholder value
            placeholder = "Unknown" if df[col].dtype == 'object' else -999
            df[col] = df[col].fillna(placeholder)
            return df[col]

        else:
            # Default to forward fill
            df[col] = df[col].fillna(method='ffill').fillna(method='bfill')
            return df[col]

    def _handle_outliers(self, df: pd.DataFrame,
                        analysis_results: Optional[Dict]) -> pd.DataFrame:
        """Handle outliers based on analysis results."""
        if not analysis_results or "outliers" not in analysis_results:
            return df

        outliers = analysis_results["outliers"]
        self.cleaning_results["outlier_treatment"] = {
            "columns_processed": [],
            "outliers_removed": 0,
            "outliers_capped": 0,
            "methods_used": {}
        }

        if "combined" in outliers:
            outlier_info = outliers["combined"]
            outlier_indices = outlier_info.get("all_outlier_indices", [])

            if outlier_indices:
                # Remove outlier rows
                df = df.drop(index=outlier_indices)
                self.cleaning_results["outlier_treatment"]["outliers_removed"] = len(outlier_indices)
                self.cleaning_results["cleaning_steps"].append(
                    f"Removed {len(outlier_indices)} outlier rows"
                )

        # Handle outliers by column using IQR method
        numeric_cols = df.select_dtypes(include=[np.number]).columns

        for col in numeric_cols:
            col_data = df[col].dropna()
            if len(col_data) == 0:
                continue

            Q1 = col_data.quantile(0.25)
            Q3 = col_data.quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR

            # Cap outliers instead of removing
            outliers_mask = (df[col] < lower_bound) | (df[col] > upper_bound)
            outliers_count = outliers_mask.sum()

            if outliers_count > 0:
                df.loc[outliers_mask, col] = df.loc[outliers_mask, col].clip(
                    lower=lower_bound, upper=upper_bound
                )

                self.cleaning_results["outlier_treatment"]["columns_processed"].append(col)
                self.cleaning_results["outlier_treatment"]["outliers_capped"] += outliers_count
                self.cleaning_results["outlier_treatment"]["methods_used"][col] = "iqr_capping"

                self.cleaning_results["cleaning_steps"].append(
                    f"Capped {outliers_count} outliers in '{col}' using IQR method"
                )

        return df

    def _remove_duplicates(self, df: pd.DataFrame) -> pd.DataFrame:
        """Remove duplicate rows."""
        original_count = len(df)
        df = df.drop_duplicates()
        removed_count = original_count - len(df)

        if removed_count > 0:
            self.cleaning_results["cleaning_steps"].append(
                f"Removed {removed_count} duplicate rows"
            )

        return df

    def _standardize_data_types(self, df: pd.DataFrame) -> pd.DataFrame:
        """Standardize data types across columns."""
        self.cleaning_results["transformation_summary"]["type_conversions"] = {}

        for col in df.columns:
            original_dtype = str(df[col].dtype)

            # Try to convert to appropriate type
            new_dtype = self._suggest_optimal_dtype(df[col])

            if new_dtype != original_dtype:
                try:
                    if new_dtype == "datetime":
                        df[col] = pd.to_datetime(df[col], errors='coerce')
                    elif new_dtype == "numeric":
                        df[col] = pd.to_numeric(df[col], errors='coerce')
                    elif new_dtype == "categorical":
                        df[col] = df[col].astype('category')

                    self.cleaning_results["transformation_summary"]["type_conversions"][col] = {
                        "from": original_dtype,
                        "to": new_dtype
                    }

                    self.cleaning_results["cleaning_steps"].append(
                        f"Converted '{col}' from {original_dtype} to {new_dtype}"
                    )
                except Exception as e:
                    # Keep original type if conversion fails
                    pass

        return df

    def _suggest_optimal_dtype(self, series: pd.Series) -> str:
        """Suggest optimal data type for a column."""
        # Check if it's already datetime
        if pd.api.types.is_datetime64_any_dtype(series):
            return "datetime"

        # Try to convert to numeric
        numeric_series = pd.to_numeric(series, errors='coerce')
        if numeric_series.notna().sum() / len(series) > 0.8:
            return "numeric"

        # Try to convert to datetime
        try:
            pd.to_datetime(series)
            return "datetime"
        except:
            pass

        # Check if it's categorical
        unique_ratio = series.nunique() / len(series)
        if unique_ratio < 0.5:
            return "categorical"

        return "object"

    def _handle_inconsistencies(self, df: pd.DataFrame) -> pd.DataFrame:
        """Handle data inconsistencies."""
        self.cleaning_results["transformation_summary"]["inconsistencies_fixed"] = {}

        for col in df.columns:
            if df[col].dtype == 'object':
                # Handle string inconsistencies
                df[col] = self._standardize_strings(df[col])

                # Handle case inconsistencies
                df[col] = self._standardize_case(df[col])

        return df

    def _standardize_strings(self, series: pd.Series) -> pd.Series:
        """Standardize string values."""
        # Remove extra whitespace
        series = series.str.strip()

        # Replace multiple spaces with single space
        series = series.str.replace(r'\s+', ' ', regex=True)

        # Handle common abbreviations
        abbreviations = {
            'usa': 'United States',
            'uk': 'United Kingdom',
            'u.s.a.': 'United States',
            'u.k.': 'United Kingdom'
        }

        for abbr, full in abbreviations.items():
            series = series.str.replace(abbr, full, case=False, regex=False)

        return series

    def _standardize_case(self, series: pd.Series) -> pd.Series:
        """Standardize case in string columns."""
        # Use title case for names, sentence case for descriptions
        if series.name and any(word in series.name.lower() for word in ['name', 'title', 'category']):
            return series.str.title()
        else:
            return series.str.capitalize()

    def _apply_transformations(self, df: pd.DataFrame) -> pd.DataFrame:
        """Apply feature scaling and encoding."""
        self.cleaning_results["transformation_summary"]["scaling"] = {}
        self.cleaning_results["transformation_summary"]["encoding"] = {}

        # Scale numeric features
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        if len(numeric_cols) > 0:
            scaler = StandardScaler()
            df[numeric_cols] = scaler.fit_transform(df[numeric_cols])
            self.scalers['numeric'] = scaler

            self.cleaning_results["transformation_summary"]["scaling"]["numeric_columns"] = list(numeric_cols)
            self.cleaning_results["cleaning_steps"].append(
                f"Scaled {len(numeric_cols)} numeric columns"
            )

        # Encode categorical features
        categorical_cols = df.select_dtypes(include=['category', 'object']).columns
        for col in categorical_cols:
            if df[col].nunique() < 50:  # Only encode if not too many unique values
                encoder = LabelEncoder()
                df[col] = encoder.fit_transform(df[col].astype(str))
                self.encoders[col] = encoder

                self.cleaning_results["transformation_summary"]["encoding"][col] = "label_encoding"
                self.cleaning_results["cleaning_steps"].append(
                    f"Label encoded '{col}'"
                )

        return df

    def get_cleaning_summary(self) -> Dict[str, Any]:
        """Get summary of cleaning operations."""
        return self.cleaning_results

    def save_cleaning_pipeline(self, filepath: str):
        """Save the cleaning pipeline for future use."""
        import joblib

        pipeline_data = {
            "imputers": self.imputers,
            "encoders": self.encoders,
            "scalers": self.scalers,
            "config": self.config
        }

        joblib.dump(pipeline_data, filepath)

    def load_cleaning_pipeline(self, filepath: str):
        """Load a saved cleaning pipeline."""
        import joblib

        pipeline_data = joblib.load(filepath)
        self.imputers = pipeline_data["imputers"]
        self.encoders = pipeline_data["encoders"]
        self.scalers = pipeline_data["scalers"]
        self.config = pipeline_data["config"]
