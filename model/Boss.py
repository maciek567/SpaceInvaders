import pygame
import Main
from view import next_level


class Boss(object):
    boss_picture = pygame.image.load('../model/img/boss.png')

    def __init__(self, x, y, width, height, start, end):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.health = 10
        self.start = start
        self.end = end
        self.path = [self.start, self.end]  # where our enemy starts and finishes his path.
        self.vel = 6
        self.time_to_recovery = 0
        self.protected = False

    def draw(self, win):
        self.move()
        win.blit(self.boss_picture, (self.x, self.y))
        pygame.draw.rect(win, (255, 0, 0), (self.x + 50, self.y - 30, 200, 20))
        pygame.draw.rect(win, (0, 128, 0), (self.x + 50, self.y - 30, 200 - 20 * (10 - self.health), 20))

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

    def check_collision(self, projectiles, win):
        for projectile in projectiles:
            if self.health >= 1:
                if self.x <= projectile.x <= self.x + self.width:
                    if self.y <= projectile.y <= self.y + self.height:
                        projectiles.pop(projectiles.index(projectile))
                        if not self.protected:
                            Main.SCORE += 10
                            self.health -= 1
                            self.protected = True
                            self.time_to_recovery = 60
            if self.health <= 0:
                self.draw(win)
                pygame.display.update()
                Main.SCORE += 500
                explosion = pygame.mixer.Sound('../Main/sounds/explosion.wav')
                explosion.play()
                next_level.you_win()

