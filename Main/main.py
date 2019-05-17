import sys
import pygame
import random
import Main
from model.Player import Player
from model.Projectile import Projectile
from model.SpecialEnemy import SpecialEnemy
from view.game_over import game_over
from view.object_draw import draw_block_of_enemies
from view.life_draw import life_draw
from view.next_level import you_win
from view.description import description_of_game
from view.scores import Scores
pygame.init()


def button(message, x, y, w, h, color, mouse_hover, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    flag = True

    font = pygame.font.SysFont("comicsansms", 40)
    text = font.render(message, 1, color)

    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        pygame.draw.rect(Main.win, mouse_hover, (x, y, text.get_width(), h))
        if click[0] == 1 and action is not None:
            if action == "main_loop":
                main_loop()
            elif action == "quit_game":
                pygame.quit()
                sys.exit()
            elif action == "description":
                description_of_game()
            elif action == "high_scores":
                scores = Scores()
                scores.show_high_scores()

    if flag is True:
        Main.win.blit(text, (x, y))
    return flag


# in every frame display all objects on their current positions
def redraw_game_window(player, enemy, special_alien, projectiles, enemy_projectiles, lives, alive):

    Main.win.blit(Main.bg, (0, 0))
    player.draw(Main.win)

    for bullet in projectiles:
        bullet.draw(Main.win)

    for enemy_bullet in enemy_projectiles:
        enemy_bullet.draw(Main.win)
        player.is_player_hit(enemy_projectiles)

    for i in range(len(enemy)):
        for j in range(len(enemy[i])):
            if enemy[i][j].check_collision(projectiles) is True and enemy[i][j].status is True:
                enemy[i][j].draw(Main.win)
            else:
                enemy[i][j].status = False
                alive -= 1

    if alive < 1:
        you_win()
    else:
        life_count = player.health
        for life in lives:
            life.draw(Main.win)
            life_count -= 1
            if life_count < 1:
                break

        if special_alien.check_collision(projectiles) is True and special_alien.status is True:
            special_alien.draw(Main.win)
        else:
            special_alien.status = False

        # display score
        score = pygame.font.SysFont('comicsans', 50)
        description = score.render("Score: " + str(Main.SCORE), 1, Main.WHITE)
        Main.win.blit(description, (Main.screenWidth - description.get_width() - 20, 20))

        # display level
        level = pygame.font.SysFont('comicsans', 50)
        lvl_description = level.render("Level: " + str(Main.LEVEL), 1, Main.WHITE)
        Main.win.blit(lvl_description, (20, 20))

    if player.health < 1:
        game_over()

    pygame.display.update()


def menu():
    intro = True
    pygame.mixer.music.stop()
    Main.win.blit(Main.bg, (0, 0))
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        Main.win.blit(Main.bg, (0, 0))
        font1 = pygame.font.SysFont('comicsans', 100)
        title = font1.render("Space Invaders", 1, Main.YELLOW)
        Main.win.blit(title, ((Main.screenWidth - title.get_width()) / 2, Main.screenHeight / 5))

        button_width = 200
        button_height = 50
        button("Play", (Main.screenWidth - button_width) / 2, Main.screenHeight * 2/5, button_width, button_height, Main.WHITE, Main.GRAY, "main_loop")
        button("Description", (Main.screenWidth - button_width) / 2, Main.screenHeight * 2.5/5, button_width, button_height, Main.WHITE, Main.GRAY, "description")
        button("High scores", (Main.screenWidth - button_width) / 2, Main.screenHeight * 3 / 5, button_width, button_height, Main.WHITE, Main.GRAY, "high_scores")
        intro = button("Quit", (Main.screenWidth - button_width) / 2, Main.screenHeight * 3.5/5, button_width, button_height,  Main.WHITE, Main.GRAY, "quit_game")

        pygame.display.update()


def main_loop():

    # Ship can shoot only if this variable is equal to 0. After every successful shoot this variable is incremented,
    # and if reaches 10, then is reduced again to 0. This feature prevent from shooting all projectiles at once
    # which can cause undesirable blurred trail on screen
    pygame.display.update()

    number = random.randint(1, 5)

    Main.bg = pygame.image.load('../model/img/big_sky' + str(number) + '.jpg')
    can_shoot = 0
    frequency_of_alien_shooting = 111 - Main.LEVEL * 10
    player = Player(20, Main.screenHeight - 100, 60, 60)
    enemy = [[None] * 10, [None] * 10, [None] * 10]
    alive = len(enemy) * len(enemy[0])
    enemy = draw_block_of_enemies(enemy)
    special_alien = SpecialEnemy(0, 60, 60, 60, 0, Main.screenWidth, False)
    lives = [None, None, None]
    lives = life_draw(lives)
    projectiles = []
    enemy_projectiles = []
    pygame.mixer.music.rewind()
    pygame.mixer.music.play()

    run = True
    paused = False
    while run:
        special = random.randint(1, 500)
        if special == 10 and Main.SPECIAL == 0:
            special_alien.status = True
            Main.SPECIAL += 1
        if special_alien.status is False and Main.SPECIAL == 1:
            Main.SPECIAL = 0
            special_alien = SpecialEnemy(0, 60, 60, 60, 0, Main.screenWidth, False)

        enemy_shot = random.randint(1, frequency_of_alien_shooting)
        enemy_x = random.randint(0, 9)
        enemy_y = random.randint(0, 2)
        Main.clock.tick(30)  # fps

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                pygame.mixer.music.stop()
                sys.exit()

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
                                                round(enemy[enemy_y][enemy_x].y + enemy[enemy_y][enemy_x].height // 2),
                                                4, Main.GREEN))
        elif enemy[enemy_y][enemy_x].status is False and frequency_of_alien_shooting > 10:
            frequency_of_alien_shooting -= 1

        # handle keys pressed by player (left arrow, right arrow, space)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player.x > player.vel and not player.killed:
            player.x -= player.vel
        elif keys[pygame.K_RIGHT] and player.x < Main.screenWidth - player.width - player.vel and not player.killed:
            player.x += player.vel
        if keys[pygame.K_SPACE] and can_shoot == 0 and not player.protection:
            Main.shoot.play()
            if len(projectiles) < 10:  # up to 10 projectiles on screen at the same moment
                projectiles.append(Projectile(round(player.x + player.width // 2),
                                              round(player.y + player.height // 2), 4, (255, 128, 0)))

            can_shoot += 1
        if keys[pygame.K_ESCAPE]:
            run = False
            paused = True
            Main.SCORE = 0
            Main.LEVEL = 1
            Player.health = 3
            menu()
        if keys[pygame.K_p]:
            if paused is False:
                paused = True
            else:
                paused = False

        if paused is False:
            redraw_game_window(player, enemy, special_alien, projectiles, enemy_projectiles, lives, alive)


menu()
