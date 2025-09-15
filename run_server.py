#!/usr/bin/env python3
"""
AutoDataFix Backend Server Runner
This script ensures the correct Python path is set before starting the server.
"""

import sys
import os
from pathlib import Path

# Add the backend directory to Python path
project_root = Path(__file__).parent
backend_dir = project_root / "backend"
sys.path.insert(0, str(backend_dir))

if __name__ == "__main__":
    import uvicorn

    print("🚀 Starting AutoDataFix Backend...")
    print("🎯 Server will be available at: http://localhost:8000")
    print("📚 API Documentation: http://localhost:8000/docs")
    print("Press Ctrl+C to stop the server")
    print()

    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
