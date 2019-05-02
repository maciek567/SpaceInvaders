import pygame

pygame.init()


class Player(object):
    ship = pygame.image.load('img/ship.png')
    ship_trans = pygame.image.load('img/ship_trans.png')

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
                self.x = 20

    def hit(self):
        explosion.play()
        self.health -= 1
        self.killed = True
        self.timeToRecover = 60


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

    # move in loop from left border to right and then from right to left
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

    # when hit : invaderKilled.play()


class Projectile(object):
    def __init__(self, x, y, radius, color):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.vel = 8  # velocity of bullet

    def draw(self, win):
        pygame.draw.circle(win, self.color, (self.x, self.y), self.radius)


# in every frame display all objects on their current positions
def redraw_game_window():
    win.blit(bg, (0, 0))
    player.draw(win)
    enemy.draw(win)

    for bullet in projectiles:
        bullet.draw(win)

    pygame.display.update()


def menu():
    intro = True
    while intro:
        for event in pygame.event.get():
            pygame.quit()
            quit()


#  gameDisplay.fill((255, 255, 255))


screenWidth = 800
screenHeight = 480
win = pygame.display.set_mode((screenWidth, screenHeight))
pygame.display.set_caption("Space Invaders")
clock = pygame.time.Clock()

bg = pygame.image.load('img/sky.jpg')
music = pygame.mixer.music.load('sounds/music1.wav')
pygame.mixer.music.play(-1)
shoot = pygame.mixer.Sound('sounds/shoot.wav')
invaderKilled = pygame.mixer.Sound('sounds/invaderKilled.wav')
explosion = pygame.mixer.Sound('sounds/explosion.wav')

player = Player(20, screenHeight - 80, 60, 60)
enemy = Enemy(20, 20, 60, 60, screenWidth - 80)
projectiles = []

# Ship can shoot only if this variable is equal to 0. After every successful shoot this variable is incremented,
# and if reaches 10, then is reduced again to 0. This feature prevent from shooting all projectiles at once
# which can cause undesirable blurred trail on screen
canShoot = 0

run = True
while run:
    clock.tick(30)  # fps

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    if canShoot > 0:
        canShoot += 1
    if canShoot >= 10:
        canShoot = 0

    # display projectiles until they reach top border of screen
    # if projectile reaches top border of screen remove it from array so that ship could shoot next ones
    for projectile in projectiles:
        if 0 < projectile.y > 0:
            projectile.y -= projectile.vel
        else:
            projectiles.pop(projectiles.index(projectile))

    # handle keys pressed by player (left arrow, right arrow, space)
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player.x > player.vel and not player.killed:
        player.x -= player.vel
    elif keys[pygame.K_RIGHT] and player.x < screenWidth - player.width - player.vel and not player.killed:
        player.x += player.vel
    if keys[pygame.K_SPACE] and canShoot == 0 and not player.killed:
        shoot.play()
        if len(projectiles) < 10:  # up to 10 projectiles on screen at the same moment
            projectiles.append(Projectile(round(player.x + player.width // 2),
                                          round(player.y + player.height // 2), 4, (255, 128, 0)))
        canShoot += 1

    if keys[pygame.K_h]:
        player.hit()

    redraw_game_window()

pygame.quit()
