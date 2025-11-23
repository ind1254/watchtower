"""Model evaluation script for comparing DQN and Random Forest models."""

import pandas as pd
import numpy as np
import torch
import joblib
import argparse
from pathlib import Path
from datetime import datetime
from typing import Dict, Tuple, Optional
import sys

from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    roc_auc_score, confusion_matrix, classification_report
)

sys.path.append(str(Path(__file__).parent.parent))
from config import MODEL_PATH, DQN_MODEL_PATH, NORM_PARAMS_PATH, MODELS_DIR

# Import existing utilities
from scripts.train_model import load_training_data, prepare_features
from scripts.model_utils import load_normalizer
from scripts.rl_agent import DQNAgent


def load_and_split_data(use_synthetic: bool = True, test_size: float = 0.2, random_state: int = 42) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Load data and split into train/test sets.
    
    Args:
        use_synthetic: Whether to use synthetic data
        test_size: Proportion of data for test set
        random_state: Random seed for reproducibility
        
    Returns:
        Tuple of (train_df, test_df)
    """
    print("Loading data...")
    df = load_training_data(use_synthetic=use_synthetic)
    
    print(f"Total transactions: {len(df)}")
    print(f"Fraud rate: {df['Class'].mean() * 100:.2f}%")
    
    # Split data
    train_df, test_df = train_test_split(
        df, test_size=test_size, random_state=random_state, stratify=df['Class']
    )
    
    print(f"\nTrain set: {len(train_df)} transactions ({len(train_df)/len(df)*100:.1f}%)")
    print(f"Test set: {len(test_df)} transactions ({len(test_df)/len(df)*100:.1f}%)")
    print(f"Test set fraud rate: {test_df['Class'].mean() * 100:.2f}%")
    
    return train_df, test_df


def load_models() -> Tuple[Optional[object], Optional[DQNAgent], Optional[object]]:
    """
    Load Random Forest, DQN models, and normalizer.
    
    Returns:
        Tuple of (rf_model, dqn_agent, normalizer)
    """
    rf_model = None
    dqn_agent = None
    normalizer = None
    
    # Load Random Forest model
    print("\nLoading Random Forest model...")
    try:
        rf_model = joblib.load(MODEL_PATH)
        print(f"✓ Random Forest model loaded from {MODEL_PATH}")
    except FileNotFoundError:
        print(f"✗ Random Forest model not found at {MODEL_PATH}")
    except Exception as e:
        print(f"✗ Error loading Random Forest model: {e}")
    
    # Load DQN model
    print("\nLoading DQN model...")
    try:
        dqn_agent = DQNAgent(state_dim=30, action_dim=2)
        dqn_agent.load(str(DQN_MODEL_PATH))
        dqn_agent.q_network.eval()  # Set to evaluation mode
        dqn_agent.epsilon = 0.0  # Disable exploration
        print(f"✓ DQN model loaded from {DQN_MODEL_PATH}")
    except FileNotFoundError:
        print(f"✗ DQN model not found at {DQN_MODEL_PATH}")
    except Exception as e:
        print(f"✗ Error loading DQN model: {e}")
        dqn_agent = None
    
    # Load normalizer
    if dqn_agent is not None:
        print("\nLoading normalization parameters...")
        try:
            normalizer = load_normalizer(NORM_PARAMS_PATH)
            print(f"✓ Normalization parameters loaded")
        except Exception as e:
            print(f"✗ Error loading normalization parameters: {e}")
            normalizer = None
    
    return rf_model, dqn_agent, normalizer


def evaluate_rf_model(rf_model, X_test: np.ndarray, y_test: np.ndarray) -> Dict:
    """
    Evaluate Random Forest model.
    
    Args:
        rf_model: Trained Random Forest model
        X_test: Test features
        y_test: Test labels
        
    Returns:
        Dictionary with predictions, probabilities, and metrics
    """
    print("\nEvaluating Random Forest model...")
    
    # Predict
    y_pred = rf_model.predict(X_test)
    y_pred_proba = rf_model.predict_proba(X_test)[:, 1]
    
    # Compute metrics
    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred, zero_division=0)
    recall = recall_score(y_test, y_pred, zero_division=0)
    f1 = f1_score(y_test, y_pred, zero_division=0)
    
    try:
        roc_auc = roc_auc_score(y_test, y_pred_proba)
    except ValueError:
        roc_auc = 0.0
    
    cm = confusion_matrix(y_test, y_pred)
    tn, fp, fn, tp = cm.ravel() if cm.size == 4 else (0, 0, 0, 0)
    
    return {
        'model_name': 'Random Forest',
        'y_pred': y_pred,
        'y_pred_proba': y_pred_proba,
        'accuracy': accuracy,
        'precision': precision,
        'recall': recall,
        'f1_score': f1,
        'roc_auc': roc_auc,
        'confusion_matrix': cm,
        'true_positives': int(tp),
        'true_negatives': int(tn),
        'false_positives': int(fp),
        'false_negatives': int(fn),
        'mean_probability': float(np.mean(y_pred_proba)),
        'std_probability': float(np.std(y_pred_proba))
    }


def evaluate_dqn_model(dqn_agent: DQNAgent, normalizer, X_test: np.ndarray, y_test: np.ndarray) -> Dict:
    """
    Evaluate DQN model.
    
    Args:
        dqn_agent: Trained DQN agent
        normalizer: Feature normalizer
        X_test: Test features
        y_test: Test labels
        
    Returns:
        Dictionary with predictions, probabilities, and metrics
    """
    print("\nEvaluating DQN model...")
    
    # Normalize features
    normalized_features = normalizer.transform(X_test)
    
    # Get Q-values from DQN
    with torch.no_grad():
        features_tensor = torch.FloatTensor(normalized_features).to(dqn_agent.device)
        q_values = dqn_agent.q_network(features_tensor)
    
    # Convert Q-values to probabilities using softmax
    q_values_np = q_values.cpu().numpy()
    exp_q = np.exp(q_values_np - np.max(q_values_np, axis=-1, keepdims=True))
    probabilities = exp_q / np.sum(exp_q, axis=-1, keepdims=True)
    
    # Extract fraud probability (action 1)
    y_pred_proba = probabilities[:, 1]
    y_pred = (y_pred_proba > 0.5).astype(int)
    
    # Compute metrics
    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred, zero_division=0)
    recall = recall_score(y_test, y_pred, zero_division=0)
    f1 = f1_score(y_test, y_pred, zero_division=0)
    
    try:
        roc_auc = roc_auc_score(y_test, y_pred_proba)
    except ValueError:
        roc_auc = 0.0
    
    cm = confusion_matrix(y_test, y_pred)
    tn, fp, fn, tp = cm.ravel() if cm.size == 4 else (0, 0, 0, 0)
    
    return {
        'model_name': 'DQN',
        'y_pred': y_pred,
        'y_pred_proba': y_pred_proba,
        'accuracy': accuracy,
        'precision': precision,
        'recall': recall,
        'f1_score': f1,
        'roc_auc': roc_auc,
        'confusion_matrix': cm,
        'true_positives': int(tp),
        'true_negatives': int(tn),
        'false_positives': int(fp),
        'false_negatives': int(fn),
        'mean_probability': float(np.mean(y_pred_proba)),
        'std_probability': float(np.std(y_pred_proba))
    }


def compare_models(rf_results: Optional[Dict], dqn_results: Optional[Dict]) -> Dict:
    """Compare two models and identify winners for each metric."""
    comparison = {'metrics': {}, 'winners': {}, 'differences': {}}
    metrics_to_compare = ['accuracy', 'precision', 'recall', 'f1_score', 'roc_auc']
    
    for metric in metrics_to_compare:
        rf_val = rf_results.get(metric, 0) if rf_results else None
        dqn_val = dqn_results.get(metric, 0) if dqn_results else None
        
        comparison['metrics'][metric] = {'random_forest': rf_val, 'dqn': dqn_val}
        
        if rf_val is None and dqn_val is None:
            winner = None
        elif rf_val is None:
            winner = 'DQN'
        elif dqn_val is None:
            winner = 'Random Forest'
        elif dqn_val > rf_val:
            winner = 'DQN'
        elif rf_val > dqn_val:
            winner = 'Random Forest'
        else:
            winner = 'Tie'
        
        comparison['winners'][metric] = winner
        
        if rf_val is not None and dqn_val is not None:
            diff = dqn_val - rf_val
            comparison['differences'][metric] = {
                'absolute': diff,
                'relative': (diff / rf_val * 100) if rf_val > 0 else 0
            }
    
    return comparison


def generate_report(rf_results: Optional[Dict], dqn_results: Optional[Dict], 
                   comparison: Dict, test_df: pd.DataFrame, timestamp: str) -> str:
    """Generate formatted evaluation report."""
    report_lines = []
    report_lines.append("=" * 70)
    report_lines.append("MODEL EVALUATION REPORT")
    report_lines.append("=" * 70)
    report_lines.append(f"Date: {timestamp}")
    report_lines.append(f"Test Set Size: {len(test_df)} transactions")
    report_lines.append(f"Test Set Fraud Rate: {test_df['Class'].mean() * 100:.2f}%")
    report_lines.append("")
    
    if rf_results:
        report_lines.append("-" * 70)
        report_lines.append("RANDOM FOREST MODEL")
        report_lines.append("-" * 70)
        report_lines.append(f"Accuracy:  {rf_results['accuracy']:.4f}")
        report_lines.append(f"Precision: {rf_results['precision']:.4f}")
        report_lines.append(f"Recall:    {rf_results['recall']:.4f}")
        report_lines.append(f"F1-Score:  {rf_results['f1_score']:.4f}")
        report_lines.append(f"ROC-AUC:   {rf_results['roc_auc']:.4f}")
        report_lines.append("")
        report_lines.append("Confusion Matrix:")
        report_lines.append("                Predicted")
        report_lines.append("Actual      Normal    Fraud")
        report_lines.append(f"Normal      {rf_results['true_negatives']:6d}    {rf_results['false_positives']:6d}")
        report_lines.append(f"Fraud       {rf_results['false_negatives']:6d}    {rf_results['true_positives']:6d}")
        report_lines.append("")
        report_lines.append(f"Mean Probability: {rf_results['mean_probability']:.4f}")
        report_lines.append(f"Std Probability:  {rf_results['std_probability']:.4f}")
    else:
        report_lines.append("-" * 70)
        report_lines.append("RANDOM FOREST MODEL: Not Available")
        report_lines.append("-" * 70)
        report_lines.append("")
    
    if dqn_results:
        report_lines.append("-" * 70)
        report_lines.append("DQN MODEL")
        report_lines.append("-" * 70)
        report_lines.append(f"Accuracy:  {dqn_results['accuracy']:.4f}")
        report_lines.append(f"Precision: {dqn_results['precision']:.4f}")
        report_lines.append(f"Recall:    {dqn_results['recall']:.4f}")
        report_lines.append(f"F1-Score:  {dqn_results['f1_score']:.4f}")
        report_lines.append(f"ROC-AUC:   {dqn_results['roc_auc']:.4f}")
        report_lines.append("")
        report_lines.append("Confusion Matrix:")
        report_lines.append("                Predicted")
        report_lines.append("Actual      Normal    Fraud")
        report_lines.append(f"Normal      {dqn_results['true_negatives']:6d}    {dqn_results['false_positives']:6d}")
        report_lines.append(f"Fraud       {dqn_results['false_negatives']:6d}    {dqn_results['true_positives']:6d}")
        report_lines.append("")
        report_lines.append(f"Mean Probability: {dqn_results['mean_probability']:.4f}")
        report_lines.append(f"Std Probability:  {dqn_results['std_probability']:.4f}")
    else:
        report_lines.append("-" * 70)
        report_lines.append("DQN MODEL: Not Available")
        report_lines.append("-" * 70)
        report_lines.append("")
    
    if rf_results and dqn_results:
        report_lines.append("=" * 70)
        report_lines.append("COMPARISON")
        report_lines.append("=" * 70)
        report_lines.append("Winner by Metric:")
        for metric in ['accuracy', 'precision', 'recall', 'f1_score', 'roc_auc']:
            winner = comparison['winners'].get(metric, 'N/A')
            metric_name = metric.replace('_', ' ').title()
            report_lines.append(f"  {metric_name:12s}: {winner}")
        report_lines.append("")
        
        report_lines.append("Recommendations:")
        rf_f1 = rf_results['f1_score']
        dqn_f1 = dqn_results['f1_score']
        
        if dqn_f1 > rf_f1:
            report_lines.append(f"  • DQN model has better overall performance (F1: {dqn_f1:.4f} vs {rf_f1:.4f})")
        elif rf_f1 > dqn_f1:
            report_lines.append(f"  • Random Forest has better overall performance (F1: {rf_f1:.4f} vs {dqn_f1:.4f})")
        else:
            report_lines.append("  • Both models perform similarly")
        
        if dqn_results['recall'] > rf_results['recall']:
            report_lines.append(f"  • DQN has higher recall ({dqn_results['recall']:.4f} vs {rf_results['recall']:.4f}) - better at catching fraud")
        elif rf_results['recall'] > dqn_results['recall']:
            report_lines.append(f"  • Random Forest has higher recall ({rf_results['recall']:.4f} vs {dqn_results['recall']:.4f}) - better at catching fraud")
        
        if dqn_results['precision'] > rf_results['precision']:
            report_lines.append(f"  • DQN has higher precision ({dqn_results['precision']:.4f} vs {rf_results['precision']:.4f}) - fewer false positives")
        elif rf_results['precision'] > dqn_results['precision']:
            report_lines.append(f"  • Random Forest has higher precision ({rf_results['precision']:.4f} vs {dqn_results['precision']:.4f}) - fewer false positives")
    
    report_lines.append("")
    report_lines.append("=" * 70)
    return "\n".join(report_lines)


def main():
    """Main evaluation function."""
    parser = argparse.ArgumentParser(
        description='Evaluate and compare DQN and Random Forest models',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python scripts/evaluate_models.py
  python scripts/evaluate_models.py --no-synthetic
  python scripts/evaluate_models.py --save-report
  python scripts/evaluate_models.py --test-size 0.3
        """
    )
    
    parser.add_argument('--test-size', type=float, default=0.2, help='Proportion of data for test set (default: 0.2)')
    parser.add_argument('--use-synthetic', action='store_true', default=True, help='Use synthetic data (default: True)')
    parser.add_argument('--no-synthetic', dest='use_synthetic', action='store_false', help='Use sample data instead')
    parser.add_argument('--save-report', action='store_true', help='Save report to file')
    parser.add_argument('--output-dir', type=str, default=None, help=f'Output directory for reports (default: {MODELS_DIR})')
    
    args = parser.parse_args()
    
    if not (0 < args.test_size < 1):
        print("Error: test-size must be between 0 and 1")
        sys.exit(1)
    
    output_dir = Path(args.output_dir) if args.output_dir else MODELS_DIR
    output_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    try:
        train_df, test_df = load_and_split_data(use_synthetic=args.use_synthetic, test_size=args.test_size, random_state=42)
        X_test, y_test = prepare_features(test_df)
        rf_model, dqn_agent, normalizer = load_models()
        
        if rf_model is None and dqn_agent is None:
            print("\nError: No models available for evaluation.")
            print("Please train at least one model first.")
            sys.exit(1)
        
        if dqn_agent is not None and normalizer is None:
            print("\nError: DQN model loaded but normalizer is missing.")
            print("Please run: python scripts/save_norm_params.py")
            sys.exit(1)
        
        rf_results = None
        dqn_results = None
        
        if rf_model is not None:
            try:
                rf_results = evaluate_rf_model(rf_model, X_test, y_test)
            except Exception as e:
                print(f"\nError evaluating Random Forest model: {e}")
                import traceback
                traceback.print_exc()
        
        if dqn_agent is not None and normalizer is not None:
            try:
                dqn_results = evaluate_dqn_model(dqn_agent, normalizer, X_test, y_test)
            except Exception as e:
                print(f"\nError evaluating DQN model: {e}")
                import traceback
                traceback.print_exc()
        
        comparison = compare_models(rf_results, dqn_results)
        report = generate_report(rf_results, dqn_results, comparison, test_df, timestamp)
        print("\n" + report)
        
        if args.save_report:
            report_path = output_dir / "evaluation_report.txt"
            with open(report_path, 'w') as f:
                f.write(report)
            print(f"\nReport saved to: {report_path}")
        
    except FileNotFoundError as e:
        print(f"\nError: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\nUnexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
