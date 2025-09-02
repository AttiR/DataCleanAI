#!/bin/bash

# AutoDataFix Dependency Installation Script
# Compatible with Python 3.12 and macOS

set -e  # Exit on any error

echo "🚀 Installing AutoDataFix dependencies..."

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found. Creating one..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "📦 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip and build tools
echo "⬆️  Upgrading pip and build tools..."
pip install --upgrade pip setuptools wheel

# Install main requirements
echo "📋 Installing main requirements..."
pip install -r requirements.txt

echo "✅ Core dependencies installed successfully!"

# Optional: Install ML packages with better error handling
echo ""
echo "🤖 Attempting to install optional ML packages..."
echo "⚠️  These may require additional system dependencies..."

# Try to install gradient boosting libraries
install_optional() {
    local package=$1
    local version=$2
    echo "Trying to install $package..."

    if pip install "$package==$version" 2>/dev/null; then
        echo "✅ $package installed successfully"
    else
        echo "⚠️  Failed to install $package - you can install it later via conda"
        echo "   conda install -c conda-forge $package"
    fi
}

# Try to install optional packages
install_optional "lightgbm" "4.2.0"
install_optional "xgboost" "2.0.3"
install_optional "catboost" "1.2.3"

echo ""
echo "🎉 Installation complete!"
echo ""
echo "📝 Notes:"
echo "   - If any optional ML packages failed, you can install them via conda:"
echo "     conda install -c conda-forge lightgbm xgboost catboost"
echo "   - For macOS users, you may need to install cmake first:"
echo "     brew install cmake libomp"
echo ""
echo "🚀 To start the application:"
echo "   source venv/bin/activate"
echo "   cd backend"
echo "   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000"
