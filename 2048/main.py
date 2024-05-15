import json
import sys

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
    Display the start screen
    """
    # create light theme button
    # light_theme = Button(
    #     tuple(c["colour"]["light"]["2048"]), 200-70, 275, 45, 45, "light")
    # # create dark theme button
    # dark_theme = Button(
    #     tuple(c["colour"]["dark"]["2048"]), 270-70, 275, 45, 45, "dark")
    global theme, difficulty
    # initialise theme
    theme = 'light'  # Start with no theme selected
    difficulty = 2048  # Default difficulty not set
    theme_selected = False
    diff_selected = False
    buttons = {
        "light_theme": Button(tuple(c["colour"]["light"]["2048"]), 130, 275, 45, 45, "Light"),
        "dark_theme": Button(tuple(c["colour"]["dark"]["2048"]), 200, 275, 45, 45, "Dark"),
        "2048": Button(tuple(c["colour"]["light"]["64"]), 130, 330, 45, 45, "2048"),
        "1024": Button(tuple(c["colour"]["light"]["2048"]), 200, 330, 45, 45, "1024"),
        "512": Button(tuple(c["colour"]["light"]["2048"]), 270, 330, 45, 45, "512"),
        "256": Button(tuple(c["colour"]["light"]["2048"]), 340, 330, 45, 45, "256"),
        "play": Button(tuple(c["colour"]["light"]["2048"]), 130, 400, 45, 45, "Play"),
        "A*": Button(tuple(c["colour"]["light"]["2048"]), 200, 400, 45, 45, "A*"),
        "E-MAX": Button(tuple(c["colour"]["light"]["2048"]), 270, 400, 45, 45, "E-MAX"),
        "Random": Button(tuple(c["colour"]["light"]["2048"]), 340, 400, 45, 45, "Random")
    }

    while True:
        screen.fill(BLACK)
        for button in buttons.values():
            button.draw(screen, WHITE, pygame.font.SysFont(c["font"], 14, bold=True))
        pygame.display.update()

        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()
            if event.type == QUIT or (event.type == pygame.KEYDOWN and event.key == K_q):
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if buttons["light_theme"].isOver(pos) or buttons["dark_theme"].isOver(pos):
                    theme = "light" if buttons["light_theme"].isOver(pos) else "dark"
                    theme_selected = True

                for key in ["2048", "1024", "512", "256"]:
                    if buttons[key].isOver(pos):
                        difficulty = int(key)
                        diff_selected = True

                if any([buttons[mode].isOver(pos) for mode in ["play", "A*", "E-MAX", "Random"]]) and theme_selected and diff_selected:
                    ai_mode = 'astar' if buttons["A*"].isOver(pos) else 'expectimax' if buttons["E-MAX"].isOver(pos) else 'random' if buttons["Random"].isOver(pos) else None
                    playGame(theme, difficulty, ai_mode=ai_mode)

                # Reset if clicking outside the buttons
                if not any([b.isOver(pos) for b in buttons.values()]):
                    theme_selected = False
                    diff_selected = False
                    theme = 'light'  # Reset to default
                    difficulty = 2048
                    
                    
    # # pygame loop for start screen
    # while True:
    #     screen.fill(BLACK)

    #     screen.blit(pygame.transform.scale(
    #         pygame.image.load("images/icon.ico"), (200, 200)), (155, 50))

    #     font = pygame.font.SysFont(c["font"], 15, bold=True)

    #     theme_text = font.render("Theme: ", 1, WHITE)
    #     screen.blit(theme_text, (55, 285))

    #     diff_text = font.render("Difficulty: ", 1, WHITE)
    #     screen.blit(diff_text, (40, 345))

    #     # set fonts for buttons
    #     font1 = pygame.font.SysFont(c["font"], 15, bold=True)
    #     font2 = pygame.font.SysFont(c["font"], 14, bold=True)

    #     # draw all buttons on the screen
    #     light_theme.draw(screen, BLACK, font1)
    #     dark_theme.draw(screen, (197, 255, 215), font1)
    #     _2048.draw(screen, BLACK, font2)
    #     _1024.draw(screen, BLACK, font2)
    #     _512.draw(screen, BLACK, font2)
    #     _256.draw(screen, BLACK, font2)
    #     play.draw(screen, BLACK, font1)
    #     A_star.draw(screen, BLACK, font1)
    #     e_max.draw(screen, BLACK, font1)
    #     rand.draw(screen, BLACK, font1)

    #     pygame.display.update()

    #     for event in pygame.event.get():
    #         # store mouse position (coordinates)
    #         pos = pygame.mouse.get_pos()

    #         if event.type == QUIT or \
    #                 (event.type == pygame.KEYDOWN and event.key == K_q):
    #             # exit if q is pressed 
    #             pygame.quit()
    #             sys.exit()

    #         # check if a button is clicked
    #         if event.type == pygame.MOUSEBUTTONDOWN:
    #             # select light theme
    #             if light_theme.isOver(pos):
    #                 dark_theme.colour = tuple(c["colour"]["dark"]["2048"])
    #                 light_theme.colour = tuple(c["colour"]["light"]["64"])
    #                 theme = "light"
    #                 theme_selected = True

    #             # select dark theme
    #             if dark_theme.isOver(pos):
    #                 dark_theme.colour = tuple(c["colour"]["dark"]["background"])
    #                 light_theme.colour = tuple(c["colour"]["light"]["2048"])
    #                 theme = "dark"
    #                 theme_selected = True
                
    #             if _2048.isOver(pos):
    #                 _2048.colour = tuple(c["colour"]["light"]["64"])
    #                 _1024.colour = tuple(c["colour"]["light"]["2048"])
    #                 _512.colour = tuple(c["colour"]["light"]["2048"])
    #                 _256.colour = tuple(c["colour"]["light"]["2048"])
    #                 difficulty = 2048
    #                 diff_selected = True
                
    #             if _1024.isOver(pos):
    #                 _1024.colour = tuple(c["colour"]["light"]["64"])
    #                 _2048.colour = tuple(c["colour"]["light"]["2048"])
    #                 _512.colour = tuple(c["colour"]["light"]["2048"])
    #                 _256.colour = tuple(c["colour"]["light"]["2048"])
    #                 difficulty = 1024
    #                 diff_selected = True
                
    #             if _512.isOver(pos):
    #                 _512.colour = tuple(c["colour"]["light"]["64"])
    #                 _1024.colour = tuple(c["colour"]["light"]["2048"])
    #                 _2048.colour = tuple(c["colour"]["light"]["2048"])
    #                 _256.colour = tuple(c["colour"]["light"]["2048"])
    #                 difficulty = 512
    #                 diff_selected = True
                
    #             if _256.isOver(pos):
    #                 _256.colour = tuple(c["colour"]["light"]["64"])
    #                 _1024.colour = tuple(c["colour"]["light"]["2048"])
    #                 _512.colour = tuple(c["colour"]["light"]["2048"])
    #                 _2048.colour = tuple(c["colour"]["light"]["2048"])
    #                 difficulty = 256
    #                 diff_selected = True

    #             # play game with selected theme
    #             if play.isOver(pos):
    #                 if theme != "" and difficulty != 0:
    #                     playGame(theme, difficulty)
    #             if A_star.isOver(pos):
    #                 # Play using A* algorithm
    #                 playGame(theme, difficulty, ai_mode='astar')
    #             elif e_max.isOver(pos):
    #                 # Play using Expectimax algorithm
    #                 playGame(theme, difficulty, ai_mode='expectimax')
    #             elif rand.isOver(pos):
    #                 # Play using random moves (simple example for AI)
    #                 playGame(theme, difficulty, ai_mode='random')
                    
    #             # reset theme & diff choice if area outside buttons is clicked
    #             if not play.isOver(pos) and \
    #                 not dark_theme.isOver(pos) and \
    #                 not light_theme.isOver(pos) and \
    #                 not _2048.isOver(pos) and \
    #                 not _1024.isOver(pos) and \
    #                 not _512.isOver(pos) and \
    #                 not _256.isOver(pos):

    #                 theme = ""
    #                 theme_selected = False
    #                 diff_selected = False

    #                 light_theme.colour = tuple(c["colour"]["light"]["2048"])
    #                 dark_theme.colour = tuple(c["colour"]["dark"]["2048"])
    #                 _2048.colour = tuple(c["colour"]["light"]["2048"])
    #                 _1024.colour = tuple(c["colour"]["light"]["2048"])
    #                 _512.colour = tuple(c["colour"]["light"]["2048"])
    #                 _256.colour = tuple(c["colour"]["light"]["2048"])
                    

    #         # change colour on hovering over buttons
    #         if event.type == pygame.MOUSEMOTION:
    #             if not theme_selected:
    #                 if light_theme.isOver(pos):
    #                     light_theme.colour = tuple(c["colour"]["light"]["64"])
    #                 else:
    #                     light_theme.colour = tuple(c["colour"]["light"]["2048"])
                    
    #                 if dark_theme.isOver(pos):
    #                     dark_theme.colour = tuple(c["colour"]["dark"]["background"])
    #                 else:
    #                     dark_theme.colour = tuple(c["colour"]["dark"]["2048"])
                
    #             if not diff_selected:
    #                 if _2048.isOver(pos):
    #                     _2048.colour = tuple(c["colour"]["light"]["64"])
    #                 else:
    #                     _2048.colour = tuple(c["colour"]["light"]["2048"])
                    
    #                 if _1024.isOver(pos):
    #                     _1024.colour = tuple(c["colour"]["light"]["64"])
    #                 else:
    #                     _1024.colour = tuple(c["colour"]["light"]["2048"])
                    
    #                 if _512.isOver(pos):
    #                     _512.colour = tuple(c["colour"]["light"]["64"])
    #                 else:
    #                     _512.colour = tuple(c["colour"]["light"]["2048"])
                    
    #                 if _256.isOver(pos):
    #                     _256.colour = tuple(c["colour"]["light"]["64"])
    #                 else:
    #                     _256.colour = tuple(c["colour"]["light"]["2048"])
                
    #             if play.isOver(pos):
    #                 play.colour = tuple(c["colour"]["light"]["64"])
    #             else:
    #                 play.colour = tuple(c["colour"]["light"]["2048"])


if __name__ == "__main__":
    # load json data
    c = json.load(open("constants.json", "r"))

    # set up pygame
    pygame.init()
    # set up screen
    screen = pygame.display.set_mode(
        (c["size"], c["size"]))
    pygame.display.set_caption("2048 by Rajit Banerjee")

    # display game icon in window
    icon = pygame.transform.scale(
        pygame.image.load("images/icon.ico"), (32, 32))
    pygame.display.set_icon(icon)

    # set font according to json data specifications
    my_font = pygame.font.SysFont(c["font"], c["font_size"], bold=True)

    # display the start screen 
    showMenu()
