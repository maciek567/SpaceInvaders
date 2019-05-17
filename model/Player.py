import pygame


class Player(object):
    ship = pygame.image.load('../model/img/ship.png')
    ship_trans = pygame.image.load('../model/img/ship_trans.png')

    def __init__(self, x, y, width, height):
        self.x = x  # coordinates of ship at the beginning
        self.y = y
        self.width = width
        self.height = height
        self.vel = 5  # velocity of ship
        self.health = 3
        self.killed = False
        self.protection = False
        self.timeToRecover = 0  # number of fps after death when player cannot move
        self.protectionTime = 0  # number of fps after death when player cannot loose life

    def draw(self, win):
        if not self.protection:
            win.blit(self.ship, (self.x, self.y))
        else:
            if (self.protectionTime // 5) % 2 == 0:
                win.blit(self.ship_trans, (self.x, self.y))
            else:
                win.blit(self.ship, (self.x, self.y))

            self.protectionTime -= 1
            if self.protectionTime == 0:
                self.protection = False
        if self.killed:
            self.timeToRecover -= 1
            if self.timeToRecover == 0:
                self.killed = False

    def hit(self):
        explosion = pygame.mixer.Sound('sounds/explosion.wav')
        if not self.protection:
            explosion.play()
            self.health -= 1
            self.killed = True
            self.protection = True
            self.timeToRecover = 50
            self.protectionTime = 100

    def is_player_hit(self, enemy_projectiles):
        for enemy_projectile in enemy_projectiles:
            if self.x < enemy_projectile.x < self.x + 60:
                if self.y <= enemy_projectile.y <= self.y + 60:
                    enemy_projectiles.pop(enemy_projectiles.index(enemy_projectile))
                    self.hit()
