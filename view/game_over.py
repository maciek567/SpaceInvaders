import sys
import pygame
import Main
from view.scores import Scores


def game_over():

    game_over_text = True
    Main.LEVEL = 1
    pygame.mixer.music.stop()

    font1 = pygame.font.SysFont('comicsans', 200)
    title = font1.render("Game over!", 1, Main.RED)
    Main.win.blit(title, ((Main.screenWidth - title.get_width()) / 2, Main.screenHeight / 3.5))

    font2 = pygame.font.SysFont('comicsans', 100)
    description = font2.render("Your score: " + str(Main.SCORE), 1, Main.WHITE)
    Main.win.blit(description, ((Main.screenWidth - description.get_width()) / 2, Main.screenHeight / 2))

    font3 = pygame.font.SysFont('comicsans', 80)
    description = font3.render("Press space to continue", 1, Main.GREEN)
    Main.win.blit(description, ((Main.screenWidth - description.get_width()) / 2, Main.screenHeight / 1.5))

    scores = Scores()
    scores.save_score(['Player', str(Main.SCORE)])

    Main.SCORE = 0
    pygame.display.update()

    while game_over_text:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            game_over_text = False
            from Main.main import menu
            menu()
