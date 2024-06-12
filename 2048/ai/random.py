import random
class RandomAgent:
    def __init__(self):
        self.actions = ['w', 'a', 's', 'd']

    def get_state(self, board):
        # RandomAgent does not need to process board state in traditional ways
        return None

    def choose_action(self, state):
        # Return the index of the action instead of the action itself
        return random.randint(0, len(self.actions) - 1)

    def update(self, state, action, reward, next_state):
        # RandomAgent does not update its strategy based on gameplay
        pass
