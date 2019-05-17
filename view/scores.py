import csv
import sys
import pygame
import Main


class Scores(object):
    def __init__(self):
        self.list_of_scores = []
        Scores.read_scores(self)

    def show_high_scores(self):
        loop = True
        while loop:
            Main.win.blit(Main.bg, (0, 0))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            keys = pygame.key.get_pressed()
            if keys[pygame.K_ESCAPE]:
                loop = False

            font1 = pygame.font.SysFont('comicsans', 100)
            title = font1.render("High scores:", 1, Main.WHITE)
            Main.win.blit(title, ((Main.screenWidth - title.get_width()) / 2, Main.screenHeight / 10))

            score_number = 1
            font2 = pygame.font.SysFont('comicsans', 50)
            for record in self.list_of_scores:
                player = font2.render(record[0], 1, Main.WHITE)
                score = font2.render(record[1], 1, Main.YELLOW)
                Main.win.blit(player, ((Main.screenWidth - title.get_width()) / 2, Main.screenHeight * ((3+score_number)/15)))
                Main.win.blit(score, (Main.screenWidth / 2, Main.screenHeight * ((3 + score_number) / 15)))
                score_number += 1

            pygame.display.update()

    def save_score(self, record):
        self.list_of_scores.append(record)
        self.list_of_scores.sort(key=lambda record: int(record[1]), reverse=True)
        self.list_of_scores.pop(10)
        self.write_scores()

    def read_scores(self):
        with open('../view/high_scores.csv') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            for row in csv_reader:
                player_and_score = [row[0], row[1]]
                self.list_of_scores.append(player_and_score)

    def write_scores(self):
        with open('../view/high_scores.csv', mode="w", newline='') as csv_file:
            csv_files = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
            for record in self.list_of_scores:
                csv_files.writerow([record[0], record[1]])
