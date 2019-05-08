from model.Enemy import Enemy
import Main


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
