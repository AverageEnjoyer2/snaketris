import pygame as pg
import random
import sys
from pygame.locals import *

fps = 25
w, h = 600, 500
blocksize = 20 #  размер одного блока
side = int((w - 20 * blocksize) / 2)
top = h - (10 * blocksize) - 5
#  все тетрамино
tetraminos = [[['00100',
                '00100',
                '01100',
                '00000',
                '00000'], ['01100',
                           '00100',
                           '00100',
                           '00000',
                           '00000']], [['01110',
                                        '00010',
                                        '00000',
                                        '00000',
                                        '00000'], ['00010',
                                                   '01110',
                                                   '00000',
                                                   '00000',
                                                   '00000']], [['00110',
                                                                '00100',
                                                                '00100',
                                                                '00000',
                                                                '00000'], ['00100',
                                                                           '00100',
                                                                           '00110',
                                                                           '00000',
                                                                           '00000']], [['00100',
                                                                                        '00111',
                                                                                        '00000',
                                                                                        '00000',
                                                                                        '00000'], ['11100',
                                                                                                   '10000',
                                                                                                   '00000',
                                                                                                   '00000',
                                                                                                   '00000']],
              [['00110',
                '01100',
                '00000',
                '00000',
                '00000'],
               ['01100',
                '00110',
                '00000',
                '00000',
                '00000']],
              [['00100',
                '00110',
                '00010',
                '00000',
                '00000'],
               ['00100',
                '01100',
                '01000',
                '00000',
                '00000']],
              [['01110',
                '00100',
                '00000',
                '00000',
                '00000'],
               ['00100',
                '01110',
                '00000',
                '00000',
                '00000']],
              [['00100',
                '00110',
                '00100',
                '00000',
                '00000'],
               ['00010',
                '00110',
                '00010',
                '00000',
                '00000']],
              [['00100',
                '00100',
                '00100',
                '00100',
                '00000'],
               ['01111',
                '00000',
                '00000',
                '00000',
                '00000']],
              [['00110',
                '00110',
                '00000',
                '00000',
                '00000'],
               ['00110',
                '00110',
                '00000',
                '00000',
                '00000']]
              ]

colors = ("blue", "green", "red", "yellow")







def drawBlock(block_x, block_y, color, pixelx=None, pixely=None): #  отрисовка блока
    if color == "0":
        return
    pg.draw.rect(screen, color, (pixelx + 1, pixely + 1, blocksize - 1, blocksize - 1), 0, 3)

def drawTetra(index=-1, pixelx=w-150, pixely=230, rotated=False):  # отрисовка тетрамино
    print("a")
    if index < 0:
        tetramino = random.choice(tetraminos)  # Случайное тетрамино
    else:
        tetramino = tetraminos[index] # прописанное тетрамино
    color = random.choice(colors)
    number = 0
    if rotated:  # проверка наклона
        number += 1

    for x in range(5):
        for y in range(5):
            if tetramino[number][y][x] != "0":
                drawBlock(None, None, color, pixelx + (x * blocksize), pixely + (y * blocksize))
    return tetraminos.index(tetramino)





if __name__ == '__main__':
    global fps_clock, screen, basic_font, big_font
    pg.init()
    fps_clock = pg.time.Clock()
    screen = pg.display.set_mode((w, h))
    running = True
    print("huh")
    tetradrawn = False
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT: # выход из игры
                running = False
            elif event.type == pg.KEYUP:
                if event.key == K_SPACE:
                    screen.fill("black")
                    tetra = drawTetra()  # отрисовка нового тетамино
                elif event.key == pg.K_a:
                    screen.fill("black")
                    tetra = drawTetra(index=tetra, rotated=True)  # Поворот тетрамино в одну сторону
                elif event.key == pg.K_d:
                    screen.fill("black")
                    tetra = drawTetra(index=tetra)  # Поворот тетрамино в другую сторону

        if not tetradrawn:
            tetra = drawTetra()
            tetradrawn = True
        pg.display.update()
    pg.quit()
    sys.exit()
