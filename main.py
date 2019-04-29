import pygame
pygame.init()


class Player(object):
    ship = pygame.image.load('img/ship.png')

    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 5

    def draw(self, win):
        win.blit(self.ship, (self.x, self.y))


class Enemy(object):
    alien = pygame.image.load('img/alien.png')

    def __init__(self, x, y, width, height, end):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.end = end
        self.path = [self.x, self.end]  # where our enemy starts and finishes his path.
        self.vel = 3

    def draw(self, win):
        self.move()
        win.blit(self.alien, (self.x, self.y))

    def move(self):
        if self.vel > 0:
            if self.x + self.vel < self.path[1]:
                self.x += self.vel
            else:
                self.vel = self.vel * -1
        else:
            if self.x - self.vel > self.path[0]:
                self.x += self.vel
            else:
                self.vel = self.vel * -1


def redraw_game_window():
    win.blit(bg, (0, 0))
    player.draw(win)
    enemy.draw(win)
    pygame.display.update()


screenWidth = 800
screenHeight = 480
win = pygame.display.set_mode((screenWidth, screenHeight))
pygame.display.set_caption("Space Invaders")
clock = pygame.time.Clock()

bg = pygame.image.load('img/sky.jpg')
player = Player(20, screenHeight - 80, 60, 60)
enemy = Enemy(20, 20, 60, 60, screenWidth - 80)


run = True
while run:
    clock.tick(30)  # fps

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT] and player.x > player.vel:
        player.x -= player.vel
    elif keys[pygame.K_RIGHT] and player.x < screenWidth - player.width - player.vel:
        player.x += player.vel

    redraw_game_window()

pygame.quit()
