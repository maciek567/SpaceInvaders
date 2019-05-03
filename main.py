import pygame
import random
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

    def hit(self):
        explosion.play()
        self.health -= 1
        self.killed = True
        self.timeToRecover = 60

    def is_player_hit(self, enemy_projectiles):
        for enemy_projectile in enemy_projectiles:
            if self.x <= enemy_projectile.x <= self.x + 60 and self.killed is False:
                if self.y <= enemy_projectile.y <= self.y + 60:
                    enemy_projectiles.pop(enemy_projectiles.index(enemy_projectile))
                    self.hit()


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
        self.vel = 2
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

    # for every foe check collision with projectiles on screen
    def check_collison(foe, projectiles):
        for projectile in projectiles:
            if foe.x <= projectile.x <= foe.x + 60 and foe.status is True:
                if foe.y <= projectile.y <= foe.y + 40:
                    invaderKilled.play()
                    projectiles.pop(projectiles.index(projectile))
                    return False
        return True


class Projectile(object):
    def __init__(self, x, y, radius, color):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.vel = 8  # velocity of bullet

    def draw(self, win):
        pygame.draw.circle(win, self.color, (self.x, self.y), self.radius)


def draw_block_of_enemies(enemy):
    x = 20
    y = 60
    for j in range(len(enemy)):
        for i in range(len(enemy[j])):
            enemy[j][i] = Enemy(x, y, 60, 60, i*60, screenWidth - 60*(10-i), True)
            x += 60
        x = 20
        y += 40
        i = 1
    return enemy


# in every frame display all objects on their current positions
def redraw_game_window(player, enemy, projectiles, enemy_projectiles):
    win.blit(bg, (0, 0))
    player.draw(win)

    for bullet in projectiles:
        bullet.draw(win)

    for enemy_bullet in enemy_projectiles:
        enemy_bullet.draw(win)
        player.is_player_hit(enemy_projectiles)

    for i in range(len(enemy)):
        for j in range(len(enemy[i])):
            if Enemy.check_collison(enemy[i][j], projectiles) is True and enemy[i][j].status is True:
                enemy[i][j].draw(win)
            else:
                enemy[i][j].status = False

    if player.health < 1:
        game_over()

    pygame.display.update()


def button(message, x, y, w, h, color, mouse_hover, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    font = pygame.font.SysFont("comicsansms", 40)
    text = font.render(message, 1, color)

    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        pygame.draw.rect(win, mouse_hover, (x, y, text.get_width(), h))
        if click[0] == 1 and action is not None:
            action()

    win.blit(text, (x, y))


def quit_game():
    pygame.quit()


def menu():
    intro = True
    pygame.mixer.music.stop()
    win.blit(bg, (0, 0))
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        win.blit(bg, (0, 0))
        font1 = pygame.font.SysFont('comicsans', 100)
        title = font1.render("Space Invaders", 1, WHITE)
        win.blit(title, ((screenWidth - title.get_width()) / 2, screenHeight / 5))

        button_width = 200
        button_height = 50
        button("Play", (screenWidth - button_width) / 2, screenHeight * 2/5, button_width, button_height, WHITE, GRAY, main_loop)
        button("Options", (screenWidth - button_width) / 2, screenHeight * 2.5/5, button_width, button_height, WHITE, GRAY)
        button("High scores", (screenWidth - button_width) / 2, screenHeight * 3 / 5, button_width, button_height, WHITE, GRAY)
        button("Quit", (screenWidth - button_width) / 2, screenHeight * 3.5/5, button_width, button_height,  WHITE, GRAY, quit_game)

        pygame.display.update()


def game_over():
    game_over_text = True
    pygame.mixer.music.stop()

    font1 = pygame.font.SysFont('comicsans', 200)
    title = font1.render("Game over!", 1, RED)
    win.blit(title, ((screenWidth - title.get_width()) / 2, screenHeight / 3))

    font2 = pygame.font.SysFont('comicsans', 80)
    description = font2.render("Press space to continue", 1, GREEN)
    win.blit(description, ((screenWidth - description.get_width()) / 2, screenHeight / 2))

    pygame.display.update()

    while game_over_text:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            game_over_text = False
            menu()


def main_loop():

    # Ship can shoot only if this variable is equal to 0. After every successful shoot this variable is incremented,
    # and if reaches 10, then is reduced again to 0. This feature prevent from shooting all projectiles at once
    # which can cause undesirable blurred trail on screen
    can_shoot = 0
    frequency_of_alien_shooting = 50
    player = Player(20, screenHeight - 80, 60, 60)
    enemy = [[None] * 10, [None] * 10, [None] * 10]
    enemy = draw_block_of_enemies(enemy)
    projectiles = []
    enemy_projectiles = []
    pygame.mixer.music.rewind()
    pygame.mixer.music.play()

    run = True
    while run:
        enemy_shot = random.randint(1, frequency_of_alien_shooting)
        enemy_x = random.randint(0, 9)
        enemy_y = random.randint(0, 2)
        clock.tick(30)  # fps

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        if can_shoot > 0:
            can_shoot += 1
        if can_shoot >= 20:
            can_shoot = 0

        # display projectiles until they reach top border of screen
        # if projectile reaches top border of screen remove it from array so that ship could shoot next ones
        for projectile in projectiles:
            if 0 < projectile.y > 0:
                projectile.y -= projectile.vel
            else:
                projectiles.pop(projectiles.index(projectile))

        for enemy_projectile in enemy_projectiles:
            if 0 < enemy_projectile.y > 0:
                enemy_projectile.y += enemy_projectile.vel
            else:
                enemy_projectiles.pop(enemy_projectiles.index(enemy_projectile))

        if enemy_shot == 2 and enemy[enemy_y][enemy_x].status is True:
            enemy_projectiles.append(Projectile(round(enemy[enemy_y][enemy_x].x + enemy[enemy_y][enemy_x].width // 2),
                                                round(enemy[enemy_y][enemy_x].y + enemy[enemy_y][enemy_x].height // 2), 4, GREEN))
        elif enemy[enemy_y][enemy_x].status is False and frequency_of_alien_shooting > 10:
            frequency_of_alien_shooting -= 1

        # handle keys pressed by player (left arrow, right arrow, space)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player.x > player.vel and not player.killed:
            player.x -= player.vel
        elif keys[pygame.K_RIGHT] and player.x < screenWidth - player.width - player.vel and not player.killed:
            player.x += player.vel
        if keys[pygame.K_SPACE] and can_shoot == 0 and not player.killed:
            shoot.play()
            if len(projectiles) < 10:  # up to 10 projectiles on screen at the same moment
                projectiles.append(Projectile(round(player.x + player.width // 2),
                                              round(player.y + player.height // 2), 4, (255, 128, 0)))

            can_shoot += 1
        if keys[pygame.K_ESCAPE]:
            run = False
            menu()

        redraw_game_window(player, enemy, projectiles, enemy_projectiles)


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (169, 169, 169)
GREEN = (0, 255, 0)
RED = (200, 0, 0)

screenWidth = 1280
screenHeight = 800
win = pygame.display.set_mode((screenWidth, screenHeight))
pygame.display.set_caption("Space Invaders")
clock = pygame.time.Clock()

bg = pygame.image.load('img/sky.jpg')
music = pygame.mixer.music.load('sounds/music1.wav')
shoot = pygame.mixer.Sound('sounds/shoot.wav')
invaderKilled = pygame.mixer.Sound('sounds/invaderKilled.wav')
explosion = pygame.mixer.Sound('sounds/explosion.wav')


menu()


# End of game!
pygame.quit()
