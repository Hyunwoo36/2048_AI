# ai_agent.py
class AI2048:
    def __init__(self, mode=None):
        self.mode = mode
        if mode == 'astar':
            self.algorithm = self.astar_algorithm
        elif mode == 'expectimax':
            self.algorithm = self.expectimax_algorithm
        else:
            self.algorithm = self.random_moves

    def get_move(self, board):
        return self.algorithm(board)

    def astar_algorithm(self, board):
        # Implement A* logic here
        return 'w'  # Example move

    def expectimax_algorithm(self, board):
        # Implement Expectimax logic here
        return 's'  # Example move

    def random_moves(self, board):
        import random
        return random.choice(['w', 'a', 's', 'd'])  # Example move
