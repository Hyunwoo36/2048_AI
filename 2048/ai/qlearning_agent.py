import random

class QLearningAgent:
    def __init__(self, alpha=0.1, gamma=0.9, epsilon=0.1):
        self.q_table = {}
        self.actions = ["w", "a", "s", "d"]
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon

    def get_state(self, board):
        return tuple(cell for row in board for cell in row)

    def choose_action(self, state):
        if random.uniform(0, 1) < self.epsilon:
            return random.choice(self.actions)
        else:
            return self.get_best_action(state)

    def get_best_action(self, state):
        state_actions = self.q_table.get(state, {})
        return max(state_actions, key=state_actions.get, default=random.choice(self.actions))

    def update(self, state, action, reward, next_state):
        if state not in self.q_table:
            self.q_table[state] = {}  # Initialize an empty dictionary for the new state

        state_actions = self.q_table.setdefault(next_state, {})
        best_next_action = max(state_actions, key=state_actions.get, default=None)

        target = reward + self.gamma * state_actions.get(best_next_action, 0)
        self.q_table[state][action] = self.q_table.get(state, {}).get(action, 0) + self.alpha * (target - self.q_table.get(state, {}).get(action, 0))

        # Decay epsilon
        # self.epsilon *= self.epsilon_decay