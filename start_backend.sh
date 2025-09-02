#!/bin/bash

# AutoDataFix Backend Startup Script

echo "🚀 Starting AutoDataFix Backend..."

# Check if we're in the project root
if [ ! -f "README.md" ] || [ ! -d "backend" ]; then
    echo "❌ Please run this script from the AutoDataFix project root directory"
    exit 1
fi

# Activate virtual environment
echo "📦 Activating virtual environment..."
source venv/bin/activate

# Change to backend directory
echo "📂 Changing to backend directory..."
cd backend

# Start the backend
echo "🎯 Starting FastAPI backend on http://localhost:8000"
echo "📚 API Documentation: http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop the backend"
echo ""

uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
