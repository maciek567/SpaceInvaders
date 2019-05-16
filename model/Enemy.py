import pygame
import random
import Main


class Enemy(object):
    alien = pygame.image.load('../model/img/alien.png')
    alien1 = pygame.image.load('../model/img/alien1.png')

    def __init__(self, x, y, width, height, start, end):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.start = start
        self.end = end
        self.path = [self.start, self.end]  # where our enemy starts and finishes his path.
        self.vel = Main.LEVEL
        self.status = True  # death or alive
        self.type = random.randint(0, 1)

    def draw_1(self, win):
        win.blit(self.alien, (self.x, self.y))

    def draw_2(self, win):
        win.blit(self.alien1, (self.x, self.y))

    def draw(self, win):
        self.move()
        if self.type == 0:
            win.blit(self.alien, (self.x, self.y))
        else:
            win.blit(self.alien1, (self.x, self.y))

    # move in loop from left border to right and then from right to left
    def move(self):
        if self.vel > 0:
            if self.x + self.vel < self.path[1]:
                self.x += self.vel
            else:
                self.y += 20
                self.vel = self.vel * -1
        else:
            if self.x - self.vel > self.path[0]:
                self.x += self.vel
            else:
                self.y += 20
                self.vel = self.vel * -1

    # for every foe check collision with projectiles on screen
    def check_collision(self, projectiles):
        invader_killed = pygame.mixer.Sound('sounds/invaderKilled.wav')
        for projectile in projectiles:
            if self.x <= projectile.x <= self.x + 60 and self.status is True:
                if self.y <= projectile.y <= self.y + 40:
                    invader_killed.play()
                    Main.SCORE += 10
                    projectiles.pop(projectiles.index(projectile))
                    return False
        return True
