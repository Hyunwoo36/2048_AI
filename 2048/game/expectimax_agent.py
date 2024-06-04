from copy import deepcopy
import numpy as np
import random
from .logic import move, fill_two_or_four, check_game_status

INF = 2**64
PERFECT_BOARD = [[2, 2**2, 2**3, 2**4],
                [2**8, 2**7, 2**6, 2**5],
                [2**9, 2**10, 2**11, 2**12],
                [2**16, 2**15, 2**14, 2**13]]

class ExpectimaxAgent:
    def __init__(self, depth=3):
            self.depth = depth
            self.actions = ["w", "a", "s", "d"]


    def snakeHeuristic(board):
        h = 0
        for i in range(board.boardSize):
            for j in range(board.boardSize):
                h += board[i][j] * PERFECT_BOARD[i][j]

        return h

    def getNextBestMoveExpectiminimax(self, board):
        
        bestScore = -INF
        bestNextMove = None
        results = []
        for action in self.actions:
            simBoard = move(action, deepcopy(board))
            if simBoard != board:
                    value = self.expectimax(simBoard, self.depth, False)
                    if value > bestScore:
                        bestScore = value
                        bestNextMove = action
        
        return bestNextMove

    def expectimax(self, board, depth, is_maximizing):
        status = check_game_status(board)
        if status != "PLAY" or depth == 0:
            return self.evaluate_board(board)
        elif depth < 0:
            return snakeHeuristic(board),self.action

        if is_maximizing:
            max_value = -np.inf
            for action in self.actions:
                new_board = move(action, deepcopy(board))
                if new_board != board:
                    value = self.expectimax(new_board, depth - 1, False)
                    max_value = max(max_value, value)
            return max_value
        else:
            empty_tiles = [(i, j) for i in range(4) for j in range(4) if board[i][j] == 0]
            if not empty_tiles:
                return self.evaluate_board(board)

            value = 0
            for tile in empty_tiles:
                for new_tile in [2, 4]:
                    new_board = deepcopy(board)
                    new_board[tile[0]][tile[1]] = new_tile
                    prob = 0.9 if new_tile == 2 else 0.1
                    value += prob * self.expectimax(new_board, depth - 1, True)

            return value

    def evaluate_board(self, board):
            return sum(sum(row) for row in board)