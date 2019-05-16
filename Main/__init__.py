import pygame
pygame.init()

SCORE = 0
LEVEL = 1
SPECIAL = 0

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (169, 169, 169)
GREEN = (0, 255, 0)
RED = (200, 0, 0)

screenWidth = 1920
screenHeight = 1060

win = pygame.display.set_mode((screenWidth, screenHeight))
pygame.display.set_caption("Space Invaders")
clock = pygame.time.Clock()
bg = pygame.image.load('../model/img/big_sky1.jpg')
music = pygame.mixer.music.load('sounds/music1.wav')
shoot = pygame.mixer.Sound('sounds/shoot.wav')
