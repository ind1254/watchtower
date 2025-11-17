"""Train the fraud detection model using Reinforcement Learning."""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score
import joblib
from pathlib import Path
import sys
import argparse
from typing import Optional

sys.path.append(str(Path(__file__).parent.parent))
from config import SAMPLES_DIR, MODEL_PATH, MODELS_DIR, SYNTHETIC_DIR

# Import RL components
try:
    from scripts.rl_environment import FraudDetectionEnv
    from scripts.rl_agent import DQNAgent
    RL_AVAILABLE = True
except ImportError as e:
    RL_AVAILABLE = False
    print(f"Warning: RL components not available: {e}")

def load_training_data(use_synthetic: bool = True):
    """
    Load training data from samples or synthetic directory.
    
    Args:
        use_synthetic: If True, use synthetic data; otherwise use samples
    
    Returns:
        DataFrame with transaction data
    """
    if use_synthetic:
        data_path = SYNTHETIC_DIR / "transactions" / "transactions_pca.csv"
        if not data_path.exists():
            print(f"Synthetic data not found at {data_path}, trying samples...")
            data_path = SAMPLES_DIR / "transactions.csv"
    else:
        data_path = SAMPLES_DIR / "transactions.csv"
    
    if not data_path.exists():
        raise FileNotFoundError(
            f"Training data not found at {data_path}. "
            "Please ensure the transactions.csv file exists or generate synthetic data first."
        )
    
    df = pd.read_csv(data_path)
    print(f"Loaded {len(df)} transactions from {data_path}")
    return df

def prepare_features(df):
    """Prepare features and target for training."""
    # Extract feature columns (Time, V1-V28, Amount)
    feature_cols = ['Time'] + [f'V{i}' for i in range(1, 29)] + ['Amount']
    X = df[feature_cols].values
    y = df['Class'].values
    
    print(f"Features shape: {X.shape}")
    print(f"Target distribution: {y.sum()} fraud ({y.mean() * 100:.2f}%)")
    
    return X, y

def train_model(X, y, test_size=0.2, random_state=42):
    """Train the random forest model."""
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state, stratify=y
    )
    
    print(f"\nTraining set: {len(X_train)} samples")
    print(f"Test set: {len(X_test)} samples")
    
    # Train model
    print("\nTraining Random Forest model...")
    model = RandomForestClassifier(
        n_estimators=100,
        max_depth=20,
        min_samples_split=5,
        min_samples_leaf=2,
        random_state=random_state,
        n_jobs=-1,
        class_weight='balanced'
    )
    
    model.fit(X_train, y_train)
    
    # Evaluate model
    print("\nEvaluating model...")
    y_pred = model.predict(X_test)
    y_pred_proba = model.predict_proba(X_test)[:, 1]
    
    print("\n" + "=" * 60)
    print("Classification Report:")
    print("=" * 60)
    print(classification_report(y_test, y_pred))
    
    print("\n" + "=" * 60)
    print("Confusion Matrix:")
    print("=" * 60)
    print(confusion_matrix(y_test, y_pred))
    
    auc_score = roc_auc_score(y_test, y_pred_proba)
    print(f"\nROC-AUC Score: {auc_score:.4f}")
    
    # Feature importance
    print("\n" + "=" * 60)
    print("Top 10 Most Important Features:")
    print("=" * 60)
    feature_cols = ['Time'] + [f'V{i}' for i in range(1, 29)] + ['Amount']
    feature_importance = pd.DataFrame({
        'feature': feature_cols,
        'importance': model.feature_importances_
    }).sort_values('importance', ascending=False)
    
    print(feature_importance.head(10).to_string(index=False))
    
    return model, X_test, y_test, y_pred

def save_model(model):
    """Save the trained model."""
    MODELS_DIR.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, MODEL_PATH)
    print(f"\nModel saved to {MODEL_PATH}")

def train_rl_model(df: pd.DataFrame, episodes: int = 100, use_synthetic: bool = True):
    """
    Train the fraud detection model using Reinforcement Learning.
    
    Args:
        df: DataFrame with transaction data
        episodes: Number of training episodes
        use_synthetic: Whether using synthetic data
    
    Returns:
        Trained DQN agent
    """
    print("\n" + "=" * 60)
    print("Training Fraud Detection Model with Reinforcement Learning")
    print("=" * 60)
    
    # Split data into train and test
    train_df, test_df = train_test_split(
        df, test_size=0.2, random_state=42, stratify=df['Class']
    )
    
    print(f"\nTraining set: {len(train_df)} transactions")
    print(f"Test set: {len(test_df)} transactions")
    print(f"Fraud rate in training: {train_df['Class'].mean() * 100:.2f}%")
    
    # Create environment
    env = FraudDetectionEnv(train_df)
    
    # Create agent
    state_dim = 30  # Time + V1-V28 + Amount
    action_dim = 2  # Flag or not
    agent = DQNAgent(
        state_dim=state_dim,
        action_dim=action_dim,
        lr=0.001,
        gamma=0.99,
        epsilon=1.0,
        epsilon_min=0.01,
        epsilon_decay=0.995,
        memory_size=10000,
        batch_size=64,
        target_update_freq=100
    )
    
    # Training loop
    print(f"\nTraining for {episodes} episodes...")
    episode_rewards = []
    episode_metrics = []
    
    for episode in range(episodes):
        state, info = env.reset()
        total_reward = 0
        done = False
        
        while not done:
            # Agent chooses action
            action = agent.act(state, training=True)
            
            # Environment step
            next_state, reward, terminated, truncated, step_info = env.step(action)
            done = terminated or truncated
            
            # Store experience
            agent.remember(state, action, reward, next_state, done)
            
            # Train agent
            loss = agent.replay()
            
            state = next_state
            total_reward += reward
        
        # Get episode metrics
        metrics = env.get_metrics()
        episode_rewards.append(total_reward)
        episode_metrics.append(metrics)
        
        # Print progress
        if (episode + 1) % 10 == 0 or episode == 0:
            print(f"\nEpisode {episode + 1}/{episodes}")
            print(f"  Total Reward: {total_reward:.2f}")
            print(f"  Accuracy: {metrics.get('accuracy', 0):.4f}")
            print(f"  Precision: {metrics.get('precision', 0):.4f}")
            print(f"  Recall: {metrics.get('recall', 0):.4f}")
            print(f"  F1 Score: {metrics.get('f1_score', 0):.4f}")
            print(f"  Epsilon: {agent.epsilon:.4f}")
            if loss:
                print(f"  Avg Loss: {np.mean(agent.losses[-100:]):.6f}")
    
    # Evaluate on test set
    print("\n" + "=" * 60)
    print("Evaluating on Test Set")
    print("=" * 60)
    
    test_env = FraudDetectionEnv(test_df)
    state, info = test_env.reset()
    done = False
    
    # Disable exploration for evaluation
    agent.epsilon = 0.0
    
    while not done:
        action = agent.act(state, training=False)
        next_state, reward, terminated, truncated, step_info = test_env.step(action)
        done = terminated or truncated
        state = next_state
    
    test_metrics = test_env.get_metrics()
    
    print("\nTest Set Performance:")
    print(f"  Accuracy: {test_metrics.get('accuracy', 0):.4f}")
    print(f"  Precision: {test_metrics.get('precision', 0):.4f}")
    print(f"  Recall: {test_metrics.get('recall', 0):.4f}")
    print(f"  F1 Score: {test_metrics.get('f1_score', 0):.4f}")
    print(f"\n  True Positives: {test_metrics.get('true_positives', 0)}")
    print(f"  True Negatives: {test_metrics.get('true_negatives', 0)}")
    print(f"  False Positives: {test_metrics.get('false_positives', 0)}")
    print(f"  False Negatives: {test_metrics.get('false_negatives', 0)}")
    
    return agent, episode_rewards, episode_metrics, test_metrics


def save_rl_model(agent: DQNAgent, model_path: Optional[Path] = None):
    """Save the trained RL model."""
    if model_path is None:
        model_path = MODELS_DIR / "dqn_model.pth"
    
    MODELS_DIR.mkdir(parents=True, exist_ok=True)
    agent.save(str(model_path))
    print(f"\nRL Model saved to {model_path}")


def main():
    """Main training function."""
    parser = argparse.ArgumentParser(description='Train fraud detection model')
    parser.add_argument('--method', type=str, default='rl', choices=['rl', 'rf'],
                        help='Training method: rl (reinforcement learning) or rf (random forest)')
    parser.add_argument('--episodes', type=int, default=100,
                        help='Number of training episodes for RL (default: 100)')
    parser.add_argument('--use-synthetic', action='store_true', default=True,
                        help='Use synthetic data for training')
    parser.add_argument('--no-synthetic', dest='use_synthetic', action='store_false',
                        help='Use sample data instead of synthetic')
    
    args = parser.parse_args()
    
    print("=" * 60)
    print("Training Fraud Detection Model")
    print("=" * 60)
    
    try:
        # Load data
        df = load_training_data(use_synthetic=args.use_synthetic)
        
        if args.method == 'rl':
            if not RL_AVAILABLE:
                print("\nError: RL components not available. Please install dependencies:")
                print("  pip install gymnasium torch")
                sys.exit(1)
            # Train with Reinforcement Learning
            agent, rewards, metrics, test_metrics = train_rl_model(
                df, episodes=args.episodes, use_synthetic=args.use_synthetic
            )
            save_rl_model(agent)
            
            print("\n" + "=" * 60)
            print("RL Model training complete!")
            print("=" * 60)
        else:
            # Train with Random Forest (original method)
            X, y = prepare_features(df)
            model, X_test, y_test, y_pred = train_model(X, y)
            save_model(model)
            
            print("\n" + "=" * 60)
            print("Random Forest Model training complete!")
            print("=" * 60)
        
    except Exception as e:
        print(f"\nError during training: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()

