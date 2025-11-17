"""Deep Q-Network (DQN) Agent for Fraud Detection."""

import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from collections import deque
import random
from typing import Tuple, Optional
import os


class DQN(nn.Module):
    """Deep Q-Network for fraud detection."""
    
    def __init__(self, state_dim: int, action_dim: int, hidden_dims: list = [128, 64, 32]):
        """
        Initialize the DQN.
        
        Args:
            state_dim: Dimension of state space (30 features)
            action_dim: Dimension of action space (2: flag or not)
            hidden_dims: List of hidden layer dimensions
        """
        super(DQN, self).__init__()
        
        layers = []
        input_dim = state_dim
        
        for hidden_dim in hidden_dims:
            layers.append(nn.Linear(input_dim, hidden_dim))
            layers.append(nn.ReLU())
            layers.append(nn.Dropout(0.2))
            input_dim = hidden_dim
        
        layers.append(nn.Linear(input_dim, action_dim))
        
        self.network = nn.Sequential(*layers)
    
    def forward(self, state: torch.Tensor) -> torch.Tensor:
        """Forward pass through the network."""
        return self.network(state)


class DQNAgent:
    """DQN Agent for fraud detection using experience replay."""
    
    def __init__(
        self,
        state_dim: int,
        action_dim: int,
        lr: float = 0.001,
        gamma: float = 0.99,
        epsilon: float = 1.0,
        epsilon_min: float = 0.01,
        epsilon_decay: float = 0.995,
        memory_size: int = 10000,
        batch_size: int = 64,
        target_update_freq: int = 100,
        device: Optional[str] = None
    ):
        """
        Initialize the DQN agent.
        
        Args:
            state_dim: Dimension of state space
            action_dim: Dimension of action space
            lr: Learning rate
            gamma: Discount factor
            epsilon: Initial exploration rate
            epsilon_min: Minimum exploration rate
            epsilon_decay: Epsilon decay rate
            memory_size: Size of replay buffer
            batch_size: Batch size for training
            target_update_freq: Frequency to update target network
            device: Device to use ('cuda' or 'cpu')
        """
        self.state_dim = state_dim
        self.action_dim = action_dim
        self.lr = lr
        self.gamma = gamma
        self.epsilon = epsilon
        self.epsilon_min = epsilon_min
        self.epsilon_decay = epsilon_decay
        self.batch_size = batch_size
        self.target_update_freq = target_update_freq
        
        # Set device
        self.device = device or ('cuda' if torch.cuda.is_available() else 'cpu')
        print(f"Using device: {self.device}")
        
        # Networks
        self.q_network = DQN(state_dim, action_dim).to(self.device)
        self.target_network = DQN(state_dim, action_dim).to(self.device)
        self.target_network.load_state_dict(self.q_network.state_dict())
        self.target_network.eval()
        
        # Optimizer
        self.optimizer = optim.Adam(self.q_network.parameters(), lr=lr)
        
        # Replay buffer
        self.memory = deque(maxlen=memory_size)
        
        # Training statistics
        self.steps = 0
        self.losses = []
    
    def remember(self, state: np.ndarray, action: int, reward: float, 
                 next_state: np.ndarray, done: bool):
        """Store experience in replay buffer."""
        self.memory.append((state, action, reward, next_state, done))
    
    def act(self, state: np.ndarray, training: bool = True) -> int:
        """
        Choose action using epsilon-greedy policy.
        
        Args:
            state: Current state
            training: Whether in training mode (uses epsilon-greedy)
            
        Returns:
            Action to take
        """
        if training and random.random() <= self.epsilon:
            return random.randrange(self.action_dim)
        
        state_tensor = torch.FloatTensor(state).unsqueeze(0).to(self.device)
        q_values = self.q_network(state_tensor)
        return q_values.argmax().item()
    
    def replay(self) -> Optional[float]:
        """
        Train the agent on a batch of experiences.
        
        Returns:
            Loss value if training occurred, None otherwise
        """
        if len(self.memory) < self.batch_size:
            return None
        
        # Sample batch
        batch = random.sample(self.memory, self.batch_size)
        states, actions, rewards, next_states, dones = zip(*batch)
        
        states = torch.FloatTensor(np.array(states)).to(self.device)
        actions = torch.LongTensor(actions).to(self.device)
        rewards = torch.FloatTensor(rewards).to(self.device)
        next_states = torch.FloatTensor(np.array(next_states)).to(self.device)
        dones = torch.BoolTensor(dones).to(self.device)
        
        # Current Q values
        q_values = self.q_network(states)
        q_value = q_values.gather(1, actions.unsqueeze(1)).squeeze(1)
        
        # Next Q values from target network
        with torch.no_grad():
            next_q_values = self.target_network(next_states)
            next_q_value = next_q_values.max(1)[0]
            target_q_value = rewards + (self.gamma * next_q_value * ~dones)
        
        # Compute loss
        loss = nn.MSELoss()(q_value, target_q_value)
        
        # Optimize
        self.optimizer.zero_grad()
        loss.backward()
        # Gradient clipping for stability
        torch.nn.utils.clip_grad_norm_(self.q_network.parameters(), 1.0)
        self.optimizer.step()
        
        # Update target network periodically
        self.steps += 1
        if self.steps % self.target_update_freq == 0:
            self.target_network.load_state_dict(self.q_network.state_dict())
        
        # Decay epsilon
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay
        
        loss_value = loss.item()
        self.losses.append(loss_value)
        
        return loss_value
    
    def save(self, filepath: str):
        """Save the agent's Q-network."""
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        torch.save({
            'q_network_state_dict': self.q_network.state_dict(),
            'target_network_state_dict': self.target_network.state_dict(),
            'optimizer_state_dict': self.optimizer.state_dict(),
            'epsilon': self.epsilon,
            'steps': self.steps
        }, filepath)
        print(f"Model saved to {filepath}")
    
    def load(self, filepath: str):
        """Load the agent's Q-network."""
        checkpoint = torch.load(filepath, map_location=self.device)
        self.q_network.load_state_dict(checkpoint['q_network_state_dict'])
        self.target_network.load_state_dict(checkpoint['target_network_state_dict'])
        self.optimizer.load_state_dict(checkpoint['optimizer_state_dict'])
        self.epsilon = checkpoint.get('epsilon', self.epsilon_min)
        self.steps = checkpoint.get('steps', 0)
        print(f"Model loaded from {filepath}")

