import json
import sys
import pygame
from pygame.locals import *
from game import show_menu

def main():
    global c, screen
    c = json.load(open("constants.json", "r"))
    pygame.init()
    screen = pygame.display.set_mode((120 + c["size"], c["size"]))
    pygame.display.set_caption("2048 by Rajit Banerjee/AI by the Boys")

    icon = pygame.transform.scale(pygame.image.load("images/icon.ico"), (32, 32))
    pygame.display.set_icon(icon)

    my_font = pygame.font.SysFont(c["font"], c["font_size"], bold=True)
    show_menu(c, screen, my_font)

if __name__ == "__main__":
    main()
