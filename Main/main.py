import pygame
import random
from model.Player import Player
from model.Enemy import Enemy
from model.Projectile import Projectile
import Main
pygame.init()


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


def you_win():
    game_over_text = True

    font1 = pygame.font.SysFont('comicsans', 200)
    title = font1.render("Victory!", 1, Main.RED)
    win.blit(title, ((Main.screenWidth - title.get_width()) / 2, Main.screenHeight / 3.5))

    font2 = pygame.font.SysFont('comicsans', 100)
    description = font2.render("Your score: " + str(Main.SCORE), 1, Main.WHITE)
    win.blit(description, ((Main.screenWidth - description.get_width()) / 2, Main.screenHeight / 2))

    font3 = pygame.font.SysFont('comicsans', 80)
    description = font3.render("Press space to continue", 1, Main.GREEN)
    win.blit(description, ((Main.screenWidth - description.get_width()) / 2, Main.screenHeight / 1.5))

    Main.SCORE = 0
    pygame.display.update()

    while game_over_text:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            game_over_text = False
            menu()


def game_over():
    game_over_text = True
    # pygame.mixer.music.stop()

    font1 = pygame.font.SysFont('comicsans', 200)
    title = font1.render("Game over!", 1, Main.RED)
    win.blit(title, ((Main.screenWidth - title.get_width()) / 2, Main.screenHeight / 3.5))

    font2 = pygame.font.SysFont('comicsans', 100)
    description = font2.render("Your score: " + str(Main.SCORE), 1, Main.WHITE)
    win.blit(description, ((Main.screenWidth - description.get_width()) / 2, Main.screenHeight / 2))

    font3 = pygame.font.SysFont('comicsans', 80)
    description = font3.render("Press space to continue", 1, Main.GREEN)
    win.blit(description, ((Main.screenWidth - description.get_width()) / 2, Main.screenHeight / 1.5))

    Main.SCORE = 0
    pygame.display.update()

    while game_over_text:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            game_over_text = False
            menu()


# in every frame display all objects on their current positions
def redraw_game_window(player, enemy, projectiles, enemy_projectiles):
    alive = len(enemy)*len(enemy[0])
    win.blit(bg, (0, 0))
    player.draw(win)

    for bullet in projectiles:
        bullet.draw(win)

    for enemy_bullet in enemy_projectiles:
        enemy_bullet.draw(win)
        player.is_player_hit(enemy_projectiles)

    for i in range(len(enemy)):
        for j in range(len(enemy[i])):
            if enemy[i][j].check_collison(projectiles) is True and enemy[i][j].status is True:   # Enemy.check_collison(enemy[i][j], projectiles)
                enemy[i][j].draw(win)
            else:
                enemy[i][j].status = False
                alive -= 1

    if alive < 1:
        you_win()
    else:
        # display score
        font = pygame.font.SysFont('comicsans', 50)
        description = font.render("Score: " + str(Main.SCORE), 1, Main.WHITE)
        win.blit(description, (Main.screenWidth - description.get_width() - 20, 20))

    if player.health < 1:
        game_over()

    pygame.display.update()


def draw_block_of_enemies(enemy):
    x = 20
    y = 60
    for j in range(len(enemy)):
        for i in range(len(enemy[j])):
            enemy[j][i] = Enemy(x, y, 60, 60, i*60, Main.screenWidth - 60*(10-i), True)
            x += 60
        x = 20
        y += 40
    return enemy


def quit_game():
    pygame.quit()


def menu():
    intro = True
    # pygame.mixer.music.stop()
    win.blit(bg, (0, 0))
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                intro = False
                pygame.quit()

        if intro:
            win.blit(bg, (0, 0))
            font1 = pygame.font.SysFont('comicsans', 100)
            title = font1.render("Space Invaders", 1, Main.WHITE)
            win.blit(title, ((Main.screenWidth - title.get_width()) / 2, Main.screenHeight / 5))

            button_width = 200
            button_height = 50
            button("Play", (Main.screenWidth - button_width) / 2, Main.screenHeight * 2/5, button_width, button_height, Main.WHITE, Main.GRAY, main_loop)
            button("Options", (Main.screenWidth - button_width) / 2, Main.screenHeight * 2.5/5, button_width, button_height, Main.WHITE, Main.GRAY)
            button("High scores", (Main.screenWidth - button_width) / 2, Main.screenHeight * 3 / 5, button_width, button_height, Main.WHITE, Main.GRAY)
            button("Quit", (Main.screenWidth - button_width) / 2, Main.screenHeight * 3.5/5, button_width, button_height,  Main.WHITE, Main.GRAY, quit_game)

            pygame.display.update()


def main_loop():

    # Ship can shoot only if this variable is equal to 0. After every successful shoot this variable is incremented,
    # and if reaches 10, then is reduced again to 0. This feature prevent from shooting all projectiles at once
    # which can cause undesirable blurred trail on screen
    can_shoot = 0
    frequency_of_alien_shooting = 50
    player = Player(20, Main.screenHeight - 80, 60, 60)
    enemy = [[None] * 10, [None] * 10, [None] * 10]
    enemy = draw_block_of_enemies(enemy)
    projectiles = []
    enemy_projectiles = []
    # pygame.mixer.music.rewind()
    # pygame.mixer.music.play()

    run = True
    paused = False
    while run:
        enemy_shot = random.randint(1, frequency_of_alien_shooting)
        enemy_x = random.randint(0, 9)
        enemy_y = random.randint(0, 2)
        clock.tick(30)  # fps

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                # pygame.mixer.music.stop()

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
                                                round(enemy[enemy_y][enemy_x].y + enemy[enemy_y][enemy_x].height // 2), 4, Main.GREEN))
        elif enemy[enemy_y][enemy_x].status is False and frequency_of_alien_shooting > 10:
            frequency_of_alien_shooting -= 1

        # handle keys pressed by player (left arrow, right arrow, space)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player.x > player.vel and not player.killed:
            player.x -= player.vel
        elif keys[pygame.K_RIGHT] and player.x < Main.screenWidth - player.width - player.vel and not player.killed:
            player.x += player.vel
        if keys[pygame.K_SPACE] and can_shoot == 0 and not player.killed:
            # shoot.play()
            if len(projectiles) < 10:  # up to 10 projectiles on screen at the same moment
                projectiles.append(Projectile(round(player.x + player.width // 2),
                                              round(player.y + player.height // 2), 4, (255, 128, 0)))

            can_shoot += 1
        if keys[pygame.K_ESCAPE]:
            run = False
            menu()
        if keys[pygame.K_p]:
            if paused is False:
                paused = True
            else:
                paused = False

        if paused is False:
            redraw_game_window(player, enemy, projectiles, enemy_projectiles)


win = pygame.display.set_mode((Main.screenWidth, Main.screenHeight))
pygame.display.set_caption("Space Invaders")
clock = pygame.time.Clock()
bg = pygame.image.load('model/img/sky.jpg')

# music = pygame.mixer.music.load('sounds/music1.wav')
# shoot = pygame.mixer.Sound('sounds/shoot.wav')
# invaderKilled = pygame.mixer.Sound('sounds/invaderKilled.wav')
# explosion = pygame.mixer.Sound('sounds/explosion.wav')

menu()

# End of game!
pygame.quit()
