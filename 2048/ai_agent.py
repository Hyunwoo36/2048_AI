import random
import heapq
from copy import deepcopy
import numpy as np

class AI2048:
    def __init__(self, mode=None):
        self.mode = mode
        if mode is None or mode not in ['a*', 'expectimax', 'random']:
            self.mode = 'random'  # Default to random if no mode or invalid mode is provided
        self.algorithm = {
            'a*': self.astar_algorithm,
            'emax': self.expectimax_algorithm,
            'random': self.random_moves
        }[self.mode]

    def get_move(self, board):
        return self.algorithm(board)

    def astar_algorithm(self, board):
        return self.a_star_search(board)

    def expectimax_algorithm(self, board):
        print("Expectimax move!!")
        return 's'  # Example move

    def random_moves(self, board):
        print("Random move!!")
        return random.choice(['w', 'a', 's', 'd'])  # Example move

    def heuristic(self, board):
        """
        Heuristic to prioritize combining higher tiles. 
        """
        # Sum of all tiles
        total_sum = max(cell for row in board for cell in row)
        
        # Penalty for empty spaces
        empty_spaces = max(1 for row in board for cell in row if cell == 0)
        
        # Incentive for combining higher tiles (penalize the sum of inverses of tiles)
        
        return -total_sum - empty_spaces

    def possible_moves(self, board):
        moves = []
        for move in ['w', 'a', 's', 'd']:
            new_board = move_board(move, deepcopy(board))
            if new_board != board:
                moves.append((move, new_board))
        return moves

    def a_star_search(self, board):
        # Priority queue for A* search
        frontier = []
        heapq.heappush(frontier, (0, board, []))  # (priority, board, path)

        while frontier:
            _, current_board, path = heapq.heappop(frontier)
            
            # Check if the game is over
            if checkGameStatus(current_board, 2048) != 'PLAY':
                return path[0] if path else 'w'  # Return the first move in the path

            for move, new_board in self.possible_moves(current_board):
                new_path = path + [move]
                priority = len(new_path) + self.heuristic(new_board)
                heapq.heappush(frontier, (priority, new_board, new_path))

        return random.choice(['w', 'a', 's', 'd'])  # Default move if no path is found

def move_board(move, board):
    """
    Function to make a move on the board. This function should return the new board after making the move.
    """
    new_board = deepcopy(board)
    # Implement the logic for moving the board here
    return new_board

def checkGameStatus(board, difficulty):
    """
    Function to check the game status. This function should return 'PLAY' if the game continues,
    'WIN' if the game is won, or 'LOSE' if the game is lost.
    """
    # Implement the logic for checking the game status here
    return 'PLAY'



# Q LEARNING
class QLearningAgent:
    def __init__(self, actions, alpha=0.1, gamma=0.9, epsilon=0.1):
        self.q_table = {}  # State-action values
        self.actions = actions
        self.alpha = alpha  # Learning rate
        self.gamma = gamma  # Discount factor
        self.epsilon = epsilon  # Exploration rate

    def get_state(self, board):
        return str(board)

    def choose_action(self, state):
        if random.uniform(0, 1) < self.epsilon:
            return random.choice(self.actions)  # Explore
        else:
            return self.get_best_action(state)  # Exploit

    def get_best_action(self, state):
        state_actions = self.q_table.get(state, {})
        return max(state_actions, key=state_actions.get, default=random.choice(self.actions))

    def learn(self, state, action, reward, next_state):
        state_actions = self.q_table.setdefault(state, {})
        next_state_actions = self.q_table.setdefault(next_state, {})  # Initialize next_state in Q-table
        best_next_action = max(next_state_actions, key=next_state_actions.get, default=None)
        
        target = reward + self.gamma * (next_state_actions.get(best_next_action, 0))
        state_actions[action] = state_actions.get(action, 0) + self.alpha * (target - state_actions.get(action, 0))

    def update(self, state, action, reward, next_state):
        self.learn(state, action, reward, next_state)
        state_actions = self.q_table.setdefault(state, {})
        next_state_actions = self.q_table.setdefault(next_state, {})  # Ensure next_state is in Q-table
        best_next_action = max(next_state_actions, key=next_state_actions.get, default=random.choice(self.actions))
        self.q_table[state][action] = state_actions.get(action, 0) + self.alpha * (
            reward + self.gamma * next_state_actions.get(best_next_action, 0) - state_actions.get(action, 0)
        )
