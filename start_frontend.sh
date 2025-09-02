#!/bin/bash

# AutoDataFix Frontend Startup Script

echo "⚛️ Starting AutoDataFix Frontend..."

# Check if we're in the project root
if [ ! -f "README.md" ] || [ ! -d "frontend" ]; then
    echo "❌ Please run this script from the AutoDataFix project root directory"
    exit 1
fi

# Change to frontend directory
echo "📂 Changing to frontend directory..."
cd frontend

# Check if node_modules exists
if [ ! -d "node_modules" ]; then
    echo "📦 Installing dependencies..."
    npm install
fi

# Start the frontend
echo "🎯 Starting React frontend on http://localhost:3000"
echo ""
echo "Press Ctrl+C to stop the frontend"
echo ""

npm start
