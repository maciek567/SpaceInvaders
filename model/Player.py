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
        self.timeToRecover = 0  # number of fps after ship being killed by alien when ship blink

    def draw(self, win):
        if not self.killed:
            win.blit(self.ship, (self.x, self.y))
        else:
            if (self.timeToRecover // 5) % 2 == 0:
                win.blit(self.ship_trans, (self.x, self.y))
            else:
                win.blit(self.ship, (self.x, self.y))
            self.timeToRecover -= 1
            if self.timeToRecover == 0:
                self.killed = False

    def hit(self):
        explosion = pygame.mixer.Sound('sounds/explosion.wav')
        if not self.killed:
            explosion.play()
            self.health -= 1
            self.killed = True
            self.timeToRecover = 60

    def is_player_hit(self, enemy_projectiles):
        for enemy_projectile in enemy_projectiles:
            if self.x < enemy_projectile.x < self.x + 60 and self.killed is False:
                if self.y <= enemy_projectile.y <= self.y + 60:
                    enemy_projectiles.pop(enemy_projectiles.index(enemy_projectile))
                    self.hit()
