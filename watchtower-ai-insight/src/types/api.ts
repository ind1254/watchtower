/** API response types matching FastAPI backend */

export interface TransactionResponse {
  is_fraud: boolean;
  fraud_probability: number;
  risk_score: number;
}

export interface BatchTransactionResponse {
  predictions: TransactionResponse[];
  total_transactions: number;
  fraud_count: number;
  fraud_rate: number;
}

export interface ApiError {
  detail: string;
}

export interface HealthCheckResponse {
  status: string;
  models: {
    random_forest: {
      loaded: boolean;
      available: boolean;
    };
    dqn: {
      loaded: boolean;
      available: boolean;
    };
  };
  default_model: string;
}

