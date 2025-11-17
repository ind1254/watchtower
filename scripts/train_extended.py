"""Extended training script for RL fraud detection model.
Runs multiple training iterations with checkpointing and progress tracking."""

import pandas as pd
import numpy as np
import json
import argparse
from pathlib import Path
from datetime import datetime
import sys
from typing import Dict, List, Optional
import time

sys.path.append(str(Path(__file__).parent.parent))
from config import SAMPLES_DIR, MODELS_DIR, SYNTHETIC_DIR

try:
    from scripts.rl_environment import FraudDetectionEnv
    from scripts.rl_agent import DQNAgent
    from scripts.train_model import load_training_data
    RL_AVAILABLE = True
except ImportError as e:
    RL_AVAILABLE = False
    print(f"Error: RL components not available: {e}")
    sys.exit(1)


class TrainingTracker:
    """Track training progress and metrics across multiple runs."""
    
    def __init__(self, log_dir: Path):
        self.log_dir = log_dir
        self.log_dir.mkdir(parents=True, exist_ok=True)
        self.history_file = log_dir / "training_history.json"
        self.history = self.load_history()
    
    def load_history(self) -> List[Dict]:
        """Load training history from file."""
        if self.history_file.exists():
            with open(self.history_file, 'r') as f:
                return json.load(f)
        return []
    
    def save_history(self):
        """Save training history to file."""
        with open(self.history_file, 'w') as f:
            json.dump(self.history, f, indent=2)
    
    def add_run(self, run_data: Dict):
        """Add a training run to history."""
        run_data['timestamp'] = datetime.now().isoformat()
        self.history.append(run_data)
        self.save_history()
    
    def get_best_run(self, metric: str = 'f1_score') -> Optional[Dict]:
        """Get the best training run based on a metric."""
        if not self.history:
            return None
        
        valid_runs = [r for r in self.history if 'test_metrics' in r and metric in r['test_metrics']]
        if not valid_runs:
            return None
        
        return max(valid_runs, key=lambda x: x['test_metrics'][metric])


def train_with_checkpointing(
    df: pd.DataFrame,
    episodes_per_iteration: int = 100,
    total_iterations: int = 10,
    checkpoint_freq: int = 5,
    resume_from: Optional[str] = None,
    use_synthetic: bool = True
) -> DQNAgent:
    """
    Train the model over multiple iterations with checkpointing.
    
    Args:
        df: Training data
        episodes_per_iteration: Episodes per training iteration
        total_iterations: Total number of training iterations
        checkpoint_freq: Save checkpoint every N iterations
        resume_from: Path to checkpoint to resume from
        use_synthetic: Whether using synthetic data
    
    Returns:
        Trained agent
    """
    print("\n" + "=" * 70)
    print("EXTENDED RL TRAINING - Multiple Iterations")
    print("=" * 70)
    print(f"Total Iterations: {total_iterations}")
    print(f"Episodes per Iteration: {episodes_per_iteration}")
    print(f"Total Episodes: {total_iterations * episodes_per_iteration}")
    print("=" * 70)
    
    # Setup tracking
    tracker = TrainingTracker(MODELS_DIR / "training_logs")
    
    # Split data
    from sklearn.model_selection import train_test_split
    train_df, test_df = train_test_split(
        df, test_size=0.2, random_state=42, stratify=df['Class']
    )
    
    # Create environment
    env = FraudDetectionEnv(train_df)
    
    # Create or load agent
    state_dim = 30
    action_dim = 2
    
    if resume_from and Path(resume_from).exists():
        print(f"\nResuming from checkpoint: {resume_from}")
        agent = DQNAgent(state_dim=state_dim, action_dim=action_dim)
        agent.load(resume_from)
        start_iteration = len(tracker.history) + 1
    else:
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
        start_iteration = 1
    
    best_f1 = -1
    best_model_path = MODELS_DIR / "dqn_model_best.pth"
    
    # Training iterations
    for iteration in range(start_iteration, total_iterations + 1):
        print(f"\n{'='*70}")
        print(f"ITERATION {iteration}/{total_iterations}")
        print(f"{'='*70}")
        
        iteration_start_time = time.time()
        episode_rewards = []
        episode_metrics = []
        
        # Train for this iteration
        for episode in range(episodes_per_iteration):
            state, info = env.reset()
            total_reward = 0
            done = False
            
            while not done:
                action = agent.act(state, training=True)
                next_state, reward, terminated, truncated, step_info = env.step(action)
                done = terminated or truncated
                
                agent.remember(state, action, reward, next_state, done)
                agent.replay()
                
                state = next_state
                total_reward += reward
            
            metrics = env.get_metrics()
            episode_rewards.append(total_reward)
            episode_metrics.append(metrics)
            
            # Print progress every 10 episodes
            if (episode + 1) % 10 == 0 or episode == 0:
                print(f"  Episode {episode + 1}/{episodes_per_iteration} | "
                      f"Reward: {total_reward:.2f} | "
                      f"Acc: {metrics.get('accuracy', 0):.4f} | "
                      f"F1: {metrics.get('f1_score', 0):.4f} | "
                      f"Epsilon: {agent.epsilon:.4f}")
        
        # Evaluate on test set
        print(f"\nEvaluating on test set...")
        test_env = FraudDetectionEnv(test_df)
        state, info = test_env.reset()
        done = False
        agent.epsilon = 0.0  # Disable exploration
        
        while not done:
            action = agent.act(state, training=False)
            next_state, reward, terminated, truncated, step_info = test_env.step(action)
            done = terminated or truncated
            state = next_state
        
        test_metrics = test_env.get_metrics()
        agent.epsilon = max(agent.epsilon_min, agent.epsilon * (0.995 ** episodes_per_iteration))
        
        iteration_time = time.time() - iteration_start_time
        
        # Print iteration summary
        print(f"\nIteration {iteration} Summary:")
        print(f"  Test Accuracy: {test_metrics.get('accuracy', 0):.4f}")
        print(f"  Test Precision: {test_metrics.get('precision', 0):.4f}")
        print(f"  Test Recall: {test_metrics.get('recall', 0):.4f}")
        print(f"  Test F1 Score: {test_metrics.get('f1_score', 0):.4f}")
        print(f"  Avg Episode Reward: {np.mean(episode_rewards):.2f}")
        print(f"  Time: {iteration_time:.2f}s")
        
        # Save best model
        current_f1 = test_metrics.get('f1_score', 0)
        if current_f1 > best_f1:
            best_f1 = current_f1
            agent.save(str(best_model_path))
            print(f"  ✓ New best model saved! (F1: {best_f1:.4f})")
        
        # Save checkpoint
        if iteration % checkpoint_freq == 0:
            checkpoint_path = MODELS_DIR / f"dqn_model_checkpoint_iter{iteration}.pth"
            agent.save(str(checkpoint_path))
            print(f"  ✓ Checkpoint saved: {checkpoint_path}")
        
        # Track this iteration
        tracker.add_run({
            'iteration': iteration,
            'episodes_per_iteration': episodes_per_iteration,
            'avg_reward': float(np.mean(episode_rewards)),
            'test_metrics': {k: float(v) for k, v in test_metrics.items()},
            'training_time': iteration_time,
            'epsilon': float(agent.epsilon),
            'total_steps': agent.steps
        })
    
    # Final evaluation
    print(f"\n{'='*70}")
    print("FINAL EVALUATION")
    print(f"{'='*70}")
    
    test_env = FraudDetectionEnv(test_df)
    state, info = test_env.reset()
    done = False
    agent.epsilon = 0.0
    
    while not done:
        action = agent.act(state, training=False)
        next_state, reward, terminated, truncated, step_info = test_env.step(action)
        done = terminated or truncated
        state = next_state
    
    final_metrics = test_env.get_metrics()
    
    print(f"\nFinal Test Performance:")
    print(f"  Accuracy: {final_metrics.get('accuracy', 0):.4f}")
    print(f"  Precision: {final_metrics.get('precision', 0):.4f}")
    print(f"  Recall: {final_metrics.get('recall', 0):.4f}")
    print(f"  F1 Score: {final_metrics.get('f1_score', 0):.4f}")
    print(f"\n  True Positives: {final_metrics.get('true_positives', 0)}")
    print(f"  True Negatives: {final_metrics.get('true_negatives', 0)}")
    print(f"  False Positives: {final_metrics.get('false_positives', 0)}")
    print(f"  False Negatives: {final_metrics.get('false_negatives', 0)}")
    
    # Save final model
    final_model_path = MODELS_DIR / "dqn_model_final.pth"
    agent.save(str(final_model_path))
    print(f"\nFinal model saved to: {final_model_path}")
    print(f"Best model (F1={best_f1:.4f}) saved to: {best_model_path}")
    
    # Print training summary
    best_run = tracker.get_best_run('f1_score')
    if best_run:
        print(f"\nBest iteration: {best_run['iteration']} (F1: {best_run['test_metrics']['f1_score']:.4f})")
    
    return agent


def main():
    """Main function for extended training."""
    parser = argparse.ArgumentParser(
        description='Extended RL training with multiple iterations',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Train for 20 iterations, 100 episodes each
  python scripts/train_extended.py --iterations 20 --episodes 100
  
  # Train with more episodes per iteration
  python scripts/train_extended.py --iterations 10 --episodes 200
  
  # Resume from checkpoint
  python scripts/train_extended.py --resume models/dqn_model_checkpoint_iter5.pth
        """
    )
    
    parser.add_argument('--iterations', type=int, default=20,
                       help='Number of training iterations (default: 20)')
    parser.add_argument('--episodes', type=int, default=100,
                       help='Episodes per iteration (default: 100)')
    parser.add_argument('--checkpoint-freq', type=int, default=5,
                       help='Save checkpoint every N iterations (default: 5)')
    parser.add_argument('--resume', type=str, default=None,
                       help='Resume from checkpoint file')
    parser.add_argument('--use-synthetic', action='store_true', default=True,
                       help='Use synthetic data (default: True)')
    parser.add_argument('--no-synthetic', dest='use_synthetic', action='store_false',
                       help='Use sample data instead')
    
    args = parser.parse_args()
    
    if not RL_AVAILABLE:
        print("Error: RL components not available. Please install dependencies:")
        print("  pip install gymnasium torch")
        sys.exit(1)
    
    try:
        # Load data
        print("Loading training data...")
        df = load_training_data(use_synthetic=args.use_synthetic)
        print(f"Loaded {len(df)} transactions")
        print(f"Fraud rate: {df['Class'].mean() * 100:.2f}%")
        
        # Train
        agent = train_with_checkpointing(
            df=df,
            episodes_per_iteration=args.episodes,
            total_iterations=args.iterations,
            checkpoint_freq=args.checkpoint_freq,
            resume_from=args.resume,
            use_synthetic=args.use_synthetic
        )
        
        print("\n" + "=" * 70)
        print("EXTENDED TRAINING COMPLETE!")
        print("=" * 70)
        print(f"Total training iterations: {args.iterations}")
        print(f"Total episodes: {args.iterations * args.episodes}")
        print(f"Models saved in: {MODELS_DIR}")
        print(f"Training logs: {MODELS_DIR / 'training_logs'}")
        
    except KeyboardInterrupt:
        print("\n\nTraining interrupted by user. Checkpoints saved.")
        sys.exit(0)
    except Exception as e:
        print(f"\nError during training: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()

