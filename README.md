# DataCleanAI - AI-Powered Data Quality System

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.108+-green.svg)](https://fastapi.tiangolo.com)
[![React](https://img.shields.io/badge/React-18+-blue.svg)](https://reactjs.org)
[![TypeScript](https://img.shields.io/badge/TypeScript-4.9+-blue.svg)](https://www.typescriptlang.org)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

An advanced AI-powered system that automatically detects and rectifies common data quality issues, making datasets ready for analysis or modeling.

## 🏗️ Project Architecture

This project follows clean software architecture principles with clear separation of concerns:

```
DataCleanAI/
├── backend/                    # Python FastAPI backend
│   ├── app/                   # Application core
│   │   ├── api/              # API routes and endpoints
│   │   ├── core/             # Configuration and utilities
│   │   ├── models/           # Database models
│   │   ├── services/         # Business logic layer
│   │   └── ml/               # Machine learning components
│   ├── database/             # Database files
│   ├── static/               # Static files (if any)
│   └── storage/              # File storage (uploads, models, logs)
├── frontend/                 # React TypeScript frontend
│   ├── public/               # Static assets
│   └── src/                  # Source code
│       ├── components/       # Reusable UI components
│       ├── pages/            # Page components
│       └── services/         # API communication
├── tests/                    # Test files for backend
├── docs/                     # Documentation
├── config/                   # Configuration files
├── scripts/                  # Utility and start scripts (e.g., start_backend.sh, start_frontend.sh)
├── examples/                 # Sample datasets for testing
├── LICENSE                   # License file
└── README.md                 # Project overview
```

## 🚀 Quick Start

### Prerequisites
- Python 3.9+ (Python 3.12 recommended)
- Node.js 16+
- npm or yarn

### Installation

#### Option 1: Quick Setup (Recommended)
All start and setup scripts are located in the `scripts/` folder.
```bash
cd scripts
./start_backend.sh
./start_frontend.sh
```
# Clone and navigate
git clone <repository-url>
cd AutoDataFix

# Run setup script
./scripts/install_dependencies.sh
```

#### Option 2: Manual Setup
```bash
# Backend setup
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r config/requirements.txt

# Frontend setup
cd frontend
npm install
```

### Running the Application

#### Start Backend
```bash
source venv/bin/activate
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

#### Start Frontend
```bash
cd frontend
npm start
```

### Access Points
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

## 📊 Features

### Data Analysis & Diagnosis
- **Missing Values Detection**: Advanced algorithms to identify missing data patterns
- **Outlier Detection**: Multiple statistical and ML-based methods
- **Duplicate Detection**: Intelligent duplicate identification
- **Data Type Analysis**: Automatic detection of format inconsistencies
- **Distribution Analysis**: Statistical analysis and skewness detection

### Data Cleaning & Transformation
- **Smart Imputation**: Automatic selection of best imputation strategy
- **Outlier Treatment**: Remove, cap, or transform based on context
- **Feature Scaling**: Min-Max, Standard, Robust scaling
- **Categorical Encoding**: One-Hot, Label, Target encoding
- **Date/Time Processing**: Automatic standardization

### Machine Learning Pipeline
- **AutoML Integration**: Automated feature engineering
- **Model Selection**: Automatic algorithm selection
- **Hyperparameter Tuning**: Bayesian optimization
- **Cross-Validation**: Robust model evaluation

## 🧪 Testing

### Run Tests
```bash
# Run all tests
python -m pytest tests/

# Run specific test
python tests/test_data_quality.py

# Test with sample data
python tests/test_core_functionality.py
```

### Test with Sample Data
```bash
# Analyze sample datasets
python tests/unit/test_data_quality.py

# Test core functionality
python tests/unit/test_core_functionality.py
```

## 📚 Documentation

- **[Contributing Guide](docs/CONTRIBUTING.md)** - Development setup and contribution guidelines
- **[Architecture Guide](docs/ARCHITECTURE.md)** - System architecture overview

## 🛠️ Development

### Project Structure Guidelines
- **backend/app/**: Follow FastAPI best practices
- **frontend/src/**: React components with TypeScript
- **tests/**: Comprehensive test coverage
- **docs/**: Keep documentation updated
- **config/**: Environment-specific configurations

### Code Quality
- **Linting**: ESLint for frontend, Black for backend
- **Type Checking**: TypeScript for frontend, mypy for backend
- **Testing**: Jest for frontend, pytest for backend
- **Documentation**: Comprehensive docstrings and README files

## 🐳 Deployment

### Simple Deployment
```bash
# Run backend
cd backend && uvicorn app.main:app --host 0.0.0.0 --port 8000

# Run frontend (in new terminal)
cd frontend && npm start
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Follow the coding standards
4. Add tests for new functionality
5. Update documentation
6. Submit a pull request

See [CONTRIBUTING.md](docs/CONTRIBUTING.md) for detailed guidelines.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

- **Documentation**: Check the [docs](docs/) folder
- **Issues**: Create an issue on GitHub
- **API Reference**: Visit http://localhost:8000/docs when running

## 🔗 Links

- **Project Documentation**: [docs/](docs/)
- **API Documentation**: [docs/api/](docs/api/)
- **User Guide**: [docs/user/](docs/user/)
- **Developer Guide**: [docs/dev/](docs/dev/)

---

**Built with ❤️ for data scientists and analysts**
