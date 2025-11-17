# Watchtower - AML Intelligence Platform

AI-driven AML (Anti-Money Laundering) & Fraud Intelligence platform for transaction risk scoring, identity verification, merchant monitoring, and crypto tracing.

## Features

- **Fraud Detection**: Machine learning model for transaction fraud detection
- **Transaction Risk Analysis**: Analyze and score transaction risk
- **KYC Verification**: Identity verification and compliance checking
- **Merchant Monitoring**: Track and monitor merchant activities
- **Crypto Tracing**: Analyze cryptocurrency transactions
- **Synthetic Data Generation**: Generate realistic synthetic data for testing

## Project Structure

```
watchtower/
├── config.py                 # Configuration settings
├── scripts/                  # All scripts
│   ├── generate_transactions.py
│   ├── generate_crypto.py
│   ├── generate_kyc.py
│   ├── generate_merchants.py
│   ├── generate_all_data.py
│   ├── train_model.py
│   └── api_server.py
├── data/
│   ├── samples/             # Sample training data
│   └── synthetic/           # Generated synthetic data
├── models/                  # Trained ML models
└── requirements.txt         # Python dependencies
```

## Installation

1. **Clone the repository** (if applicable)

2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment**:
   - Windows:
     ```bash
     venv\Scripts\activate
     ```
   - Linux/Mac:
     ```bash
     source venv/bin/activate
     ```

4. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

5. **Set up environment variables** (optional):
   Create a `.env` file in the project root:
   ```env
   OPENAI_API_KEY=your_openai_api_key_here
   SUPABASE_URL=your_supabase_url
   SUPABASE_KEY=your_supabase_key
   ```

## Usage

### 1. Generate Synthetic Data

Generate all synthetic data types:
```bash
python scripts/generate_all_data.py
```

Or generate specific data types:
```bash
python scripts/generate_transactions.py
python scripts/generate_crypto.py
python scripts/generate_kyc.py
python scripts/generate_merchants.py
```

### 2. Train the Model

**Option A: Standard Training (RL or Random Forest)**
```bash
# Train with Reinforcement Learning (default)
python scripts/train_model.py --method rl --episodes 100

# Train with Random Forest
python scripts/train_model.py --method rf
```

**Option B: Extended Training (Recommended for RL)**
For comprehensive RL training with multiple iterations, checkpointing, and progress tracking:
```bash
# Extended training: 20 iterations, 100 episodes each (2000 total episodes)
python scripts/train_extended.py --iterations 20 --episodes 100

# More intensive training
python scripts/train_extended.py --iterations 50 --episodes 200

# Resume from checkpoint
python scripts/train_extended.py --resume models/dqn_model_checkpoint_iter10.pth
```

The trained models will be saved to:
- `models/dqn_model.pth` - Standard RL model
- `models/dqn_model_best.pth` - Best performing RL model (F1 score)
- `models/dqn_model_final.pth` - Final RL model after extended training
- `models/rf_model.joblib` - Random Forest model

### 3. Run the API Server

Start the FastAPI server:
```bash
python scripts/api_server.py
```

Or using uvicorn directly:
```bash
uvicorn scripts.api_server:app --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`

API Documentation: `http://localhost:8000/docs`

## API Endpoints

### POST `/predict`
Predict fraud for a single transaction.

**Request Body:**
```json
{
  "Time": 0.0,
  "V1": 1.191857,
  "V2": 0.266151,
  ...
  "V28": -0.021053,
  "Amount": 149.62
}
```

**Response:**
```json
{
  "is_fraud": false,
  "fraud_probability": 0.0234,
  "risk_score": 2.34
}
```

### POST `/predict/batch`
Predict fraud for a batch of transactions from CSV file.

**Request:** Upload CSV file with columns: Time, V1-V28, Amount

**Response:**
```json
{
  "predictions": [...],
  "total_transactions": 100,
  "fraud_count": 2,
  "fraud_rate": 2.0
}
```

### GET `/health`
Health check endpoint.

## Configuration

Edit `config.py` to customize:

- Number of synthetic records to generate
- API host and port
- Model paths
- Data directories

## Requirements

- Python 3.8+
- pandas
- numpy
- scikit-learn
- fastapi
- faker (for data generation)

See `requirements.txt` for complete list.

## License

[Your License Here]

## Contributing

[Contributing Guidelines Here]

