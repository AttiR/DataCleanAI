#!/usr/bin/env python3
"""
Test script to analyze the quality of dummy datasets and verify AutoDataFix functionality.
This script will help you understand what issues exist in each dataset.
"""

import sys
import os
import pandas as pd
import numpy as np
from pathlib import Path

# Add the backend directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend'))

def analyze_dataset_quality(file_path, dataset_name):
    """Analyze the quality issues in a dataset."""
    print(f"\n{'='*60}")
    print(f"ANALYZING: {dataset_name}")
    print(f"File: {file_path}")
    print(f"{'='*60}")

    try:
        # Read the dataset
        df = pd.read_csv(file_path)
        print(f"📊 Dataset Shape: {df.shape[0]} rows × {df.shape[1]} columns")

        # Basic info
        print(f"\n📋 Columns: {list(df.columns)}")

        # Missing data analysis
        missing_data = df.isnull().sum()
        missing_pct = (missing_data / len(df)) * 100

        print(f"\n🔍 MISSING DATA ANALYSIS:")
        print(f"Total missing values: {missing_data.sum()}")
        print(f"Missing data percentage: {(missing_data.sum() / df.size) * 100:.2f}%")

        if missing_data.sum() > 0:
            print("\nColumns with missing data:")
            for col, count in missing_data[missing_data > 0].items():
                print(f"  • {col}: {count} missing ({missing_pct[col]:.1f}%)")

        # Duplicate analysis
        duplicates = df.duplicated().sum()
        if duplicates > 0:
            print(f"\n🔄 DUPLICATES: {duplicates} duplicate rows found")
            duplicate_rows = df[df.duplicated(keep=False)]
            print(f"   Duplicate row indices: {duplicate_rows.index.tolist()}")

        # Data type issues
        print(f"\n📊 DATA TYPES:")
        for col, dtype in df.dtypes.items():
            print(f"  • {col}: {dtype}")

        # Outliers and anomalies
        print(f"\n⚠️  POTENTIAL ISSUES DETECTED:")
        issues_found = []

        for col in df.columns:
            col_issues = []

            # Check for mixed case in text columns
            if df[col].dtype == 'object':
                unique_values = df[col].dropna().astype(str)
                if len(unique_values) > 0:
                    # Check for inconsistent casing
                    case_variations = set()
                    for val in unique_values:
                        case_variations.add(val.lower())
                    if len(case_variations) < len(unique_values.unique()):
                        col_issues.append("Inconsistent text casing")

                    # Check for empty strings
                    if any(val.strip() == '' for val in unique_values):
                        col_issues.append("Empty strings found")

            # Check for outliers in numeric columns
            elif pd.api.types.is_numeric_dtype(df[col]):
                numeric_data = df[col].dropna()
                if len(numeric_data) > 0:
                    # Check for negative values where they shouldn't be
                    if col.lower() in ['age', 'price', 'quantity', 'salary', 'income', 'cost'] and (numeric_data < 0).any():
                        col_issues.append("Negative values in typically positive field")

                    # Check for extreme values
                    Q1 = numeric_data.quantile(0.25)
                    Q3 = numeric_data.quantile(0.75)
                    IQR = Q3 - Q1
                    lower_bound = Q1 - 1.5 * IQR
                    upper_bound = Q3 + 1.5 * IQR
                    outliers = numeric_data[(numeric_data < lower_bound) | (numeric_data > upper_bound)]
                    if len(outliers) > 0:
                        col_issues.append(f"{len(outliers)} statistical outliers")

            if col_issues:
                issues_found.append(f"  • {col}: {', '.join(col_issues)}")

        if issues_found:
            for issue in issues_found:
                print(issue)
        else:
            print("  ✅ No obvious data quality issues detected")

        # Sample problematic rows
        print(f"\n🔍 SAMPLE DATA (first 3 rows):")
        print(df.head(3).to_string())

        return {
            'shape': df.shape,
            'missing_count': missing_data.sum(),
            'missing_percentage': (missing_data.sum() / df.size) * 100,
            'duplicates': duplicates,
            'issues_count': len(issues_found)
        }

    except Exception as e:
        print(f"❌ Error analyzing {dataset_name}: {e}")
        return None

def main():
    """Main function to analyze all test datasets."""
    print("🚀 AutoDataFix - Test Dataset Quality Analysis")
    print("This script analyzes the dummy datasets to show what issues AutoDataFix can fix")

    # Define test datasets
    datasets = [
        ("examples/customer_data_messy.csv", "Customer Data (Messy)"),
        ("examples/sales_data_problematic.csv", "Sales Data (Problematic)"),
        ("examples/employee_performance_dirty.csv", "Employee Performance (Dirty)"),
        ("examples/financial_transactions_messy.csv", "Financial Transactions (Messy)"),
        ("examples/inventory_data_issues.csv", "Inventory Data (Issues)")
    ]

    results = {}

    for file_path, name in datasets:
        # Adjust path to be relative to project root
        full_path = Path(os.path.join(os.path.dirname(__file__), '..', file_path))
        if full_path.exists():
            results[name] = analyze_dataset_quality(full_path, name)
        else:
            print(f"\n❌ File not found: {file_path}")

    # Summary
    print(f"\n{'='*60}")
    print("📊 SUMMARY OF ALL DATASETS")
    print(f"{'='*60}")

    total_datasets = len([r for r in results.values() if r is not None])
    total_rows = sum(r['shape'][0] for r in results.values() if r is not None)
    total_missing = sum(r['missing_count'] for r in results.values() if r is not None)

    print(f"📈 Total datasets analyzed: {total_datasets}")
    print(f"📊 Total data points: {total_rows}")
    print(f"🔍 Total missing values: {total_missing}")
    print(f"⚠️  Average data quality issues per dataset: {sum(r['issues_count'] for r in results.values() if r is not None) / total_datasets:.1f}")

    print(f"\n🎯 WHAT AUTODATAFIX CAN HELP WITH:")
    print("✅ Missing data imputation (mean, median, mode, KNN)")
    print("✅ Outlier detection and treatment")
    print("✅ Duplicate row removal")
    print("✅ Data type standardization")
    print("✅ Text case normalization")
    print("✅ Date format standardization")
    print("✅ Data validation and quality scoring")

    print(f"\n🚀 READY TO TEST!")
    print("Upload these datasets to AutoDataFix to see the cleaning in action:")
    for file_path, name in datasets:
        full_path = Path(os.path.join(os.path.dirname(__file__), '..', file_path))
        if full_path.exists():
            print(f"  📁 {file_path}")

if __name__ == "__main__":
    main()
