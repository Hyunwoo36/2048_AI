import random

class AI2048:
    def __init__(self, mode=None):
        self.mode = mode
        if mode is None:
            self.mode = 'random'  # Default to random if no mode is provided
        self.algorithm = {
            'astar': self.astar_algorithm,
            'expectimax': self.expectimax_algorithm,
            'random': self.random_moves
        }.get(self.mode, self.random_moves)
        print(f"AI mode initialized: {self.mode}")  # Debug: Check which mode is initialized

    def get_move(self, board):
        print(f"Using {self.mode} algorithm")  # Debug: Check which algorithm is used
        return self.algorithm(board)

    def astar_algorithm(self, board):
        print("A* move!!")
        return 'w'  # Example move

    def expectimax_algorithm(self, board):
        print("Expectimax move!!")
        return 's'  # Example move

    def random_moves(self, board):
        print("Random move!!")
        return random.choice(['w', 'a', 's', 'd'])  # Example move
