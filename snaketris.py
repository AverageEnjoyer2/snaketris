import pygame as pg
import random
import sys
from pygame.locals import *
from random import choice

fps = 25
w, h = 600, 500
blocksize = 20 #  размер одного блока
side = int((w - 20 * blocksize) / 2)
square_h = 20
sqare_w = 10
top = h - (10 * blocksize) - 5
#  все тетрамино
class Board:  # класс клеточной сетки, применялся мною раньше для решения задач
    # создание поля
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = [[0] * width for _ in range(height)]
        # значения по умолчанию
        self.left = 80
        self.top = 200
        self.cell_size = blocksize
        self.cells = []
        self.first_column = []

    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def render(self, screen):
        self.cells = []
        for i in range(self.height):
            for j in range(self.width):
                pg.draw.rect(screen, "white", (self.cell_size * j + self.top, self.cell_size * i + self.left,
                                                   self.cell_size, self.cell_size), 1)
                self.cells.append([i, j, self.cell_size * j + self.top, self.cell_size * i + self.left])
                if i == 0:
                    self.first_column.append([i, j, self.cell_size * j + self.top, self.cell_size * i + self.left])

    def get_cell(self, cords):
        for cell in self.cells:
            if cell[2] < cords[0] < cell[2] + self.cell_size and cell[3] < cords[1] < cell[3] + self.cell_size:
                return [cell[0], cell[1]]
        return "None"

    def on_click(self, cell):
        if cell != "None":
            print(f"({cell[0]}, {cell[1]})")
        else:
            print(cell)

    def get_click(self, mouse_pos):
        cell = self.get_cell(mouse_pos)
        self.on_click(cell)
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







def drawBlock(color, pixelx=None, pixely=None): #  отрисовка блока
    if color == "0":
        return
    pg.draw.rect(screen, color, (pixelx + 1, pixely + 1, blocksize - 1, blocksize - 1), 0, 3)
    return [pixelx + 1, pixely + 1]

def drawTetra(index=-1, pixelx=w-150, pixely=230, rotated=False, color="nocolor"):  # отрисовка тетрамино
    if index < 0:
        tetramino = random.choice(tetraminos)  # Случайное тетрамино
    else:
        tetramino = tetraminos[index] # прописанное тетрамино
    if color == "nocolor":  #  проверка, прописан ли цвет
        color = random.choice(colors)  #  случайный цвет
    number = 0
    if rotated:  # проверка наклона
        number += 1
    blcoks = []

    for x in range(5):
        for y in range(5):
            if tetramino[number][y][x] != "0":
                block = drawBlock(color, pixelx + (x * blocksize), pixely + (y * blocksize))
                blcoks.append(block)
    return [tetraminos.index(tetramino), color, blcoks]





if __name__ == '__main__':
    global fps_clock, screen, basic_font, big_font
    pg.init()
    fps_clock = pg.time.Clock()
    screen = pg.display.set_mode((w, h))
    running = True
    tetradrawn = False
    board = Board(sqare_w, square_h)
    board.render(screen)
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT: # выход из игры
                running = False
            elif event.type == pg.KEYUP:
                if event.key == K_SPACE:
                    cell = choice(board.first_column)
                    while True:
                        wrongcells = 0
                        screen.fill("black")
                        board.render(screen)
                        tetramino = drawTetra(pixelx=(cell[2] - blocksize * 2), pixely=cell[3])
                        tetra, tetracolor, tblcoks = tetramino[0], tetramino[1], tetramino[2]  # отрисовка нового тетамино в случайном месте в верхних колоннах сетки
                        for block in tblcoks:  # проверяем, не вылезают ли блоки за сетку
                            if board.get_cell([block[0], block[1]]) == "None":
                                wrongcells += 1
                        if wrongcells == 0:
                            break
                elif event.key == pg.K_a:
                    try:
                        screen.fill("black")
                        board.render(screen)
                        tetramino = drawTetra(index=tetra, rotated=True, color=tetracolor, pixelx=(cell[2] - blocksize * 2),
                                              pixely=cell[3])  # Поворот тетрамино в одну сторону
                        tetra, tetracolor, tblcoks = tetramino[0], tetramino[1], tetramino[2]
                        for block in tblcoks:  # Если при повороте тетрамино уходит за пределы сетки, возвращаем старую
                            if board.get_cell([block[0], block[1]]) == "None":
                                screen.fill("black")
                                board.render(screen)
                                tetramino = drawTetra(index=tetra, color=tetracolor,
                                                      pixelx=(cell[2] - blocksize * 2),
                                                      pixely=cell[3])
                                tetra, tetracolor, tblcoks = tetramino[0], tetramino[1], tetramino[2]
                    except NameError:
                        pass

                elif event.key == pg.K_d:
                    try:
                        screen.fill("black")
                        board.render(screen)
                        tetramino = drawTetra(index=tetra, color=tetracolor, pixelx=(cell[2] - blocksize * 2),
                                              pixely=cell[3])  # Поворот тетрамино в другую сторону
                        tetra, tetracolor, tblcoks = tetramino[0], tetramino[1], tetramino[2]
                    except NameError:
                        pass


        pg.display.update()
    pg.quit()
    sys.exit()
