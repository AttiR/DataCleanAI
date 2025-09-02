#!/bin/bash

# AutoDataFix - Professional Setup Script
# This script sets up the development environment following best practices

set -e  # Exit on any error

echo "🚀 AutoDataFix - Professional Setup"
echo "===================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Helper functions
print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Check if running from project root
if [ ! -f "README.md" ] || [ ! -d "backend" ] || [ ! -d "frontend" ]; then
    print_error "Please run this script from the AutoDataFix project root directory"
    exit 1
fi

print_info "Setting up AutoDataFix development environment..."

# 1. Check prerequisites
print_info "Checking prerequisites..."

# Check Python
if ! command -v python3 &> /dev/null; then
    print_error "Python 3 is required but not installed"
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1,2)
if ! python3 -c "import sys; exit(0 if sys.version_info >= (3, 9) else 1)"; then
    print_error "Python 3.9+ is required, found version $PYTHON_VERSION"
    exit 1
fi
print_success "Python $PYTHON_VERSION found"

# Check Node.js
if ! command -v node &> /dev/null; then
    print_error "Node.js is required but not installed"
    exit 1
fi

NODE_VERSION=$(node --version)
print_success "Node.js $NODE_VERSION found"

# Check npm
if ! command -v npm &> /dev/null; then
    print_error "npm is required but not installed"
    exit 1
fi

NPM_VERSION=$(npm --version)
print_success "npm $NPM_VERSION found"

# 2. Setup Python virtual environment
print_info "Setting up Python virtual environment..."

if [ ! -d "venv" ]; then
    python3 -m venv venv
    print_success "Virtual environment created"
else
    print_warning "Virtual environment already exists"
fi

# Activate virtual environment
source venv/bin/activate
print_success "Virtual environment activated"

# 3. Install Python dependencies
print_info "Installing Python dependencies..."

# Upgrade pip and build tools
pip install --upgrade pip setuptools wheel
print_success "Build tools upgraded"

# Install backend dependencies
if [ -f "config/requirements.txt" ]; then
    pip install -r config/requirements.txt
    print_success "Backend dependencies installed"
else
    print_error "requirements.txt not found in config/ directory"
    exit 1
fi

# Install development dependencies if available
if [ -f "config/requirements-dev.txt" ]; then
    pip install -r config/requirements-dev.txt
    print_success "Development dependencies installed"
fi

# 4. Setup frontend
print_info "Setting up frontend..."

cd frontend

# Clean install
if [ -d "node_modules" ]; then
    rm -rf node_modules package-lock.json
    print_info "Cleaned existing node_modules"
fi

npm install
print_success "Frontend dependencies installed"

# Return to project root
cd ..

# 5. Setup environment configuration
print_info "Setting up environment configuration..."

if [ ! -f "config/.env" ]; then
    if [ -f "config/env.example" ]; then
        cp config/env.example config/.env
        print_success "Environment file created from template"
        print_warning "Please edit config/.env with your specific settings"
    else
        print_warning "No environment template found"
    fi
else
    print_warning "Environment file already exists"
fi

# 6. Initialize database
print_info "Initializing database..."

cd backend
# Create database directories
mkdir -p database storage/{uploads,models,logs}

# Run database migrations if available
if command -v alembic &> /dev/null; then
    alembic upgrade head 2>/dev/null || print_warning "No alembic migrations found"
fi

cd ..

# 7. Run initial tests
print_info "Running initial tests to verify setup..."

# Test backend
print_info "Testing backend setup..."
cd backend
if python -c "from app.main import app; print('✅ Backend imports successful')" 2>/dev/null; then
    print_success "Backend setup verified"
else
    print_error "Backend setup failed - check dependencies"
fi
cd ..

# Test frontend
print_info "Testing frontend setup..."
cd frontend
if npm run type-check 2>/dev/null; then
    print_success "Frontend TypeScript setup verified"
else
    print_warning "Frontend TypeScript check failed - may need attention"
fi
cd ..

# 8. Setup development tools
print_info "Setting up development tools..."

# Install pre-commit hooks if available
if command -v pre-commit &> /dev/null; then
    pre-commit install 2>/dev/null || true
    print_success "Pre-commit hooks installed"
fi

# 9. Final verification
print_info "Running final verification..."

# Check if we can run the test suite
if python -m pytest tests/unit/ --collect-only &>/dev/null; then
    print_success "Test suite accessible"
else
    print_warning "Test suite may need configuration"
fi

# 10. Setup complete
echo ""
echo "🎉 Setup Complete!"
echo "=================="
print_success "AutoDataFix development environment is ready!"

echo ""
echo "📋 Next Steps:"
echo "1. Review and edit config/.env file"
echo "2. Start the backend: cd backend && uvicorn app.main:app --reload"
echo "3. Start the frontend: cd frontend && npm start"
echo "4. Run tests: python -m pytest tests/"
echo "5. Check the documentation in docs/"

echo ""
echo "🔗 Quick Links:"
echo "• Backend API: http://localhost:8000"
echo "• Frontend: http://localhost:3000"
echo "• API Docs: http://localhost:8000/docs"
echo "• Contributing: docs/dev/CONTRIBUTING.md"

echo ""
print_info "Happy coding! 🚀"

