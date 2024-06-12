from copy import deepcopy
import numpy as np
import random
from .logic import move, fill_two_or_four, check_game_status


INF = 2**64
PERFECT_BOARD = [[2, 2**2, 2**3, 2**4],
                [2**8, 2**7, 2**6, 2**5],
                [2**9, 2**10, 2**11, 2**12],
                [2**16, 2**15, 2**14, 2**13]]

def improved_snake_heuristic(board):
    weights = [[65536, 32768, 16384, 8192],
               [256, 512, 1024, 2048],
               [128, 64, 32, 16],
               [2, 4, 8, 1]]
    return sum(board[i][j] * weights[i][j] for i in range(4) for j in range(4))

def monotonicity_heuristic(board):
    scores = [0, 0, 0, 0]
    for row in board:
        for i in range(3):
            if row[i] > row[i + 1]:
                scores[0] += row[i] - row[i + 1]
            else:
                scores[1] += row[i + 1] - row[i]

    for col in range(4):
        for i in range(3):
            if board[i][col] > board[i + 1][col]:
                scores[2] += board[i][col] - board[i + 1][col]
            else:
                scores[3] += board[i + 1][col] - board[i][col]
    return min(scores[0], scores[1]) + min(scores[2], scores[3])
def smoothness_heuristic(board):
    smoothness = 0
    for i in range(4):
        for j in range(3):
            smoothness -= abs(board[i][j] - board[i][j + 1])
            smoothness -= abs(board[j][i] - board[j + 1][i])
    return smoothness

def empty_tiles_heuristic(board):
    return sum(row.count(0) for row in board)

def merge_potential_heuristic(board):
    merge_score = 0
    for i in range(4):
        for j in range(4):
            if j < 3 and board[i][j] == board[i][j + 1]:
                merge_score += board[i][j]
            if i < 3 and board[i][j] == board[i + 1][j]:
                merge_score += board[i][j]
    return merge_score
class ExpectimaxAgent:
    def __init__(self, depth=2):
        self.depth = depth
        self.actions = ["w", "a", "s", "d"]

    def getNextBestMoveExpectiminimax(self, board):
        bestScore = -INF
        bestNextMove = None
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

        if is_maximizing:
            max_value = -np.inf
            for action in self.actions:
                new_board = move(action, deepcopy(board))
                if new_board != board:
                    value = self.expectimax(new_board, depth - 0.5, False)
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
                    value += prob * self.expectimax(new_board, depth - 0.5, True)
            return value

    def evaluate_board(self, board):
     
        max_tile = max(max(row) for row in board)
        
        # Dynamic weight adjustment based on the highest tile value
        if max_tile >= 1024:
            snake_weight = 0.125
            monotonicity_weight = 0.125
            smoothness_weight = 0.125
            empty_tiles_weight = 0.25
            merge_potential_weight = 0.01
        elif max_tile >= 512:
            snake_weight = 0.4
            monotonicity_weight = 0.25
            smoothness_weight = 0.4
            empty_tiles_weight = 0.1
            merge_potential_weight = 0
        else:
            snake_weight = 0.5
            monotonicity_weight = 0.25
            smoothness_weight = 0.5
            empty_tiles_weight = 0
            merge_potential_weight = 0
        
        return (snake_weight * improved_snake_heuristic(board) +
                monotonicity_weight * monotonicity_heuristic(board) +
                smoothness_weight * smoothness_heuristic(board) +
                empty_tiles_weight * empty_tiles_heuristic(board) +
                merge_potential_weight * merge_potential_heuristic(board))