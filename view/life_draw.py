from model.Life import Life
import Main


def life_draw(life):
    x = Main.screenWidth - 300
    y = 10
    for i in range(3):
        life[i] = Life(x, y, 100, 100)
        x -= 70
    return life
