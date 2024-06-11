import json
import sys
import time
from copy import deepcopy
import pygame
from pygame.locals import *
from .logic import *
from ai.ai_agent import AI2048
from ai.qlearning_agent import QLearningAgent
from ai.dqn_agent import DQNAgent
import numpy as np
import matplotlib.pyplot as plt

pygame.init()
c = json.load(open("constants.json", "r"))
screen = pygame.display.set_mode((c["size"], c["size"]))
my_font = pygame.font.SysFont(c["font"], c["font_size"], bold=True)
WHITE = (255, 255, 255)
model_save_path = "q_table.json"

def win_check(board, status, theme, text_col):
    if status != "PLAY":
        size = c["size"]
        s = pygame.Surface((size, size), pygame.SRCALPHA)
        s.fill(c["colour"][theme]["over"])
        screen.blit(s, (0, 0))

        msg = "YOU WIN!" if status == "WIN" else "GAME OVER!"
        screen.blit(my_font.render(msg, 1, text_col), (140, 180))
        pygame.display.update()
        time.sleep(1)
    return (board, status)

def new_game(theme, text_col):
    board = [[0] * 4 for _ in range(4)]
    display(board, theme)

    screen.blit(my_font.render("NEW GAME!", 1, text_col), (130, 225))
    pygame.display.update()
    time.sleep(1)

    board = fill_two_or_four(board, iter=2)
    display(board, theme)
    return board

def restart(board, theme, text_col):
    s = pygame.Surface((c["size"], c["size"]), pygame.SRCALPHA)
    s.fill(c["colour"][theme]["over"])
    screen.blit(s, (0, 0))

    screen.blit(my_font.render("RESTART? (y / n)", 1, text_col), (85, 225))
    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == pygame.KEYDOWN and event.key == K_n):
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN and event.key == K_y:
                board = new_game(theme, text_col)
                return board

def display(board, theme):
    screen.fill(tuple(c["colour"][theme]["background"]))
    box = c["size"] // 4
    padding = c["padding"]
    for i in range(4):
        for j in range(4):
            colour = tuple(c["colour"][theme][str(board[i][j])])
            pygame.draw.rect(screen, colour, (j * box + padding, i * box + padding, box - 2 * padding, box - 2 * padding), 0)
            if board[i][j] != 0:
                text_colour = tuple(c["colour"][theme]["dark"]) if board[i][j] in (2, 4) else tuple(c["colour"][theme]["light"])
                screen.blit(my_font.render("{:>4}".format(board[i][j]), 1, text_colour), (j * box + 2.5 * padding, i * box + 7 * padding))
    pygame.display.update()

def calculate_smoothness(board):
    smoothness = 0
    for i in range(4):
        for j in range(4):
            if board[i][j] != 0:
                value = np.log2(board[i][j])
                for direction in [(0, 1), (1, 0)]:  # Right, Down
                    x, y = i + direction[0], j + direction[1]
                    if x < 4 and y < 4 and board[x][y] != 0:
                        target_value = np.log2(board[x][y])
                        smoothness -= abs(value - target_value)
    return smoothness

def calculate_monotonicity(board):
    def calculate_single_line(line):
        increasing, decreasing = 0, 0
        for i in range(3):
            if line[i] > line[i + 1]:
                increasing += line[i] - line[i + 1]
            elif line[i] < line[i + 1]:
                decreasing += line[i + 1] - line[i]
        return max(increasing, decreasing)

    monotonicity = 0
    for i in range(4):
        monotonicity += calculate_single_line(board[i])  # Row
        monotonicity += calculate_single_line([board[j][i] for j in range(4)])  # Column
    return -monotonicity  # Negative because higher monotonicity should be better

def calculate_reward(board, new_board, valid_move):
    if not valid_move:
        return -10  # Heavy penalty for invalid move
    
    score_diff = sum(sum(row) for row in new_board) - sum(sum(row) for row in board)
    max_tile_new = max(max(row) for row in new_board)
    max_tile_old = max(max(row) for row in board)
    empty_tiles_new = sum(row.count(0) for row in new_board)
    empty_tiles_old = sum(row.count(0) for row in board)
    
    bonus = 1.0 * (max_tile_new - max_tile_old)  # Higher bonus for achieving higher tiles
    empty_tile_bonus = 0.5 * (empty_tiles_new - empty_tiles_old)  # Higher bonus for creating empty tiles
    move_bonus = 0.1  # Small positive reward for each valid move

    # Calculate smoothness and monotonicity
    smoothness_old = calculate_smoothness(board)
    smoothness_new = calculate_smoothness(new_board)
    monotonicity_old = calculate_monotonicity(board)
    monotonicity_new = calculate_monotonicity(new_board)

    smoothness_bonus = 0.1 * (smoothness_new - smoothness_old)
    monotonicity_bonus = 0.1 * (monotonicity_new - monotonicity_old)

    return score_diff + bonus + empty_tile_bonus + move_bonus + smoothness_bonus + monotonicity_bonus

def play_game(agent, theme, difficulty, ai_mode):
    text_col = tuple(c["colour"][theme]["dark"]) if theme == "light" else WHITE
    board = new_game(theme, text_col)
    status = "PLAY"
    final_score = 0
    invalid_moves = 0
    max_steps_without_improvement = 50
    steps_without_improvement = 0
    last_max_tile = 0

    while status == "PLAY":
        state = agent.get_state(board)
        # q learning
        # action = agent.choose_action(state)
        # DQN
        action_index = agent.choose_action(state)
        action = agent.actions[action_index]
        print(f"Action: {action}, State: {state}")
        print("Board before action:")
        print(board)
        new_board = deepcopy(board)
        new_board, valid_move = move(action, new_board)
        if valid_move:
            reward = calculate_reward(board, new_board, valid_move)
            done = status != "PLAY"
            next_state = agent.get_state(new_board)
            # q leraning
            # agent.update(state, action, reward, next_state)
            agent.update(state, action, reward, next_state, done)
            print(f"State: {state}, Action: {action}, Reward: {reward}, Next State: {next_state}, Done: {done}")
            print("Board after action:")
            print(new_board)
            board = fill_two_or_four(new_board)
            display(board, theme)
            status = check_game_status(board, difficulty)
            board, status = win_check(board, status, theme, text_col)
            final_score = max(max(row) for row in board)
            steps_without_improvement = 0 if max(max(row) for row in board) > last_max_tile else steps_without_improvement + 1
            last_max_tile = max(max(row) for row in board)
        else:
            print("Invalid move.")
            invalid_moves += 1
            steps_without_improvement += 1
             # Penalize invalid move
            # q learning
            # agent.update(state, action, -10, state) 
            # DQN
            agent.update(state, action_index, -10, state, True)
        pygame.event.pump()

        if steps_without_improvement >= max_steps_without_improvement:
            break

    print(f"Episode completed, Total Reward: {final_score}, Invalid Moves: {invalid_moves}")
    return final_score

def run_games(num_games, theme, difficulty, ai_mode, agent):
    scores = []

    for i in range(num_games):
        score = play_game(agent, theme, difficulty, ai_mode)
        scores.append(score)
    print("AI MODE:", ai_mode)
    # Save the Q-learning model (Q-table)
    if ai_mode == "qlearning":
        agent.save_q_table()

    return scores