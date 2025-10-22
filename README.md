# Watchtower: Risk Coverage & Drift Monitor

A comprehensive monitoring system for financial crime detection models, providing coverage analysis, drift detection, and automated playbooks.

## 🛡️ Features

- **KPI Monitoring**: Track model performance metrics over time
- **Risk Coverage Analysis**: Monitor coverage across different risk categories
- **Drift Detection**: Detect concept, data, and covariate drift
- **Automated Playbooks**: Respond to alerts with predefined actions
- **Real-time Dashboard**: Streamlit-based monitoring interface
- **REST API**: FastAPI backend for data access and integration
- **Model Training & Serving**: Complete ML pipeline for fraud detection

## 🚀 Quick Start

### Windows Setup

**PowerShell (Recommended):**
```powershell
# Setup environment
.\setup.ps1

# Generate data and train model
.\data.ps1
.\seed.ps1
.\train.ps1

# Start services
.\api.ps1    # Terminal 1 - API server
.\ui.ps1     # Terminal 2 - Dashboard
```

**Command Prompt:**
```cmd
# Setup environment
.\setup.bat

# Generate data and train model
.\data.bat
.\seed.bat
.\train.bat

# Start services
.\api.bat    # Terminal 1 - API server
.\ui.bat     # Terminal 2 - Dashboard
```

### Linux/Mac Setup

```bash
# Setup environment
make setup

# Generate data and train model
make data
make seed
make train

# Start services
make api    # Terminal 1 - API server
make ui     # Terminal 2 - Dashboard
```

## 📱 Access Points

- **API**: http://localhost:8000
- **UI Dashboard**: http://localhost:8501
- **API Docs**: http://localhost:8000/docs

## 🏗️ Architecture

```
watchtower/
├── api/                    # FastAPI backend
│   ├── main.py            # API application
│   └── routes/            # API endpoints
├── models/                 # ML models
│   ├── train_detector.py  # Model training
│   └── serve.py           # Model serving
├── monitoring/             # Monitoring modules
│   ├── coverage.py        # Risk coverage monitoring
│   ├── drift.py           # Drift detection
│   └── alert_kpis.py      # KPI alerting
├── playbooks/             # Automated playbooks
│   ├── registry.yaml      # Playbook registry
│   └── templates/         # Playbook templates
├── ui/                    # Streamlit dashboard
│   └── app.py            # Main dashboard
├── scripts/               # Data generation scripts
└── tests/                 # Test suite
```

## 🔧 Technology Stack

- **Backend**: FastAPI, DuckDB, Pydantic
- **Frontend**: Streamlit, Plotly
- **ML**: scikit-learn, LightGBM, SHAP
- **Data**: Pandas, NumPy
- **Monitoring**: Custom drift detection, coverage analysis
- **Deployment**: Docker, Makefile, Windows batch files

## 📊 Key Components

### Risk Coverage Monitoring
- Monitor coverage across money laundering, terrorist financing, sanctions evasion
- Identify coverage gaps and trends
- Alert on low coverage scenarios

### Drift Detection
- Statistical drift detection using KS tests
- Concept drift monitoring via accuracy tracking
- Covariate drift analysis of feature distributions

### Automated Playbooks
- Trigger-based responses to alerts
- Configurable actions (notifications, retraining, thresholds)
- Execution tracking and logging

### Model Explainability
- SHAP-based feature importance
- Transaction-level explanations
- Global model insights

## 🧪 Testing

```bash
# Run all tests
make test

# Run specific test modules
pytest tests/test_coverage.py
pytest tests/test_drift.py
pytest tests/test_api.py
```

## 🐳 Docker Support

```bash
# Start all services
docker-compose up

# Start individual services
docker-compose up watchtower-api
docker-compose up watchtower-ui
```

## 📝 Development

```bash
# Format code
make format

# Type checking
make typecheck

# Full CI pipeline
make ci
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

MIT License - see LICENSE file for details

## 🆘 Support

For issues and questions:
- Create an issue on GitHub
- Check the documentation in `/docs`
- Review the API documentation at `/docs` endpoint