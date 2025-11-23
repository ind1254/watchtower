"""Script to compute and save normalization parameters from training data."""

import sys
from pathlib import Path
import argparse

sys.path.append(str(Path(__file__).parent.parent))
from config import NORM_PARAMS_PATH
from scripts.model_utils import Normalizer
from scripts.train_model import load_training_data


def main():
    """Main function to save normalization parameters."""
    parser = argparse.ArgumentParser(
        description='Compute and save normalization parameters from training data'
    )
    parser.add_argument('--use-synthetic', action='store_true', default=True,
                       help='Use synthetic data (default: True)')
    parser.add_argument('--no-synthetic', dest='use_synthetic', action='store_false',
                       help='Use sample data instead')
    parser.add_argument('--output', type=str, default=None,
                       help=f'Output path for normalization params (default: {NORM_PARAMS_PATH})')
    
    args = parser.parse_args()
    
    output_path = Path(args.output) if args.output else NORM_PARAMS_PATH
    
    print("=" * 60)
    print("Computing Normalization Parameters")
    print("=" * 60)
    
    try:
        # Load training data
        print(f"\nLoading training data...")
        df = load_training_data(use_synthetic=args.use_synthetic)
        print(f"Loaded {len(df)} transactions")
        
        # Create normalizer and fit
        print("\nComputing normalization parameters...")
        normalizer = Normalizer()
        normalizer.fit(df)
        
        print(f"\nMean shape: {normalizer.mean.shape}")
        print(f"Std shape: {normalizer.std.shape}")
        print(f"\nMean range: [{normalizer.mean.min():.4f}, {normalizer.mean.max():.4f}]")
        print(f"Std range: [{normalizer.std.min():.4f}, {normalizer.std.max():.4f}]")
        
        # Save parameters
        print(f"\nSaving to {output_path}...")
        normalizer.save(output_path)
        
        print("\n" + "=" * 60)
        print("Normalization parameters saved successfully!")
        print("=" * 60)
        
    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()

