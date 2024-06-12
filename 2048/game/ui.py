import pygame
from pygame.locals import *
import statistics
from .game import run_games
from ai.qlearning_agent import QLearningAgent
from ai.dqn_agent import DQNAgent
from ai.random import RandomAgent

class Button:
    def __init__(self, colour, x, y, width, height, text=""):
        self.colour = colour
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text

    def draw(self, win, text_col, font, constants):
        draw_round_rect(win, self.colour, (self.x, self.y, self.width, self.height), constants)
        if self.text != "":
            text = font.render(self.text, 1, text_col)
            win.blit(text, (self.x + (self.width / 2 - text.get_width() / 2), self.y + (self.height / 2 - text.get_height() / 2)))

    def is_over(self, pos):
        if self.x < pos[0] < self.x + self.width and self.y < pos[1] < self.y + self.height:
            return True
        return False

def draw_round_rect(surface, colour, rect, constants, radius=0.4):
    BLACK = tuple(constants["colour"]["light"]["dark"])  # Adjust to the correct path for BLACK
    rect = Rect(rect)
    colour = Color(*colour)
    alpha = colour.a
    colour.a = 0
    pos = rect.topleft
    rect.topleft = 0, 0
    rectangle = pygame.Surface(rect.size, SRCALPHA)

    circle = pygame.Surface([min(rect.size) * 3] * 2, SRCALPHA)
    pygame.draw.ellipse(circle, BLACK, circle.get_rect(), 0)
    circle = pygame.transform.smoothscale(circle, [int(min(rect.size) * radius)] * 2)

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

def show_menu(constants, screen, my_font):
    theme = 'light'
    difficulty = 2048
    ai_mode_selected = False
    ai_mode = None
    agent = None

    button_width = 125
    button_height = 50
    button_start_y = 375
    button_spacing = 15
    first_button_x = 30

    buttons = {
        # "A*": Button(tuple(constants["colour"][theme]["2048"]), first_button_x, button_start_y, button_width, button_height, "A*"),
        "E-MAX": Button(tuple(constants["colour"][theme]["2048"]), first_button_x, button_start_y, button_width, button_height, "E-MAX"),
        "Random": Button(tuple(constants["colour"][theme]["2048"]), first_button_x + (button_width + button_spacing), button_start_y, button_width, button_height, "Random"),
        "Q-Learning": Button(tuple(constants["colour"][theme]["2048"]), first_button_x + 2 * (button_width + button_spacing), button_start_y, button_width, button_height, "Q-Learning"),
        "DQN": Button(tuple(constants["colour"][theme]["2048"]), first_button_x + 3 * (button_width + button_spacing), button_start_y, button_width, button_height, "DQN"),
        "start": Button(tuple(constants["colour"][theme]["2048"]), 180, 450, 200, 50, "Start AI Game")
    }

    label = my_font.render("Select AI Mode:", True, tuple(constants["colour"][theme]["dark"]))

    while True:
        screen.fill(tuple(constants["colour"][theme]["background"]))
        screen.blit(pygame.transform.scale(pygame.image.load("images/icon.ico"), (200, 200)), (155, 50))
        screen.blit(label, (first_button_x, 325))

        for button in buttons.values():
            button.draw(screen, tuple(constants["colour"][theme]["dark"]), my_font, constants)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_q):
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()

                for key, button in buttons.items():
                    if button.is_over(pos):
                        if key in ["E-MAX", "Random", "Q-Learning", "DQN"]:
                            ai_mode = key.lower().replace("-", "").replace(" ", "_")
                            ai_mode_selected = True
                            if key == "Random":
                                agent = RandomAgent()
                                print("Random agent initialized.")
                            elif key == "DQN":
                                state_size = (4, 4, 1)
                                action_size = 4
                                agent = DQNAgent(state_size, action_size)
                                print("DQN agent initialized.")
                            elif key == "Q-Learning":
                                agent = QLearningAgent()
                                print("Q-Learning agent initialized.")
                                
                        if key == "start" and ai_mode_selected:
                            if ai_mode == "qlearning" and agent is None:
                                agent = QLearningAgent()  # Ensure the agent is initialized if not already
                            scores = run_games(10, theme, difficulty, ai_mode, agent)  # Pass the agent
                            average_score = statistics.mean(scores)
                            print(f"Average score for {ai_mode}: {average_score}")
                            print(f"All scores for {ai_mode}: ", scores)
                            return
