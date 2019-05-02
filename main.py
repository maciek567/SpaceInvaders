import pygame
pygame.init()


class Player(object):
    ship = pygame.image.load('img/ship.png')

    def __init__(self, x, y, width, height):
        self.x = x  # coordinates of ship at the beginning
        self.y = y
        self.width = width
        self.height = height
        self.vel = 5  # velocity of ship

    def draw(self, win):
        win.blit(self.ship, (self.x, self.y))

    # when hit : explosion.play()


class Enemy(object):
    alien = pygame.image.load('img/alien.png')

    def __init__(self, x, y, width, height, start, end, status):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.start = start
        self.end = end
        self.path = [self.start, self.end]  # where our enemy starts and finishes his path.
        self.vel = 3
        self.status = True  # death or alive

    def draw(self, win):
        self.move()
        win.blit(self.alien, (self.x, self.y))

    # move in loop from left border to right and then from right to left
    def move(self):
        if self.vel > 0:
            if self.x + self.vel < self.path[1]:
                self.x += self.vel
            else:
                self.y += 40
                self.vel = self.vel * -1
        else:
            if self.x - self.vel > self.path[0]:
                self.x += self.vel
            else:
                self.y += 40
                self.vel = self.vel * -1

    # when hit : invaderKilled.play()


class Projectile(object):
    def __init__(self, x, y, radius, color):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.vel = 6  # velocity of bullet

    def draw(self, win):
        pygame.draw.circle(win, self.color, (self.x, self.y), self.radius)


def draw_block_of_enemies():
    x = 20
    y = 20
    for j in range(len(enemy)):
        for i in range(len(enemy[j])):
            enemy[j][i] = Enemy(x, y, 60, 60, i*60, screenWidth - 60*(10-i), True)
            x += 60
        x = 20
        y += 40
        i = 1

    return enemy

# for every foe check collision with projectiles on screen
def check_collison(foe):
    for projectile in projectiles:
        if  foe.x <= projectile.x <= foe.x + 60 and foe.status is True:
            if foe.y <= projectile.y <= foe.y + 40:
                projectiles.pop(projectiles.index(projectile))
                return False
    return True

# in every frame display all objects on their current positions
def redraw_game_window():
    win.blit(bg, (0, 0))
    player.draw(win)

    for bullet in projectiles:
        bullet.draw(win)

    for i in range(len(enemy)):
        for j in range(len(enemy[i])):
            if check_collison(enemy[i][j]) is True and enemy[i][j].status is True:
                enemy[i][j].draw(win)
            else:
                enemy[i][j].status = False

    pygame.display.update()


screenWidth = 1280
screenHeight = 800
win = pygame.display.set_mode((screenWidth, screenHeight))
pygame.display.set_caption("Space Invaders")
clock = pygame.time.Clock()

bg = pygame.image.load('img/sky.jpg')
player = Player(20, screenHeight - 80, 60, 60)
enemy = [[None]*10, [None]*10, [None]*10]
enemy = draw_block_of_enemies()
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
    if keys[pygame.K_LEFT] and player.x > player.vel:
        player.x -= player.vel
    elif keys[pygame.K_RIGHT] and player.x < screenWidth - player.width - player.vel:
        player.x += player.vel
    if keys[pygame.K_SPACE] and canShoot == 0:
        if len(projectiles) < 10:  # up to 10 projectiles on screen at the same moment
            projectiles.append(Projectile(round(player.x + player.width // 2),
                                          round(player.y + player.height // 2), 4, (255, 128, 0)))
        canShoot += 1

    redraw_game_window()

#End of game!
pygame.quit()
