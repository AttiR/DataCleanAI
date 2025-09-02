#!/usr/bin/env python3
"""
Test script for AutoDataFix system
"""

import pandas as pd
import os
import sys

def test_data_creation():
    """Test creating sample data with issues"""
    print("🧪 Testing data creation...")

    # Create a sample dataset with various issues
    data = {
        'id': range(1, 101),
        'name': ['John', 'Jane', None, 'Bob', 'Alice'] * 20,
        'age': [25, 30, 35, None, 40, 45, 50, 55, 60, 65] * 10,
        'salary': [50000, 60000, 70000, 80000, 90000, 100000, 110000, 120000, 130000, 140000] * 10,
        'department': ['IT', 'HR', 'Finance', 'Marketing', 'Sales'] * 20,
        'rating': [4.5, 4.2, 3.8, 4.7, 4.1, 4.3, 3.9, 4.6, 4.4, 3.7] * 10
    }

    # Add some outliers
    data['salary'][0] = 500000  # Outlier
    data['age'][10] = 150  # Outlier

    # Add some duplicates
    data['id'].extend([1, 2, 3])  # Duplicate IDs
    data['name'].extend(['John', 'Jane', 'Bob'])
    data['age'].extend([25, 30, 35])
    data['salary'].extend([50000, 60000, 70000])
    data['department'].extend(['IT', 'HR', 'Finance'])
    data['rating'].extend([4.5, 4.2, 3.8])

    df = pd.DataFrame(data)

    # Save test data
    os.makedirs('data', exist_ok=True)
    df.to_csv('data/test_dataset_with_issues.csv', index=False)

    print(f"✅ Created test dataset with {len(df)} rows and {len(df.columns)} columns")
    print(f"   - Missing values: {df.isnull().sum().sum()}")
    print(f"   - Duplicates: {df.duplicated().sum()}")
    print(f"   - File saved: data/test_dataset_with_issues.csv")

    return df

def test_ml_components():
    """Test ML components"""
    print("\n🧪 Testing ML components...")

    try:
        # Test imports
        sys.path.append('backend')
        from app.ml.data_analyzer import DataQualityAnalyzer
        from app.ml.data_cleaner import AutoDataCleaner

        print("✅ ML components imported successfully")

        # Test analyzer
        analyzer = DataQualityAnalyzer()
        print("✅ DataQualityAnalyzer created")

        # Test cleaner
        cleaner = AutoDataCleaner()
        print("✅ AutoDataCleaner created")

        return True

    except Exception as e:
        print(f"❌ ML component test failed: {e}")
        return False

def test_data_analysis():
    """Test data analysis on sample data"""
    print("\n🧪 Testing data analysis...")

    try:
        # Load test data
        df = pd.read_csv('data/test_dataset_with_issues.csv')

        # Test analysis
        sys.path.append('backend')
        from app.ml.data_analyzer import DataQualityAnalyzer

        analyzer = DataQualityAnalyzer()
        results = analyzer.analyze_dataset(df)

        print("✅ Data analysis completed")
        print(f"   - Quality score: {results['quality_score']:.1f}%")
        print(f"   - Missing data: {results['missing_data']['missing_percentage']:.1f}%")
        print(f"   - Duplicates: {results['duplicates']['exact_duplicate_pct']:.1f}%")
        print(f"   - Outliers: {results['outliers']['combined']['total_outliers']}")

        return True

    except Exception as e:
        print(f"❌ Data analysis test failed: {e}")
        return False

def test_data_cleaning():
    """Test data cleaning on sample data"""
    print("\n🧪 Testing data cleaning...")

    try:
        # Load test data
        df = pd.read_csv('data/test_dataset_with_issues.csv')

        # Test cleaning
        sys.path.append('backend')
        from app.ml.data_cleaner import AutoDataCleaner

        cleaner = AutoDataCleaner()
        cleaned_df = cleaner.clean_dataset(df)

        print("✅ Data cleaning completed")
        print(f"   - Original shape: {df.shape}")
        print(f"   - Cleaned shape: {cleaned_df.shape}")
        print(f"   - Rows removed: {df.shape[0] - cleaned_df.shape[0]}")

        # Save cleaned data
        cleaned_df.to_csv('data/test_dataset_cleaned.csv', index=False)
        print(f"   - Cleaned file saved: data/test_dataset_cleaned.csv")

        return True

    except Exception as e:
        print(f"❌ Data cleaning test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 AutoDataFix System Test")
    print("=" * 50)

    # Test data creation
    test_data_creation()

    # Test ML components
    ml_ok = test_ml_components()

    if ml_ok:
        # Test analysis
        analysis_ok = test_data_analysis()

        # Test cleaning
        cleaning_ok = test_data_cleaning()

        if analysis_ok and cleaning_ok:
            print("\n🎉 All tests passed! System is ready to use.")
        else:
            print("\n⚠️  Some tests failed. Check the output above.")
    else:
        print("\n❌ ML components test failed. Please check your installation.")

    print("\n📊 Test files created:")
    print("   - data/test_dataset_with_issues.csv")
    print("   - data/test_dataset_cleaned.csv")
    print("\n🚀 You can now run './start.sh' to start the full system!")

if __name__ == "__main__":
    main()
