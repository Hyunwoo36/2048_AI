import json
import sys
import time
from copy import deepcopy

import pygame
from pygame.locals import *

from logic import *
from ai_agent import AI2048

# TODO: Add a RULES button on start page
# TODO: Add score keeping

# set up pygame for main gameplay
pygame.init()
c = json.load(open("constants.json", "r"))
screen = pygame.display.set_mode(
    (c["size"], c["size"]))
my_font = pygame.font.SysFont(c["font"], c["font_size"], bold=True)
WHITE = (255, 255, 255)


def winCheck(board, status, theme, text_col):
    """
    Check game status and display win/lose result.

    Parameters:
        board (list): game board
        status (str): game status
        theme (str): game interface theme
        text_col (tuple): text colour
    Returns:
        board (list): updated game board
        status (str): game status
    """
    if status != "PLAY":
        size = c["size"]
        # Fill the window with a transparent background
        s = pygame.Surface((size, size), pygame.SRCALPHA)
        s.fill(c["colour"][theme]["over"])
        screen.blit(s, (0, 0))

        # Display win/lose status
        if status == "WIN":
            msg = "YOU WIN!"
        else:
            msg = "GAME OVER!"

        screen.blit(my_font.render(msg, 1, text_col), (140, 180))
        # Ask user to play again
        screen.blit(my_font.render(
            "Play again? (y/ n)", 1, text_col), (80, 255))

        pygame.display.update()

        while True:
            for event in pygame.event.get():
                if event.type == QUIT or \
                        (event.type == pygame.KEYDOWN and event.key == K_n):
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN and event.key == K_y:
                    # 'y' is pressed to start a new game
                    board = newGame(theme, text_col)
                    return (board, "PLAY")
    return (board, status)


def newGame(theme, text_col):
    """
    Start a new game by resetting the board.

    Parameters:
        theme (str): game interface theme
        text_col (tuple): text colour
    Returns:
        board (list): new game board
    """
    # clear the board to start a new game
    board = [[0] * 4 for _ in range(4)]
    display(board, theme)

    screen.blit(my_font.render("NEW GAME!", 1, text_col), (130, 225))
    pygame.display.update()
    # wait for 1 second before starting over
    time.sleep(1)

    board = fillTwoOrFour(board, iter=2)
    display(board, theme)
    return board


def restart(board, theme, text_col):
    """
    Ask user to restart the game if 'n' key is pressed.

    Parameters:
        board (list): game board
        theme (str): game interface theme
        text_col (tuple): text colour
    Returns:
        board (list): new game board
    """
    # Fill the window with a transparent background
    s = pygame.Surface((c["size"], c["size"]), pygame.SRCALPHA)
    s.fill(c["colour"][theme]["over"])
    screen.blit(s, (0, 0))

    screen.blit(my_font.render("RESTART? (y / n)", 1, text_col), (85, 225))
    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == QUIT or \
                    (event.type == pygame.KEYDOWN and event.key == K_n):
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN and event.key == K_y:
                board = newGame(theme, text_col)
                return board


def display(board, theme):
    """
    Display the board 'matrix' on the game window.

    Parameters:
        board (list): game board
        theme (str): game interface theme
    """
    screen.fill(tuple(c["colour"][theme]["background"]))
    box = c["size"] // 4
    padding = c["padding"]
    for i in range(4):
        for j in range(4):
            colour = tuple(c["colour"][theme][str(board[i][j])])
            pygame.draw.rect(screen, colour, (j * box + padding,
                                              i * box + padding,
                                              box - 2 * padding,
                                              box - 2 * padding), 0)
            if board[i][j] != 0:
                if board[i][j] in (2, 4):
                    text_colour = tuple(c["colour"][theme]["dark"])
                else:
                    text_colour = tuple(c["colour"][theme]["light"])
                # display the number at the centre of the tile
                screen.blit(my_font.render("{:>4}".format(
                    board[i][j]), 1, text_colour),
                    # 2.5 and 7 were obtained by trial and error
                    (j * box + 2.5 * padding, i * box + 7 * padding))
    pygame.display.update()


def playGame(theme, difficulty, ai_mode = None):
    """
    Main game loop function.

    Parameters:
        theme (str): game interface theme
        difficulty (int): game difficulty, i.e., max. tile to get
    """
    

    # set text colour according to theme
    if theme == "light":
        text_col = tuple(c["colour"][theme]["dark"])
    else:
        text_col = WHITE
    print(f"Starting game with theme: {theme}, difficulty: {difficulty}, AI mode: {ai_mode}")
    board = newGame(theme, text_col)
    status = "PLAY"
    if ai_mode:
        ai_agent = AI2048(ai_mode)
        while status == "PLAY":
            move_key = ai_agent.get_move(board)
            print(f"Move decided: {move_key}")
            new_board = move(move_key, deepcopy(board))
            if new_board != board:
                board = fillTwoOrFour(new_board)
                display(board, theme)
                status = checkGameStatus(board, difficulty)
                board, status = winCheck(board, status, theme, text_col)
            pygame.event.pump()  # Process event queue without blocking.
    else:
        while True:
            for event in pygame.event.get():
                if event.type == QUIT or (event.type == pygame.KEYDOWN and event.key == K_q):
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_n:
                        board = restart(board, theme, text_col)
                        continue
                    if str(event.key) not in c["keys"]:
                        continue
                    key = c["keys"][str(event.key)]
                    new_board = move(key, deepcopy(board))
                    if new_board != board:
                        board = fillTwoOrFour(new_board)
                        display(board, theme)
                        status = checkGameStatus(board, difficulty)
                        board, status = winCheck(board, status, theme, text_col)
                        if status != "PLAY":
                            return  # Exit if game over