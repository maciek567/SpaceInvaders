import pygame
pygame.init()

SCORE = 0
LEVEL = 1
SPECIAL = 0
BOSS = False

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (169, 169, 169)
GREEN = (0, 255, 0)
RED = (200, 0, 0)
YELLOW = (255, 255, 0)
DARKER_YELLOW = (200, 200, 0)
BLUE = (66, 155, 254)
ORANGE = (255, 128, 0)

screenWidth = 1280
screenHeight = 720
alien_size = 60
win = pygame.display.set_mode((screenWidth, screenHeight))
pygame.display.set_caption("Space Invaders")
clock = pygame.time.Clock()
bg = pygame.image.load('../model/img/big_sky1.jpg')
music = pygame.mixer.music.load('../Main/sounds/music1.wav')
shoot = pygame.mixer.Sound('../Main/sounds/shoot.wav')
