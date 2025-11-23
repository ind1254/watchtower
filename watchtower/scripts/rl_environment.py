"""Reinforcement Learning Environment for Fraud Detection."""

import numpy as np
import gymnasium as gym
from gymnasium import spaces
from typing import Tuple, Optional
import pandas as pd


class FraudDetectionEnv(gym.Env):
    """
    Custom Gymnasium environment for fraud detection.
    
    The agent processes transactions sequentially and decides whether to flag them as fraud.
    Rewards are based on correct predictions with emphasis on catching fraud.
    """
    
    metadata = {"render_modes": ["human"], "render_fps": 4}
    
    def __init__(self, transactions: pd.DataFrame, reward_config: Optional[dict] = None):
        """
        Initialize the fraud detection environment.
        
        Args:
            transactions: DataFrame with transaction features and 'Class' column (0=normal, 1=fraud)
            reward_config: Dictionary with reward weights (default: balanced rewards)
        """
        super().__init__()
        
        self.transactions = transactions.reset_index(drop=True)
        self.current_idx = 0
        self.total_transactions = len(transactions)
        
        # Extract features and labels
        feature_cols = ['Time'] + [f'V{i}' for i in range(1, 29)] + ['Amount']
        self.features = self.transactions[feature_cols].values
        self.labels = self.transactions['Class'].values
        
        # Normalize features for better training
        self.feature_mean = self.features.mean(axis=0)
        self.feature_std = self.features.std(axis=0) + 1e-8
        self.features_normalized = (self.features - self.feature_mean) / self.feature_std
        
        # Reward configuration - optimized for fraud detection
        # Calculate adaptive rewards based on class imbalance
        fraud_rate = transactions['Class'].mean() if 'Class' in transactions.columns else 0.1
        class_imbalance = (1 - fraud_rate) / max(fraud_rate, 0.01)  # Ratio of normal to fraud
        
        self.reward_config = reward_config or {
            'true_positive': 50.0,      # Heavily reward catching fraud
            'true_negative': 0.5,       # Small reward for correct normal (common case)
            'false_positive': -1.0,     # Small penalty for false alarms
            'false_negative': -100.0    # Heavy penalty for missing fraud
        }
        
        # Scale rewards based on imbalance if not custom config
        if reward_config is None:
            # Adjust rewards to account for class imbalance
            # More imbalance = higher rewards for fraud detection
            imbalance_factor = min(class_imbalance / 10, 2.0)  # Cap at 2x
            self.reward_config['true_positive'] *= (1 + imbalance_factor * 0.5)
            self.reward_config['false_negative'] *= (1 + imbalance_factor)
        
        # Statistics tracking
        self.stats = {
            'true_positives': 0,
            'true_negatives': 0,
            'false_positives': 0,
            'false_negatives': 0,
            'total_reward': 0.0
        }
        
        # Action space: 0 = don't flag, 1 = flag as fraud
        self.action_space = spaces.Discrete(2)
        
        # Observation space: normalized transaction features (30 features)
        self.observation_space = spaces.Box(
            low=-np.inf,
            high=np.inf,
            shape=(30,),
            dtype=np.float32
        )
    
    def reset(self, seed: Optional[int] = None, options: Optional[dict] = None) -> Tuple[np.ndarray, dict]:
        """Reset the environment to start a new episode."""
        super().reset(seed=seed)
        
        # Shuffle transactions for each episode
        indices = np.random.permutation(self.total_transactions)
        self.features_normalized = self.features_normalized[indices]
        self.labels = self.labels[indices]
        
        self.current_idx = 0
        self.stats = {
            'true_positives': 0,
            'true_negatives': 0,
            'false_positives': 0,
            'false_negatives': 0,
            'total_reward': 0.0
        }
        
        observation = self.features_normalized[0].astype(np.float32)
        info = {'transaction_idx': 0}
        
        return observation, info
    
    def step(self, action: int) -> Tuple[np.ndarray, float, bool, bool, dict]:
        """
        Execute one step in the environment.
        
        Args:
            action: 0 = don't flag, 1 = flag as fraud
            
        Returns:
            observation: Next transaction features
            reward: Reward for the action taken
            terminated: Whether episode is done
            truncated: Whether episode was truncated
            info: Additional information
        """
        if self.current_idx >= self.total_transactions:
            raise RuntimeError("Episode is done. Call reset() first.")
        
        # Get current transaction label
        is_fraud = self.labels[self.current_idx]
        
        # Calculate reward based on action and true label
        if action == 1 and is_fraud == 1:
            # True positive: correctly flagged fraud
            reward = self.reward_config['true_positive']
            self.stats['true_positives'] += 1
        elif action == 0 and is_fraud == 0:
            # True negative: correctly didn't flag normal
            reward = self.reward_config['true_negative']
            self.stats['true_negatives'] += 1
        elif action == 1 and is_fraud == 0:
            # False positive: incorrectly flagged normal
            reward = self.reward_config['false_positive']
            self.stats['false_positives'] += 1
        else:  # action == 0 and is_fraud == 1
            # False negative: missed fraud
            reward = self.reward_config['false_negative']
            self.stats['false_negatives'] += 1
        
        self.stats['total_reward'] += reward
        
        # Move to next transaction
        self.current_idx += 1
        terminated = self.current_idx >= self.total_transactions
        truncated = False
        
        # Get next observation
        if terminated:
            observation = np.zeros(30, dtype=np.float32)
        else:
            observation = self.features_normalized[self.current_idx].astype(np.float32)
        
        info = {
            'transaction_idx': self.current_idx,
            'is_fraud': bool(is_fraud),
            'action': action,
            'correct': (action == is_fraud),
            'stats': self.stats.copy()
        }
        
        return observation, reward, terminated, truncated, info
    
    def render(self, mode: str = "human"):
        """Render the environment (print current statistics)."""
        if mode == "human":
            print(f"\nTransaction {self.current_idx}/{self.total_transactions}")
            print(f"Stats: TP={self.stats['true_positives']}, "
                  f"TN={self.stats['true_negatives']}, "
                  f"FP={self.stats['false_positives']}, "
                  f"FN={self.stats['false_negatives']}")
            print(f"Total Reward: {self.stats['total_reward']:.2f}")
    
    def get_metrics(self) -> dict:
        """Get performance metrics."""
        total = sum([
            self.stats['true_positives'],
            self.stats['true_negatives'],
            self.stats['false_positives'],
            self.stats['false_negatives']
        ])
        
        if total == 0:
            return {}
        
        tp = self.stats['true_positives']
        tn = self.stats['true_negatives']
        fp = self.stats['false_positives']
        fn = self.stats['false_negatives']
        
        accuracy = (tp + tn) / total if total > 0 else 0.0
        precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
        recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0
        f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0.0
        
        return {
            'accuracy': accuracy,
            'precision': precision,
            'recall': recall,
            'f1_score': f1,
            'true_positives': tp,
            'true_negatives': tn,
            'false_positives': fp,
            'false_negatives': fn,
            'total_reward': self.stats['total_reward']
        }

