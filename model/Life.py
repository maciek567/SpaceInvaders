import pygame


class Life(object):
    life = pygame.image.load('../model/img/life.png')

    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.status = True

    def draw(self, win):
        win.blit(self.life, (self.x, self.y))
