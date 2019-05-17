import sys

import pygame
import Main
from model.Player import Player
from model.Enemy import Enemy
from model.SpecialEnemy import SpecialEnemy
from model.Life import Life


def description_of_game():
    res = True
    while res:
        Main.win.blit(Main.bg, (0, 0))

        font1 = pygame.font.SysFont('comicsans', 50)
        description = font1.render("Try to kill all of the aliens!", 1, Main.WHITE)
        Main.win.blit(description, ((Main.screenWidth - description.get_width()) / 2, 40))

        player = Player(30, 120, 60, 60)
        font2 = pygame.font.SysFont('comicsans', 40)
        description = font2.render("   -   your ship", 1, Main.WHITE)
        Main.win.blit(description, (80, 135))
        player.draw(Main.win)

        enemy1 = Enemy(30, 200, 60, 60, 0, 0)
        enemy2 = Enemy(90, 200, 60, 60, 0, 0)
        enemy3 = SpecialEnemy(150, 200, 60, 60, 0, 0, True)
        font3 = pygame.font.SysFont('comicsans', 40)
        description = font3.render(" -  aliens / enemies", 1, Main.WHITE)
        Main.win.blit(description, (230, 220))
        enemy1.draw_1(Main.win)
        enemy2.draw_2(Main.win)
        enemy3.draw(Main.win)

        life = Life(30, 290, 60, 60)
        font4 = pygame.font.SysFont('comicsans', 40)
        description = font4.render("   -   your health points", 1, Main.WHITE)
        Main.win.blit(description, (100, 300))
        life.draw(Main.win)

        font5 = pygame.font.SysFont('comicsans', 40)
        description = font5.render("Arrow left, Arrow right   -   move", 1, Main.WHITE)
        Main.win.blit(description, (30, 420))
        description = font5.render("Spacebar   -   shoot", 1, Main.WHITE)
        Main.win.blit(description, (30, 480))
        description = font5.render("P    -    pause", 1, Main.WHITE)
        Main.win.blit(description, (30, 540))
        description = font5.render("Esc    -    escape game / go back to menu", 1, Main.WHITE)
        Main.win.blit(description, (30, 600))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                res = False
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            res = False

        pygame.display.update()
