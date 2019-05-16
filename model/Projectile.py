import pygame


class Projectile(object):
    def __init__(self, x, y, radius, color):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.vel = 10  # velocity of bullet

    def draw(self, win):
        pygame.draw.circle(win, self.color, (self.x, self.y), self.radius)
