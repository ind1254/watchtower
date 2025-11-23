"""Utility functions and classes for model normalization and prediction."""

import numpy as np
import pandas as pd
import json
from pathlib import Path
from typing import Optional, Dict, Tuple
import sys

sys.path.append(str(Path(__file__).parent.parent))
from config import SAMPLES_DIR, SYNTHETIC_DIR, NORM_PARAMS_PATH


class Normalizer:
    """Handles feature normalization for DQN model predictions."""
    
    def __init__(self, mean: Optional[np.ndarray] = None, std: Optional[np.ndarray] = None):
        """
        Initialize the normalizer.
        
        Args:
            mean: Mean values for normalization (30 features)
            std: Standard deviation values for normalization (30 features)
        """
        self.mean = mean
        self.std = std
        self.fitted = mean is not None and std is not None
    
    def fit(self, transactions_df: pd.DataFrame):
        """
        Compute mean and std from training data.
        
        Args:
            transactions_df: DataFrame with transaction features (Time, V1-V28, Amount) and Class
        """
        feature_cols = ['Time'] + [f'V{i}' for i in range(1, 29)] + ['Amount']
        features = transactions_df[feature_cols].values
        
        self.mean = features.mean(axis=0)
        self.std = features.std(axis=0) + 1e-8  # Add small epsilon to avoid division by zero
        self.fitted = True
    
    def transform(self, features: np.ndarray) -> np.ndarray:
        """
        Normalize features using saved parameters.
        
        Args:
            features: Feature array (can be 1D or 2D)
            
        Returns:
            Normalized features
            
        Raises:
            ValueError: If normalizer is not fitted
        """
        if not self.fitted:
            raise ValueError("Normalizer is not fitted. Call fit() or load() first.")
        
        features = np.asarray(features)
        was_1d = features.ndim == 1
        
        if was_1d:
            features = features.reshape(1, -1)
        
        normalized = (features - self.mean) / self.std
        
        if was_1d:
            normalized = normalized.flatten()
        
        return normalized.astype(np.float32)
    
    def save(self, filepath: Path):
        """
        Save normalization parameters to JSON file.
        
        Args:
            filepath: Path to save the parameters
        """
        if not self.fitted:
            raise ValueError("Normalizer is not fitted. Cannot save.")
        
        params = {
            'mean': self.mean.tolist(),
            'std': self.std.tolist()
        }
        
        filepath.parent.mkdir(parents=True, exist_ok=True)
        with open(filepath, 'w') as f:
            json.dump(params, f, indent=2)
        
        print(f"Normalization parameters saved to {filepath}")
    
    def load(self, filepath: Path):
        """
        Load normalization parameters from JSON file.
        
        Args:
            filepath: Path to load the parameters from
            
        Raises:
            FileNotFoundError: If file doesn't exist
        """
        if not filepath.exists():
            raise FileNotFoundError(f"Normalization parameters not found at {filepath}")
        
        with open(filepath, 'r') as f:
            params = json.load(f)
        
        self.mean = np.array(params['mean'])
        self.std = np.array(params['std'])
        self.fitted = True
        
        print(f"Normalization parameters loaded from {filepath}")


def get_normalization_params(use_synthetic: bool = True) -> Tuple[np.ndarray, np.ndarray]:
    """
    Load training data and compute normalization parameters.
    
    Args:
        use_synthetic: If True, use synthetic data; otherwise use samples
        
    Returns:
        Tuple of (mean, std) arrays
        
    Raises:
        FileNotFoundError: If training data not found
    """
    from scripts.train_model import load_training_data
    
    df = load_training_data(use_synthetic=use_synthetic)
    
    feature_cols = ['Time'] + [f'V{i}' for i in range(1, 29)] + ['Amount']
    features = df[feature_cols].values
    
    mean = features.mean(axis=0)
    std = features.std(axis=0) + 1e-8
    
    return mean, std


def load_normalizer(filepath: Optional[Path] = None, use_synthetic: bool = True) -> Normalizer:
    """
    Load normalizer from saved file, or compute from training data if not available.
    
    Args:
        filepath: Path to normalization parameters file (default: NORM_PARAMS_PATH)
        use_synthetic: Whether to use synthetic data if computing params
        
    Returns:
        Normalizer instance
    """
    if filepath is None:
        filepath = NORM_PARAMS_PATH
    
    normalizer = Normalizer()
    
    # Try to load from file first
    if filepath.exists():
        try:
            normalizer.load(filepath)
            return normalizer
        except Exception as e:
            print(f"Warning: Could not load normalization params from {filepath}: {e}")
            print("Computing from training data...")
    
    # If file doesn't exist or failed to load, compute from training data
    try:
        mean, std = get_normalization_params(use_synthetic=use_synthetic)
        normalizer = Normalizer(mean=mean, std=std)
        # Try to save for future use
        try:
            normalizer.save(filepath)
        except Exception as e:
            print(f"Warning: Could not save normalization params: {e}")
        return normalizer
    except Exception as e:
        raise ValueError(f"Could not compute normalization parameters: {e}")

