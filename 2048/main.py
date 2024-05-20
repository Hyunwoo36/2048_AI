import json
import sys
import os

import pygame
from pygame.locals import *

from game import playGame

# We are trying to implement
# Expectimax, A* Search, and Reinforcement Learning.
# make the button options for AI and three algorithms.

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


class Button():
    """
    Class to create a new button in pygame window.
    """
    # initialise the button
    def __init__(self, colour, x, y, width, height, text=""):
        self.colour = colour
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text

    # draw the button on the screen
    def draw(self, win, text_col, font):
        drawRoundRect(win, self.colour, (self.x, self.y,
                                         self.width, self.height))

        if self.text != "":
            text = font.render(self.text, 1, text_col)
            win.blit(text, (self.x + (self.width/2 - text.get_width()/2),
                            self.y + (self.height/2 - text.get_height()/2)))

    # check if the mouse is positioned over the button
    def isOver(self, pos):
        # pos is the mouse position or a tuple of (x,y) coordinates
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True

        return False


def drawRoundRect(surface, colour, rect, radius=0.4):
    """
    Draw an antialiased rounded filled rectangle on screen

    Parameters:
        surface (pygame.Surface): destination
        colour (tuple): RGB values for rectangle fill colour
        radius (float): 0 <= radius <= 1
    """

    rect = Rect(rect)
    colour = Color(*colour)
    alpha = colour.a
    colour.a = 0
    pos = rect.topleft
    rect.topleft = 0, 0
    rectangle = pygame.Surface(rect.size, SRCALPHA)

    circle = pygame.Surface([min(rect.size) * 3] * 2, SRCALPHA)
    pygame.draw.ellipse(circle, BLACK, circle.get_rect(), 0)
    circle = pygame.transform.smoothscale(
        circle, [int(min(rect.size)*radius)]*2)

    radius = rectangle.blit(circle, (0, 0))
    radius.bottomright = rect.bottomright
    rectangle.blit(circle, radius)
    radius.topright = rect.topright
    rectangle.blit(circle, radius)
    radius.bottomleft = rect.bottomleft
    rectangle.blit(circle, radius)

    rectangle.fill(BLACK, rect.inflate(-radius.w, 0))
    rectangle.fill(BLACK, rect.inflate(0, -radius.h))

    rectangle.fill(colour, special_flags=BLEND_RGBA_MAX)
    rectangle.fill((255, 255, 255, alpha), special_flags=BLEND_RGBA_MIN)

    surface.blit(rectangle, pos)
    
def showMenu():
    """
    Display the start screen with AI mode options clearly and ensure they are selectable.
    """
    global theme, difficulty, c
    theme = 'light'  # Assuming light theme for better visibility
    difficulty = 2048
    ai_mode_selected = False
    ai_mode = None

    # Adjusting button sizes and positions based on provided screenshot
    button_width = 125
    button_height = 50
    button_start_y = 375
    button_spacing = 15
    
    first_button_x = 80  # Reduced starting x position

    buttons = {
        "A*": Button(tuple(c["colour"][theme]["2048"]), first_button_x, button_start_y, button_width, button_height, "A*"),
        "E-MAX": Button(tuple(c["colour"][theme]["2048"]), first_button_x + button_width + button_spacing, button_start_y, button_width, button_height, "E-MAX"),
        "Random": Button(tuple(c["colour"][theme]["2048"]), first_button_x + 2 * (button_width + button_spacing), button_start_y, button_width, button_height, "Random"),
        "start": Button(tuple(c["colour"][theme]["2048"]), 180, 450, 200, 50, "Start AI Game")
    }

    # Adjusting font size and style
    my_font = pygame.font.SysFont(c["font"], 20)
    label = my_font.render("Select AI Mode:", True, tuple(c["colour"][theme]["dark"]))
    
    while True:
        screen.fill(tuple(c["colour"][theme]["background"]))
        screen.blit(pygame.transform.scale(
            pygame.image.load("images/icon.ico"), (200, 200)), (155, 50)
        )
        screen.blit(label, (first_button_x, 325))  # Positioning the label above the buttons

        for button in buttons.values():
            button.draw(screen, tuple(c["colour"][theme]["dark"]), my_font)

        pygame.display.update()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_q):
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                print("Mouse button pressed at:", pos)  # Debugging print statement

                for key, button in buttons.items():
                    if button.isOver(pos):
                        print(f"Button {key} clicked.")  # More specific debugging print statement

                        if key in ["A*", "E-MAX", "Random"]:
                            ai_mode = key.lower().replace("-", "")
                            ai_mode_selected = True
                            print("AI Mode selected:", ai_mode)  # Debugging print statement

                        if key == "start" and ai_mode_selected:
                            print(f"Starting game with {theme}, {difficulty}, {ai_mode}")
                            playGame(theme, difficulty, ai_mode=ai_mode)
                            return  # Exits after starting the game

if __name__ == "__main__":
    # load json data
    c = json.load(open("constants.json", "r"))

    # set up pygame
    pygame.init()
    # set up screen
    screen = pygame.display.set_mode(
        (c["size"], c["size"])
    )
    pygame.display.set_caption("2048 by Rajit Banerjee")

    # display game icon in window
    icon = pygame.transform.scale(
        pygame.image.load("images/icon.ico"), (32, 32)
    )
    pygame.display.set_icon(icon)

    # set font according to json data specifications
    my_font = pygame.font.SysFont(c["font"], c["font_size"], bold=True)

    # display the start screen 
    showMenu()
