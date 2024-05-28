import random
import heapq
from copy import deepcopy
import numpy as np
from .qlearning_agent import QLearningAgent
from game.logic import move, check_game_status, fill_two_or_four

class AI2048:
    def __init__(self, mode=None):
        self.mode = mode if mode in ['a*', 'expectimax', 'random'] else 'random'
        self.algorithm = {
            'a*': self.a_star_search,
            'expectimax': self.expectimax_algorithm,
            'random': self.random_moves
        }[self.mode]

    def get_move(self, board):
        move = self.algorithm(board)
        print(f"A* algorithm selected move: {move}")
        return move

    def expectimax_algorithm(self, board):
        # Implement expectimax here
        return 's'  # Example move

    def random_moves(self, board):
        return random.choice(['w', 'a', 's', 'd'])

    def heuristic(self, board):
        max_tile = max(cell for row in board for cell in row)
        empty_spaces = sum(1 for row in board for cell in row if cell == 0)
        clustering_penalty = 0

        for i in range(4):
            for j in range(4):
                if board[i][j] != 0:
                    for di, dj in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                        ni, nj = i + di, j + dj
                        if 0 <= ni < 4 and 0 <= nj < 4 and board[ni][nj] != 0:
                            clustering_penalty += abs(board[i][j] - board[ni][nj])

        return max_tile + empty_spaces * 10 - clustering_penalty


    def possible_moves(self, board):
        moves = []
        for direction in ['w', 'a', 's', 'd']:
            new_board = move(direction, deepcopy(board))
            if new_board != board:
                new_board = fill_two_or_four(new_board)
                moves.append((direction, new_board))
        return moves

    def a_star_search(self, board, max_depth=6):
        class Node:
            def __init__(self, board, path, cost, depth):
                self.board = board
                self.path = path
                self.cost = cost
                self.depth = depth

            def __lt__(self, other):
                return self.cost < other.cost

        frontier = []
        start_node = Node(board, [], self.heuristic(board), 0)
        heapq.heappush(frontier, start_node)
        max_search_depth = 0

        while frontier:
            current_node = heapq.heappop(frontier)
            current_board, path, depth = current_node.board, current_node.path, current_node.depth

            max_search_depth = max(max_search_depth, depth)

            if check_game_status(current_board, 2048) != 'PLAY':
                if path:
                    print(f"Chosen move: {path[0]}, Path: {path}, Cost: {current_node.cost}, Depth: {depth}")
                    print(f"Max search depth: {max_search_depth}")
                    return path[0]
                else:
                    return 'w'

            if depth < max_depth:
                for direction, new_board in self.possible_moves(current_board):
                    new_path = path + [direction]
                    priority = len(new_path) + self.heuristic(new_board)
                    new_node = Node(new_board, new_path, priority, depth + 1)
                    heapq.heappush(frontier, new_node)

        print(f"No path found, choosing random move, Max search depth: {max_search_depth}")
        return random.choice(['w', 'a', 's', 'd'])
