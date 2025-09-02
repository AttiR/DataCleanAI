import pandas as pd
import numpy as np
from typing import Dict, List, Any, Optional, Tuple
import missingno as msno
from scipy import stats
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import IsolationForest
from sklearn.neighbors import LocalOutlierFactor
from sklearn.svm import OneClassSVM
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')


class DataQualityAnalyzer:
    """
    Advanced data quality analyzer with comprehensive assessment capabilities.
    """

    def __init__(self, config: Optional[Dict] = None):
        self.config = config or {}
        self.analysis_results = {}

    def analyze_dataset(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Comprehensive dataset analysis covering all quality aspects.
        """
        self.analysis_results = {
            "basic_info": self._analyze_basic_info(df),
            "missing_data": self._analyze_missing_data(df),
            "duplicates": self._analyze_duplicates(df),
            "outliers": self._analyze_outliers(df),
            "data_types": self._analyze_data_types(df),
            "distributions": self._analyze_distributions(df),
            "correlations": self._analyze_correlations(df),
            "quality_score": 0.0,
            "recommendations": []
        }

        # Calculate overall quality score
        self.analysis_results["quality_score"] = self._calculate_quality_score()

        # Generate recommendations
        self.analysis_results["recommendations"] = self._generate_recommendations()

        return self.analysis_results

    def _analyze_basic_info(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Analyze basic dataset information."""
        return {
            "shape": df.shape,
            "memory_usage": df.memory_usage(deep=True).sum(),
            "columns": list(df.columns),
            "dtypes": df.dtypes.to_dict(),
            "sample_data": df.head().to_dict()
        }

    def _analyze_missing_data(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Comprehensive missing data analysis."""
        missing_data = {}

        # Overall missing data
        total_missing = df.isnull().sum().sum()
        total_cells = df.size
        missing_percentage = (total_missing / total_cells) * 100

        # Per column missing data
        column_missing = df.isnull().sum()
        column_missing_pct = (column_missing / len(df)) * 100

        # Missing data patterns
        missing_patterns = self._identify_missing_patterns(df)

        missing_data = {
            "total_missing": total_missing,
            "total_cells": total_cells,
            "missing_percentage": missing_percentage,
            "column_missing": column_missing.to_dict(),
            "column_missing_pct": column_missing_pct.to_dict(),
            "missing_patterns": missing_patterns,
            "severity": self._assess_missing_severity(missing_percentage)
        }

        return missing_data

    def _identify_missing_patterns(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Identify patterns in missing data."""
        patterns = {}

        # Check for completely missing columns
        completely_missing = df.columns[df.isnull().all()].tolist()

        # Check for rows with all missing values
        completely_missing_rows = df[df.isnull().all(axis=1)].shape[0]

        # Check for missing data clusters
        missing_matrix = df.isnull()
        missing_clusters = self._find_missing_clusters(missing_matrix)

        patterns = {
            "completely_missing_columns": completely_missing,
            "completely_missing_rows": completely_missing_rows,
            "missing_clusters": missing_clusters
        }

        return patterns

    def _find_missing_clusters(self, missing_matrix: pd.DataFrame) -> List[Dict]:
        """Find clusters of missing data."""
        clusters = []

        # Find consecutive missing values in each column
        for col in missing_matrix.columns:
            missing_series = missing_matrix[col]
            if missing_series.any():
                # Find start and end of missing sequences
                missing_starts = missing_series.ne(missing_series.shift()).cumsum()
                missing_groups = missing_series.groupby(missing_starts)

                for group_id, group in missing_groups:
                    if group.iloc[0]:  # If it's a missing group
                        start_idx = group.index[0]
                        end_idx = group.index[-1]
                        length = len(group)

                        clusters.append({
                            "column": col,
                            "start_index": start_idx,
                            "end_index": end_idx,
                            "length": length,
                            "type": "consecutive"
                        })

        return clusters

    def _assess_missing_severity(self, missing_percentage: float) -> str:
        """Assess severity of missing data."""
        if missing_percentage < 5:
            return "low"
        elif missing_percentage < 20:
            return "medium"
        else:
            return "high"

    def _analyze_duplicates(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Analyze duplicate data."""
        # Exact duplicates
        exact_duplicates = df.duplicated().sum()
        exact_duplicate_pct = (exact_duplicates / len(df)) * 100

        # Duplicate rows
        duplicate_rows = df[df.duplicated(keep=False)]

        # Near duplicates (fuzzy matching)
        near_duplicates = self._find_near_duplicates(df)

        return {
            "exact_duplicates": exact_duplicates,
            "exact_duplicate_pct": exact_duplicate_pct,
            "duplicate_rows": duplicate_rows.shape[0],
            "near_duplicates": near_duplicates,
            "severity": self._assess_duplicate_severity(exact_duplicate_pct)
        }

    def _find_near_duplicates(self, df: pd.DataFrame) -> List[Dict]:
        """Find near-duplicate rows using fuzzy matching."""
        near_duplicates = []

        # For now, implement a simple approach
        # In production, you might use more sophisticated fuzzy matching
        numeric_cols = df.select_dtypes(include=[np.number]).columns

        if len(numeric_cols) > 0:
            # Use correlation to find similar rows
            numeric_df = df[numeric_cols].fillna(0)

            # Find rows with high similarity
            for i in range(len(numeric_df)):
                for j in range(i + 1, len(numeric_df)):
                    similarity = np.corrcoef(
                        numeric_df.iloc[i], numeric_df.iloc[j]
                    )[0, 1]

                    if similarity > 0.95:  # High similarity threshold
                        near_duplicates.append({
                            "row1": i,
                            "row2": j,
                            "similarity": similarity
                        })

        return near_duplicates

    def _assess_duplicate_severity(self, duplicate_pct: float) -> str:
        """Assess severity of duplicate data."""
        if duplicate_pct < 1:
            return "low"
        elif duplicate_pct < 10:
            return "medium"
        else:
            return "high"

    def _analyze_outliers(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Comprehensive outlier analysis using multiple methods."""
        outliers = {}
        numeric_cols = df.select_dtypes(include=[np.number]).columns

        if len(numeric_cols) == 0:
            return {"message": "No numeric columns found for outlier analysis"}

        # Statistical methods
        outliers["statistical"] = self._statistical_outlier_detection(df, numeric_cols)

        # ML-based methods
        outliers["ml_based"] = self._ml_outlier_detection(df, numeric_cols)

        # Combined analysis
        outliers["combined"] = self._combine_outlier_results(
            outliers["statistical"], outliers["ml_based"]
        )

        return outliers

    def _statistical_outlier_detection(self, df: pd.DataFrame,
                                     numeric_cols: pd.Index) -> Dict[str, Any]:
        """Detect outliers using statistical methods."""
        results = {}

        for col in numeric_cols:
            col_data = df[col].dropna()
            if len(col_data) == 0:
                continue

            # IQR method
            Q1 = col_data.quantile(0.25)
            Q3 = col_data.quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR

            iqr_outliers = col_data[
                (col_data < lower_bound) | (col_data > upper_bound)
            ]

            # Z-score method
            z_scores = np.abs(stats.zscore(col_data))
            zscore_outliers = col_data[z_scores > 3]

            # Modified Z-score method
            median = col_data.median()
            mad = np.median(np.abs(col_data - median))
            modified_z_scores = 0.6745 * (col_data - median) / mad
            modified_zscore_outliers = col_data[np.abs(modified_z_scores) > 3.5]

            results[col] = {
                "iqr_outliers": len(iqr_outliers),
                "zscore_outliers": len(zscore_outliers),
                "modified_zscore_outliers": len(modified_zscore_outliers),
                "iqr_bounds": [lower_bound, upper_bound],
                "outlier_indices": {
                    "iqr": iqr_outliers.index.tolist(),
                    "zscore": zscore_outliers.index.tolist(),
                    "modified_zscore": modified_zscore_outliers.index.tolist()
                }
            }

        return results

    def _ml_outlier_detection(self, df: pd.DataFrame,
                             numeric_cols: pd.Index) -> Dict[str, Any]:
        """Detect outliers using machine learning methods."""
        results = {}

        # Prepare data
        numeric_df = df[numeric_cols].fillna(df[numeric_cols].median())

        if len(numeric_df) < 10:  # Need sufficient data
            return {"message": "Insufficient data for ML outlier detection"}

        # Isolation Forest
        try:
            iso_forest = IsolationForest(contamination=0.1, random_state=42)
            iso_predictions = iso_forest.fit_predict(numeric_df)
            iso_outliers = numeric_df[iso_predictions == -1]

            results["isolation_forest"] = {
                "outlier_count": len(iso_outliers),
                "outlier_indices": iso_outliers.index.tolist()
            }
        except Exception as e:
            results["isolation_forest"] = {"error": str(e)}

        # Local Outlier Factor
        try:
            lof = LocalOutlierFactor(contamination=0.1)
            lof_predictions = lof.fit_predict(numeric_df)
            lof_outliers = numeric_df[lof_predictions == -1]

            results["local_outlier_factor"] = {
                "outlier_count": len(lof_outliers),
                "outlier_indices": lof_outliers.index.tolist()
            }
        except Exception as e:
            results["local_outlier_factor"] = {"error": str(e)}

        return results

    def _combine_outlier_results(self, statistical: Dict, ml_based: Dict) -> Dict[str, Any]:
        """Combine results from different outlier detection methods."""
        combined = {
            "total_outliers": 0,
            "high_confidence_outliers": [],
            "method_agreement": {}
        }

        # Count total outliers across all methods
        all_outlier_indices = set()

        # Statistical methods
        for col, results in statistical.items():
            if isinstance(results, dict) and "outlier_indices" in results:
                for method, indices in results["outlier_indices"].items():
                    all_outlier_indices.update(indices)

        # ML methods
        for method, results in ml_based.items():
            if isinstance(results, dict) and "outlier_indices" in results:
                all_outlier_indices.update(results["outlier_indices"])

        combined["total_outliers"] = len(all_outlier_indices)
        combined["all_outlier_indices"] = list(all_outlier_indices)

        return combined

    def _analyze_data_types(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Analyze data types and format inconsistencies."""
        type_analysis = {}

        for col in df.columns:
            col_data = df[col]
            dtype = col_data.dtype

            # Check for mixed types
            mixed_types = self._check_mixed_types(col_data)

            # Check for format inconsistencies
            format_issues = self._check_format_inconsistencies(col_data)

            type_analysis[col] = {
                "dtype": str(dtype),
                "mixed_types": mixed_types,
                "format_issues": format_issues,
                "suggested_dtype": self._suggest_dtype(col_data)
            }

        return type_analysis

    def _check_mixed_types(self, series: pd.Series) -> List[str]:
        """Check for mixed data types in a column."""
        issues = []

        # Check for mixed numeric and string
        numeric_count = pd.to_numeric(series, errors='coerce').notna().sum()
        string_count = len(series) - numeric_count

        if numeric_count > 0 and string_count > 0:
            issues.append("mixed_numeric_string")

        # Check for mixed date formats
        date_formats = self._detect_date_formats(series)
        if len(date_formats) > 1:
            issues.append("mixed_date_formats")

        return issues

    def _check_format_inconsistencies(self, series: pd.Series) -> List[str]:
        """Check for format inconsistencies."""
        issues = []

        # Check for inconsistent string lengths
        if series.dtype == 'object':
            string_lengths = series.str.len().dropna()
            if string_lengths.std() > string_lengths.mean() * 0.5:
                issues.append("inconsistent_string_lengths")

        # Check for currency format inconsistencies
        currency_patterns = series.astype(str).str.contains(r'[\$€£¥]', na=False)
        if currency_patterns.any() and not currency_patterns.all():
            issues.append("inconsistent_currency_formats")

        return issues

    def _detect_date_formats(self, series: pd.Series) -> List[str]:
        """Detect different date formats in a column."""
        date_formats = set()

        for value in series.dropna():
            if isinstance(value, str):
                # Try to parse as date
                try:
                    pd.to_datetime(value)
                    date_formats.add("detected")
                except:
                    pass

        return list(date_formats)

    def _suggest_dtype(self, series: pd.Series) -> str:
        """Suggest optimal data type for a column."""
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

    def _analyze_distributions(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Analyze data distributions."""
        distributions = {}
        numeric_cols = df.select_dtypes(include=[np.number]).columns

        for col in numeric_cols:
            col_data = df[col].dropna()
            if len(col_data) == 0:
                continue

            # Basic statistics
            stats_dict = {
                "mean": col_data.mean(),
                "median": col_data.median(),
                "std": col_data.std(),
                "skewness": col_data.skew(),
                "kurtosis": col_data.kurtosis(),
                "min": col_data.min(),
                "max": col_data.max(),
                "q25": col_data.quantile(0.25),
                "q75": col_data.quantile(0.75)
            }

            # Distribution type assessment
            distribution_type = self._assess_distribution_type(col_data)

            distributions[col] = {
                "statistics": stats_dict,
                "distribution_type": distribution_type,
                "is_normal": self._test_normality(col_data)
            }

        return distributions

    def _assess_distribution_type(self, data: pd.Series) -> str:
        """Assess the type of distribution."""
        skewness = data.skew()
        kurtosis = data.kurtosis()

        if abs(skewness) < 0.5 and abs(kurtosis) < 0.5:
            return "normal"
        elif skewness > 1:
            return "right_skewed"
        elif skewness < -1:
            return "left_skewed"
        else:
            return "approximately_normal"

    def _test_normality(self, data: pd.Series) -> Dict[str, Any]:
        """Test for normality using multiple methods."""
        try:
            # Shapiro-Wilk test
            shapiro_stat, shapiro_p = stats.shapiro(data)

            # Anderson-Darling test
            anderson_result = stats.anderson(data)

            return {
                "shapiro_wilk": {
                    "statistic": shapiro_stat,
                    "p_value": shapiro_p,
                    "is_normal": shapiro_p > 0.05
                },
                "anderson_darling": {
                    "statistic": anderson_result.statistic,
                    "critical_values": anderson_result.critical_values.tolist(),
                    "significance_levels": anderson_result.significance_level.tolist()
                }
            }
        except Exception as e:
            return {"error": str(e)}

    def _analyze_correlations(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Analyze correlations between variables."""
        numeric_cols = df.select_dtypes(include=[np.number]).columns

        if len(numeric_cols) < 2:
            return {"message": "Insufficient numeric columns for correlation analysis"}

        # Pearson correlation
        pearson_corr = df[numeric_cols].corr()

        # Spearman correlation
        spearman_corr = df[numeric_cols].corr(method='spearman')

        # Find high correlations
        high_correlations = self._find_high_correlations(pearson_corr)

        return {
            "pearson_correlation": pearson_corr.to_dict(),
            "spearman_correlation": spearman_corr.to_dict(),
            "high_correlations": high_correlations
        }

    def _find_high_correlations(self, corr_matrix: pd.DataFrame,
                               threshold: float = 0.8) -> List[Dict]:
        """Find highly correlated variable pairs."""
        high_correlations = []

        for i in range(len(corr_matrix.columns)):
            for j in range(i + 1, len(corr_matrix.columns)):
                corr_value = corr_matrix.iloc[i, j]
                if abs(corr_value) >= threshold:
                    high_correlations.append({
                        "variable1": corr_matrix.columns[i],
                        "variable2": corr_matrix.columns[j],
                        "correlation": corr_value,
                        "type": "positive" if corr_value > 0 else "negative"
                    })

        return high_correlations

    def _calculate_quality_score(self) -> float:
        """Calculate overall data quality score."""
        score = 100.0

        # Penalize for missing data
        missing_pct = self.analysis_results["missing_data"]["missing_percentage"]
        score -= missing_pct * 2  # 2 points per percentage of missing data

        # Penalize for duplicates
        duplicate_pct = self.analysis_results["duplicates"]["exact_duplicate_pct"]
        score -= duplicate_pct * 1.5  # 1.5 points per percentage of duplicates

        # Penalize for outliers
        outlier_info = self.analysis_results["outliers"].get("combined", {})
        total_outliers = outlier_info.get("total_outliers", 0)
        total_rows = self.analysis_results["basic_info"]["shape"][0]
        outlier_pct = (total_outliers / total_rows) * 100 if total_rows > 0 else 0
        score -= outlier_pct * 0.5  # 0.5 points per percentage of outliers

        # Ensure score is between 0 and 100
        return max(0.0, min(100.0, score))

    def _generate_recommendations(self) -> List[str]:
        """Generate data quality improvement recommendations."""
        recommendations = []

        # Missing data recommendations
        missing_data = self.analysis_results["missing_data"]
        if missing_data["missing_percentage"] > 5:
            recommendations.append(
                f"High missing data ({missing_data['missing_percentage']:.1f}%). "
                "Consider imputation strategies or data collection improvements."
            )

        # Duplicate recommendations
        duplicates = self.analysis_results["duplicates"]
        if duplicates["exact_duplicate_pct"] > 1:
            recommendations.append(
                f"Duplicate data detected ({duplicates['exact_duplicate_pct']:.1f}%). "
                "Remove duplicates to improve data quality."
            )

        # Outlier recommendations
        outliers = self.analysis_results["outliers"]
        if "combined" in outliers:
            total_outliers = outliers["combined"].get("total_outliers", 0)
            if total_outliers > 0:
                recommendations.append(
                    f"Outliers detected ({total_outliers} points). "
                    "Review and handle outliers appropriately."
                )

        # Data type recommendations
        data_types = self.analysis_results["data_types"]
        for col, analysis in data_types.items():
            if analysis["mixed_types"]:
                recommendations.append(
                    f"Column '{col}' has mixed data types. "
                    "Standardize data format."
                )

        return recommendations

    def generate_visualizations(self) -> Dict[str, Any]:
        """Generate visualization data for the frontend."""
        if not self.analysis_results:
            return {}

        visualizations = {}

        # Missing data visualization
        if "missing_data" in self.analysis_results:
            missing_data = self.analysis_results["missing_data"]
            visualizations["missing_data"] = {
                "type": "bar",
                "data": {
                    "x": list(missing_data["column_missing_pct"].keys()),
                    "y": list(missing_data["column_missing_pct"].values()),
                    "title": "Missing Data by Column (%)"
                }
            }

        # Correlation heatmap
        if "correlations" in self.analysis_results:
            corr_data = self.analysis_results["correlations"]
            if "pearson_correlation" in corr_data:
                visualizations["correlation_heatmap"] = {
                    "type": "heatmap",
                    "data": corr_data["pearson_correlation"],
                    "title": "Correlation Heatmap"
                }

        return visualizations
