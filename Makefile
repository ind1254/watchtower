.PHONY: setup data seed train api ui all clean test format typecheck

# Default target
all: setup data seed train

# Setup environment
setup:
	@echo "🔧 Setting up Watchtower environment..."
	pip install --upgrade pip
	pip install -r requirements.txt
	python -m watchtower.config setup
	@echo "✅ Setup complete!"

# Generate synthetic data
data:
	@echo "📊 Generating synthetic data..."
	python scripts/gen_synthetic.py
	python scripts/load_to_duckdb.py
	@echo "✅ Data generation complete!"

# Seed incident data
seed:
	@echo "🌱 Seeding incident data..."
	python scripts/seed_incidents.py
	@echo "✅ Incident seeding complete!"

# Train model
train:
	@echo "🤖 Training fraud detection model..."
	python watchtower/models/train_detector.py
	@echo "✅ Model training complete!"

# Start API server
api:
	@echo "🚀 Starting Watchtower API server..."
	python watchtower/api/main.py

# Start UI dashboard
ui:
	@echo "📱 Starting Watchtower UI dashboard..."
	streamlit run watchtower/ui/app.py --server.port 8501

# Run tests
test:
	@echo "🧪 Running tests..."
	pytest tests/ -v
	@echo "✅ Tests complete!"

# Clean generated files
clean:
	@echo "🧹 Cleaning generated files..."
	rm -rf data/*.duckdb
	rm -rf data/synthetic_*
	rm -rf models/*.pkl
	rm -rf __pycache__/
	rm -rf watchtower/__pycache__/
	rm -rf tests/__pycache__/
	find . -name "*.pyc" -delete
	@echo "✅ Clean complete!"

# Format code
format:
	@echo "🎨 Formatting code..."
	black watchtower/ tests/ scripts/
	isort watchtower/ tests/ scripts/
	@echo "✅ Code formatted!"

# Type check
typecheck:
	@echo "🔍 Running type checks..."
	mypy watchtower/ --ignore-missing-imports
	@echo "✅ Type check complete!"

# Health check
health:
	@echo "🏥 Checking API health..."
	curl -f http://localhost:8000/health || echo "❌ API not responding"

# Full CI pipeline
ci: setup test typecheck format
	@echo "✅ CI pipeline complete!"

# Development mode (API + UI)
dev: api ui

# Production build
build: setup data seed train
	@echo "🏗️ Production build complete!"