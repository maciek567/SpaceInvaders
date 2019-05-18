import pygame


class Cover(object):

    cover_silver = pygame.image.load('../model/img/cover_silver.png')
    cover_yellow = pygame.image.load('../model/img/cover_yellow.png')
    cover_red = pygame.image.load('../model/img/cover_red.png')

    def __init__(self, x_pos, y_pos):
        self.health = 9
        self.x_pos = x_pos
        self.y_pos = y_pos

    def draw(self, win):
        if self.health >= 7:
            win.blit(self.cover_silver, (self.x_pos, self.y_pos))
        elif self.health >= 4:
            win.blit(self.cover_yellow, (self.x_pos, self.y_pos))
        elif self.health >= 1:
            win.blit(self.cover_red, (self.x_pos, self.y_pos))
        else:
            pass  # cover is destroyed - do not display anything

    # for every cover check collision with projectiles on screen
    def check_collision(self, projectiles):
        for projectile in projectiles:
            if self.x_pos <= projectile.x <= self.x_pos + 200:
                if self.y_pos <= projectile.y <= self.y_pos + 30 and self.health >= 1:
                    self.health -= 1
                    projectiles.pop(projectiles.index(projectile))
                    return False
        return True
