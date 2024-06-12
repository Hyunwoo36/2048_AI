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
    increasing_rows = 0
    decreasing_rows = 0
    increasing_cols = 0
    decreasing_cols = 0

    for row in board:
        increasing_rows += sum(row[i] <= row[i + 1] for i in range(3))
        decreasing_rows += sum(row[i] >= row[i + 1] for i in range(3))

    for col in range(4):
        column_values = [board[row][col] for row in range(4)]
        increasing_cols += sum(column_values[i] <= column_values[i + 1] for i in range(3))
        decreasing_cols += sum(column_values[i] >= column_values[i + 1] for i in range(3))

    return max(increasing_rows, decreasing_rows) + max(increasing_cols, decreasing_cols)
def smoothness_heuristic(board):
    smoothness = 0
    for i in range(4):
        for j in range(3):
            smoothness -= abs(board[i][j] - board[i][j + 1])
            smoothness -= abs(board[j][i] - board[j + 1][i])
            # Penalize differences with adjacent edges and corners more
            if i == 0 or i == 3 or j == 0 or j == 3:
                smoothness -= abs(board[i][j] - board[i - 1][j]) * 0.5
                smoothness -= abs(board[i][j] - board[i][j - 1]) * 0.5
                if i == 0 and j == 0:
                    smoothness -= abs(board[i][j] - board[i + 1][j]) * 0.5
                    smoothness -= abs(board[i][j] - board[i][j + 1]) * 0.5
                elif i == 0 and j == 3:
                    smoothness -= abs(board[i][j] - board[i + 1][j]) * 0.5
                    smoothness -= abs(board[i][j] - board[i][j - 1]) * 0.5
                elif i == 3 and j == 0:
                    smoothness -= abs(board[i][j] - board[i - 1][j]) * 0.5
                    smoothness -= abs(board[i][j] - board[i][j + 1]) * 0.5
                elif i == 3 and j == 3:
                    smoothness -= abs(board[i][j] - board[i - 1][j]) * 0.5
                    smoothness -= abs(board[i][j] - board[i][j - 1]) * 0.5
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
    def __init__(self, depth=4):
        self.depth = depth
        self.actions = ["w", "a", "s", "d"]

    def getNextBestMoveExpectiminimax(self, board):
        bestScore = -INF
        bestNextMove = None
        for action in self.actions:
            simBoard = move(action, deepcopy(board))
            if simBoard != board:
                value = self.expectimax(simBoard, self.depth, -INF, INF, False)
                if value > bestScore:
                    bestScore = value
                    bestNextMove = action
        return bestNextMove

    def expectimax(self, board, depth, alpha, beta, is_maximizing):
        status = check_game_status(board)
        if status != "PLAY" or depth == 0:
            return self.evaluate_board(board)

        if is_maximizing:
            max_value = -INF
            for action in self.actions:
                new_board = move(action, deepcopy(board))
                if new_board != board:
                    value = self.expectimax(new_board, depth - 1, alpha, beta, False)
                    max_value = max(max_value, value)
                    alpha = max(alpha, value)
                    if beta <= alpha:
                        break  # Beta cutoff
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
                    value += prob * self.expectimax(new_board, depth - 1, alpha, beta, True)
                    beta = min(beta, value)
                    if beta <= alpha:
                        break  # Alpha cutoff
            return value

    def evaluate_board(self, board):
        return (0.5 * improved_snake_heuristic(board) +
                0.25 * monotonicity_heuristic(board) +
                0.25 * smoothness_heuristic(board) +
                0.0 * empty_tiles_heuristic(board) +
                0.0 * merge_potential_heuristic(board))

    def evaluate_board(self, board):
     return (.25 * improved_snake_heuristic(board) +
            .25 * monotonicity_heuristic(board) +
            .5 * smoothness_heuristic(board) +
            .0 * empty_tiles_heuristic(board) +
            .0 * merge_potential_heuristic(board))