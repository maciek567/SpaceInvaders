import sys
import pygame
import Main


def you_win():

    win = True
    Main.LEVEL += 1

    # if level == 11
    #   end game with congratulation and show some credits

    font1 = pygame.font.SysFont('comicsans', 200)
    title = font1.render("Victory!", 1, Main.RED)
    Main.win.blit(title, ((Main.screenWidth - title.get_width()) / 2, Main.screenHeight / 3.5))

    font2 = pygame.font.SysFont('comicsans', 100)
    description = font2.render("Your score: " + str(Main.SCORE), 1, Main.WHITE)
    Main.win.blit(description, ((Main.screenWidth - description.get_width()) / 2, Main.screenHeight / 2))

    font3 = pygame.font.SysFont('comicsans', 80)
    description = font3.render("Press enter to move to level " + str(Main.LEVEL), 1, Main.GREEN)
    Main.win.blit(description, ((Main.screenWidth - description.get_width()) / 2, Main.screenHeight / 1.5))

    # Main.SCORE = 0
    pygame.display.update()

    while win:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN]:
            win = False
            from Main.main import main_loop
            main_loop()
