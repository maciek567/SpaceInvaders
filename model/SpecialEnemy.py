import pygame
import Main


class SpecialEnemy(object):
    special = pygame.image.load('../model/img/special.png')

    def __init__(self, x, y, width, height, start, end, status):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.start = start
        self.end = end
        self.path = [self.start, self.end]  # where our enemy starts and finishes his path.
        self.vel = 3
        self.status = status  # death or alive

    def draw(self, win):
        self.move()
        win.blit(self.special, (self.x, self.y))

    def move(self):
        if self.x + self.vel < self.path[1]:
            self.x += self.vel
        else:
            self.status = False

    def check_collision(self, projectiles):
        invader_killed = pygame.mixer.Sound('sounds/invaderKilled.wav')
        for projectile in projectiles:
            if self.x <= projectile.x <= self.x + 60 and self.status is True:
                if self.y <= projectile.y <= self.y + 50:
                    invader_killed.play()
                    Main.SCORE += 100
                    projectiles.pop(projectiles.index(projectile))
                    return False
        return True
