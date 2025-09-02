#!/usr/bin/env python3
"""
Test script to verify core functionality of AutoDataFix.
This script tests the core ML components without the problematic libraries.
"""

import sys
import os
import pandas as pd
import numpy as np

# Add the backend directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend'))

def test_data_analyzer():
    """Test the DataQualityAnalyzer."""
    print("Testing DataQualityAnalyzer...")

    try:
        from app.ml.data_analyzer import DataQualityAnalyzer

        # Create sample data with quality issues
        data = {
            'age': [25, 30, None, 45, 150, 35],  # Missing value and outlier
            'income': [50000, 60000, 55000, None, 70000, 65000],  # Missing value
            'category': ['A', 'B', 'A', 'B', 'A', 'A'],  # Categorical
            'score': [85.5, 90.2, 88.1, 92.5, 87.8, 89.3]  # Numeric
        }
        df = pd.DataFrame(data)

        analyzer = DataQualityAnalyzer()
        results = analyzer.analyze_dataset(df)

        print(f"✅ Analysis complete. Quality score: {results['quality_score']:.2f}")
        print(f"   Missing data: {results['missing_data']['missing_percentage']:.1f}%")
        print(f"   Recommendations: {len(results['recommendations'])}")

        return True

    except Exception as e:
        print(f"❌ DataQualityAnalyzer test failed: {e}")
        return False

def test_data_cleaner():
    """Test the AutoDataCleaner."""
    print("\nTesting AutoDataCleaner...")

    try:
        from app.ml.data_cleaner import AutoDataCleaner

        # Create sample data with quality issues
        data = {
            'age': [25, 30, None, 45, 150, 35, 25],  # Missing value, outlier, duplicate
            'income': [50000, 60000, 55000, None, 70000, 65000, 50000],
            'category': ['A', 'B', 'A', 'B', 'A', 'A', 'A'],
            'score': [85.5, 90.2, 88.1, 92.5, 87.8, 89.3, 85.5]
        }
        df = pd.DataFrame(data)

        cleaner = AutoDataCleaner()
        cleaned_df = cleaner.clean_dataset(df)

        summary = cleaner.get_cleaning_summary()

        print(f"✅ Cleaning complete.")
        print(f"   Original shape: {summary['original_shape']}")
        print(f"   Final shape: {summary['final_shape']}")
        print(f"   Cleaning steps: {len(summary['cleaning_steps'])}")

        return True

    except Exception as e:
        print(f"❌ AutoDataCleaner test failed: {e}")
        return False

def test_scikit_learn_alternatives():
    """Test scikit-learn's built-in gradient boosting alternatives."""
    print("\nTesting scikit-learn gradient boosting alternatives...")

    try:
        from sklearn.ensemble import HistGradientBoostingClassifier, HistGradientBoostingRegressor
        from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
        from sklearn.model_selection import train_test_split
        from sklearn.metrics import accuracy_score, mean_squared_error

        # Create sample classification data
        np.random.seed(42)
        X_class = np.random.randn(100, 4)
        y_class = np.random.randint(0, 2, 100)

        X_train, X_test, y_train, y_test = train_test_split(X_class, y_class, test_size=0.2, random_state=42)

        # Test HistGradientBoostingClassifier
        hgb_clf = HistGradientBoostingClassifier(random_state=42, max_iter=50)
        hgb_clf.fit(X_train, y_train)
        y_pred = hgb_clf.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)

        print(f"✅ HistGradientBoostingClassifier accuracy: {accuracy:.3f}")

        # Create sample regression data
        X_reg = np.random.randn(100, 4)
        y_reg = X_reg.sum(axis=1) + np.random.randn(100) * 0.1

        X_train, X_test, y_train, y_test = train_test_split(X_reg, y_reg, test_size=0.2, random_state=42)

        # Test HistGradientBoostingRegressor
        hgb_reg = HistGradientBoostingRegressor(random_state=42, max_iter=50)
        hgb_reg.fit(X_train, y_train)
        y_pred = hgb_reg.predict(X_test)
        mse = mean_squared_error(y_test, y_pred)

        print(f"✅ HistGradientBoostingRegressor MSE: {mse:.3f}")

        # Test RandomForest as fallback
        rf_clf = RandomForestClassifier(n_estimators=10, random_state=42)
        rf_clf.fit(X_train[:, :4], y_class[:len(X_train)])

        print(f"✅ RandomForestClassifier available as fallback")

        return True

    except Exception as e:
        print(f"❌ Scikit-learn alternatives test failed: {e}")
        return False

def test_dependencies():
    """Test that all core dependencies are available."""
    print("\nTesting core dependencies...")

    dependencies = [
        'pandas', 'numpy', 'scipy', 'sklearn', 'plotly',
        'matplotlib', 'seaborn', 'joblib', 'tqdm'
    ]

    failed = []
    for dep in dependencies:
        try:
            __import__(dep)
            print(f"✅ {dep}")
        except ImportError:
            print(f"❌ {dep}")
            failed.append(dep)

    if failed:
        print(f"\n❌ Failed dependencies: {', '.join(failed)}")
        return False
    else:
        print("\n✅ All core dependencies available")
        return True

def main():
    """Run all tests."""
    print("🚀 Testing AutoDataFix Core Functionality")
    print("=" * 50)

    tests = [
        test_dependencies,
        test_data_analyzer,
        test_data_cleaner,
        test_scikit_learn_alternatives
    ]

    passed = 0
    total = len(tests)

    for test in tests:
        if test():
            passed += 1

    print("\n" + "=" * 50)
    print(f"Results: {passed}/{total} tests passed")

    if passed == total:
        print("🎉 All tests passed! AutoDataFix core functionality is working.")
        return 0
    else:
        print("⚠️  Some tests failed. Check the output above for details.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
