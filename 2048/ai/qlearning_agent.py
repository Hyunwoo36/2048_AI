import random

class QLearningAgent:
    def __init__(self, actions, alpha=0.1, gamma=0.9, epsilon=0.1):
        self.q_table = {}
        self.actions = actions
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon

    def get_state(self, board):
        return str(board)

    def choose_action(self, state):
        if random.uniform(0, 1) < self.epsilon:
            return random.choice(self.actions)
        else:
            return self.get_best_action(state)

    def get_best_action(self, state):
        state_actions = self.q_table.get(state, {})
        return max(state_actions, key=state_actions.get, default=random.choice(self.actions))

    def learn(self, state, action, reward, next_state):
        state_actions = self.q_table.setdefault(state, {})
        next_state_actions = self.q_table.setdefault(next_state, {})
        best_next_action = max(next_state_actions, key=next_state_actions.get, default=None)
        
        target = reward + self.gamma * next_state_actions.get(best_next_action, 0)
        state_actions[action] = state_actions.get(action, 0) + self.alpha * (target - state_actions.get(action, 0))

    def update(self, state, action, reward, next_state):
        self.learn(state, action, reward, next_state)
        state_actions = self.q_table.setdefault(state, {})
        next_state_actions = self.q_table.setdefault(next_state, {})
        best_next_action = max(next_state_actions, key=next_state_actions.get, default=random.choice(self.actions))
        self.q_table[state][action] = state_actions.get(action, 0) + self.alpha * (
            reward + self.gamma * next_state_actions.get(best_next_action, 0) - state_actions.get(action, 0)
        )
