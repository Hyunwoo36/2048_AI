import random
import json
import os

class QLearningAgent:
    def __init__(self, alpha=0.1, gamma=0.9, epsilon=0.1, epsilon_decay=0.995, q_table_file="q_table.json"):
        self.q_table = {}
        self.actions = ["w", "a", "s", "d"]
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self.epsilon_decay = epsilon_decay
        self.q_table_file = q_table_file
        self.load_q_table()

    def get_state(self, board):
        return tuple(cell for row in board for cell in row)

    def choose_action(self, state):
        if random.uniform(0, 1) < self.epsilon:
            action = random.choice(self.actions)
            print(f'Random action {action}')
            return action
        else:
            action = self.get_best_action(state)
            print(f'Best action {action}')
            return action

    def get_best_action(self, state):
        state_actions = self.q_table.get(state, {})
        if state_actions:  # Check if the dictionary is not empty
            print("STATE ACTIONs in best action!!!", state_actions)
            return max(state_actions, key=state_actions.get)
        else:
            print("No known actions, choosing randomly.")
            return random.choice(self.actions)


    def update(self, state, action, reward, next_state):
        if state not in self.q_table:
            self.q_table[state] = {a: 0 for a in self.actions}

        state_actions = self.q_table.setdefault(next_state, {a: 0 for a in self.actions})
        best_next_action = self.get_best_action(next_state)

        target = reward + self.gamma * state_actions.get(best_next_action, 0)
        print("TARGET: ", target)
        print("PREVIOUS: ", self.q_table[state][action])
        self.q_table[state][action] += self.alpha * (target - self.q_table[state][action])

        # Decay epsilon
        self.epsilon *= self.epsilon_decay

    def save_q_table(self):
        string_q_table = {str(k): v for k, v in self.q_table.items()}
        with open(self.q_table_file, 'w') as file:
            json.dump(string_q_table, file, indent=4)
        print(f"Q-table saved to {self.q_table_file}")

    def load_q_table(self):
        if os.path.exists(self.q_table_file):
            try:
                with open(self.q_table_file, 'r') as file:
                    string_q_table = json.load(file)
                self.q_table = {eval(k): v for k, v in string_q_table.items()}
                print(f"Q-table loaded from {self.q_table_file}")
            except (json.JSONDecodeError, SyntaxError) as e:
                print(f"Error loading Q-table: {e}. Starting with an empty Q-table.")
                self.q_table = {}
