import json
import sys
import time
from copy import deepcopy
import pygame
from pygame.locals import *
from .logic import *
from ai.ai_agent import AI2048
from ai.qlearning_agent import QLearningAgent
from .expectimax_agent import ExpectimaxAgent

pygame.init()
c = json.load(open("constants.json", "r"))
screen = pygame.display.set_mode((c["size"], c["size"]))
my_font = pygame.font.SysFont(c["font"], c["font_size"], bold=True)
WHITE = (255, 255, 255)

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

def play_game(theme, difficulty, ai_mode):
    text_col = tuple(c["colour"][theme]["dark"]) if theme == "light" else WHITE
    board = new_game(theme, text_col)
    status = "PLAY"
    final_score = 0

    if ai_mode == "qlearning":
        agent = QLearningAgent(actions=["w", "a", "s", "d"])
        while status == "PLAY":
            state = agent.get_state(board)
            action = agent.choose_action(state)
            new_board = move(action, deepcopy(board))
            if new_board != board:
                reward = sum(sum(row) for row in new_board) - sum(sum(row) for row in board)
                board = fill_two_or_four(new_board)
                display(board, theme)
                next_state = agent.get_state(board)
                agent.update(state, action, reward, next_state)
                status = check_game_status(board, difficulty)
                board, status = win_check(board, status, theme, text_col)
                final_score = sum(sum(row) for row in board)
            pygame.event.pump()
    elif ai_mode == "expectimax":
        ai_agent = ExpectimaxAgent()
        while status == "PLAY":
            move_key = ai_agent.getNextBestMoveExpectiminimax(board)
            new_board = move(move_key, deepcopy(board))
            if new_board != board:
                board = fill_two_or_four(new_board)
                display(board, theme)
                status = check_game_status(board, difficulty)
                board, status = win_check(board, status, theme, text_col)
                final_score = sum(sum(row) for row in board)
            pygame.event.pump()  
    else:
        ai_agent = AI2048(ai_mode)
        while status == "PLAY":
            move_key = ai_agent.get_move(board)
            new_board = move(move_key, deepcopy(board))
            if new_board != board:
                board = fill_two_or_four(new_board)
                display(board, theme)
                status = check_game_status(board, difficulty)
                board, status = win_check(board, status, theme, text_col)
                final_score = sum(sum(row) for row in board)
            pygame.event.pump()
    return final_score

def run_games(num_games, theme, difficulty, ai_mode):
    scores = []
    for i in range(num_games):
        score = play_game(theme, difficulty, ai_mode)
        scores.append(score)
    return scores
