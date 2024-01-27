# Это не финальная версия проекта, не оценивайте пожалуйста. Спасибо
import pygame as pg
import random
import sys
from pygame.locals import *
from random import choice
import os

fps = 25
w, h = 600, 500
blocksize = 20  # размер одного блока
side = int((w - 20 * blocksize) / 2)
square_h = 20
sqare_w = 10
top = h - (10 * blocksize) - 5


def load_image(name): # Функция загрузки изображения
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pg.image.load(fullname)
    return image

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
        self.tetraminos = []  # список для упадших тетрамино
        self.score = 0
        self.scoretext = f"Очки:{self.score}"
        self.font = pg.font.SysFont('comic', 50)
        self.display_score = pg.display.set_mode((w, h))
        self.fontcolor = "red"
        self.snake = []

    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def render(self, screen):
        screen.fill("black")
        textSurf = self.font.render(self.scoretext, True, self.fontcolor)
        textRect = textSurf.get_rect()
        textRect.topleft = (w - 150, 180)
        self.display_score.blit(textSurf, textRect)
        self.cells = []
        self.tetraminos = []
        self.score = 0
        self.scoretext = f"Очки:{self.score}"
        self.snake = []
        for i in range(self.height):
            for j in range(self.width):
                pg.draw.rect(screen, "white", (self.cell_size * j + self.top, self.cell_size * i + self.left,
                                               self.cell_size, self.cell_size), 1)
                self.cells.append([i, j, self.cell_size * j + self.top, self.cell_size * i + self.left, "empty"])
                if i == 0:
                    self.first_column.append(
                        [i, j, self.cell_size * j + self.top, self.cell_size * i + self.left, "empty"])
        # for cell in self.cells[(board.width * board.height) // 2]
        for i in range(4):
            snakecell = self.cells[(board.width * board.height) // 2 + (board.width // 2) - 2 + i]
            snakecell[-1] = "dark green"
            self.cells[(board.width * board.height) // 2 + (board.width // 2) - 2 + i] = snakecell
            pg.draw.rect(screen, snakecell[-1],
                         (self.cell_size * snakecell[1] + self.top, self.cell_size * snakecell[0] + self.left,
                          self.cell_size, self.cell_size), 0)
            if i == 0:
                self.snake.append([snakecell, "none"])
            else:
                self.snake.append(snakecell)
        try:
            self.spawnspinblock()
        except NameError:
            pass


    def rerender(self, screen):
        screen.fill("black")
        try:
            fon = pg.transform.scale(load_image('background.png'), (w, h))
            screen.blit(fon, (0, 0))
            pic = pg.transform.scale(load_image(animationframe), (200, 300))
            screen.blit(pic, (400, 300))
            pg.draw.rect(screen, "darkblue", (self.top, self.left * board.width // 10,
                                          self.cell_size * self.width, self.cell_size * self.height), 1)
            nextSurf = self.font.render(self.scoretext, True, self.fontcolor)
            nextRect = nextSurf.get_rect()
            nextRect.topleft = (w - 150, 180)
            self.display_score.blit(nextSurf, nextRect)
            usedblocks = []
            for block in tblcoks:
                usedblocks.append([board.get_cell(block)[0], board.get_cell(block)[1]])
            for i in range(self.height):
                for j in range(self.width):
                    if board.cells[i * board.width + j][-1] == "empty" and [board.cells[i * board.width + j][0], board.cells[i * board.width + j][1]] not in usedblocks:
                        pass
                    elif [board.cells[i * board.width + j][0], board.cells[i * board.width + j][1]] in usedblocks:
                        pg.draw.rect(screen, tetracolor,
                                     (self.cell_size * j + self.top, self.cell_size * i + self.left,
                                      self.cell_size, self.cell_size), 0)
                    else:
                        pg.draw.rect(screen, board.cells[i * board.width + j][-1],
                                     (self.cell_size * j + self.top, self.cell_size * i + self.left,
                                      self.cell_size, self.cell_size), 0)
        except NameError:
            pass

    def get_cell(self, cords):
        for cell in self.cells:
            if cell[2] < cords[0] < cell[2] + self.cell_size and cell[3] < cords[1] < cell[3] + self.cell_size:
                return [cell[0], cell[1], self.cells.index(cell)]
        return "None"

    def on_click(self, cell):
        if cell != "None":
            print(f"({cell[0]}, {cell[1]})")
        else:
            print(cell)

    def get_click(self, mouse_pos):
        cell = self.get_cell(mouse_pos)
        self.on_click(cell)

    def check_completion(self):  # Проверка, есть ли заполненные ряды
        emptycells = 0
        cellnum = 0
        cleared = 0
        for cell in self.cells:
            if emptycells == 0 and cellnum == (self.width - 1):
                cleared += 1
                for rowcell in self.cells[cell[0] * self.width:cell[0] * self.width + self.width]:
                    del rowcell[-1]
                    rowcell.append("empty")
                    for placedtetramino in self.tetraminos:
                        for placedblock in placedtetramino:
                            if self.cells.index(rowcell) == placedblock[2]:
                                if len(placedtetramino) == 1:
                                    del self.tetraminos[self.tetraminos.index(placedtetramino)]
                                else:
                                    del placedtetramino[placedtetramino.index(placedblock)]
                self.rerender(screen)
            if cell[-1] == "empty" or cell[-1] == "darkgreen": # Если клетка пустая, то ряд не заполнен
                emptycells += 1
            if cellnum == (self.width - 1):  # С каждым рядо обновляем число незаролненных клеток
                cellnum = 0
                emptycells = 0
            else:
                cellnum += 1
        for placedtetramino in self.tetraminos:  # Разбиваем тетрамино на 2, если между его блоками нет связи
            if len(placedtetramino) > 0:
                placedtetramino.sort(key=lambda x: int(x[0]))
                row = placedtetramino[0][0]
                tetramino1 = []
                tetramino2 = []
                for placedblock in placedtetramino[1:]:
                    if placedblock[0] - 1 != row and placedblock[0] != row:
                        tetramino1 = placedtetramino[:placedtetramino.index(placedblock)]
                        tetramino2 = placedtetramino[placedtetramino.index(placedblock):]
                        break
                    else:
                        row = placedblock[0]
                if tetramino1:
                    del self.tetraminos[self.tetraminos.index(placedtetramino)]
                    self.tetraminos.append(tetramino1)
                    self.tetraminos.append(tetramino2)
        moved = 1
        while moved > 0:  # Сдвигаем тетрамино, которые можно сдвинуть вниз вниз, пока таких не останется
            moved = 0
            for placedtetramino in self.tetraminos:
                nospacebelow = 0
                try:
                    for placedblock in placedtetramino:  # Проверка для каждого блока, есть ли над ним пространство
                        blockinfo = [self.cells[placedblock[2] + self.width][0],
                                     self.cells[placedblock[2] + self.width][1],
                                     placedblock[2] + self.width]
                        if placedblock[2] + self.width > len(self.cells):
                            nospacebelow += 1
                        else:
                            if self.cells[placedblock[2] + self.width][-1] != "empty" and blockinfo not in placedtetramino:  # Проверяем, заполнена ли клетка под блоком
                                nospacebelow += 1
                except IndexError:  # Если блок в последнем ряду, его нельзя сдвинуть
                    nospacebelow += 1
                if nospacebelow == 0:  # Если под всеми блоками пустое пространство, двигаем тетрамино
                    moved += 1
                    for placedblock in reversed(placedtetramino):
                        del self.cells[placedblock[2] + self.width][-1]
                        self.cells[placedblock[2] + self.width].append(self.cells[placedblock[2]][-1])
                        del self.cells[placedblock[2]][-1]
                        self.cells[placedblock[2]].append("empty")
                        placedtetramino[placedtetramino.index(placedblock)][0] = int(
                            int(placedtetramino[placedtetramino.index(placedblock)][0]) + 1)
                        placedtetramino[placedtetramino.index(placedblock)][2] = int(
                            int(placedtetramino[placedtetramino.index(placedblock)][2]) + self.width)
        if cleared > 0:
            self.score += 10 * cleared * cleared  # Увеличиваем очки с учётои механики комбо
            if cleared == 1:
                self.scoretext = f"Очки:{self.score}"
            else:  # Если есть комбо, упоминаем его в очках
                self.scoretext = f"Очки:{self.score}(Комбо:{cleared})!"
    def spawnspinblock(self):
        usedblocks = []
        for block in tblcoks:
            usedblocks.append([board.get_cell(block)[0], board.get_cell(block)[1]])
        while True:
            blockcell = choice(self.cells)
            if blockcell[-1] == "empty" and [blockcell[0], blockcell[1]] not in usedblocks and blockcell[:-1] + ["darkgreen"] not in self.snake and blockcell[:-1] + ["darkgreen"] not in self.snake[0]:
                self.cells[self.cells.index(blockcell)][-1] = "purple"
                break
        self.rerender(screen)


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


def drawBlock(color, pixelx=None, pixely=None):  # отрисовка блока
    if color == "0":
        return
    pg.draw.rect(screen, color, (pixelx + 1, pixely + 1, blocksize - 1, blocksize - 1), 0, 3)
    return [pixelx + 1, pixely + 1]


def drawTetra(index=-1, pixelx=w - 150, pixely=230, rotated=False, color="nocolor"):  # отрисовка тетрамино
    if index < 0:
        tetramino = random.choice(tetraminos)  # Случайное тетрамино
    else:
        tetramino = tetraminos[index]  # прописанное тетрамино
    if color == "nocolor":  # проверка, прописан ли цвет
        color = random.choice(colors)  # случайный цвет
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


def snake_lose():
    global board, screen, cell, failed, rotate, lost, wrongcells, tetramino, blocksize, tetra, tetracolor, tblcoks
    board.render(screen)
    cell = choice(board.first_column)
    failed = True
    while True:
        rotate = choice([True, False])
        lost = False
        wrongcells = 0
        board.rerender(screen)
        tetramino = drawTetra(pixelx=(cell[2] - blocksize * 2), pixely=cell[3],
                              rotated=rotate)
        tetra, tetracolor, tblcoks = tetramino[0], tetramino[1], tetramino[2]
        # отрисовка нового тетамино в случайном месте в верхних колоннах сетки
        for block in tblcoks:  # проверяем, не вылезают ли блоки за сетку
            if board.get_cell([block[0], block[1]]) == "None":
                wrongcells += 1
            elif board.cells[int(board.get_cell([block[0], block[1]])[2])][
                -1] != "empty":
                lost = True
        if lost:  # Смотрим, произошёл ли проигрышб перезапускаем доску
            board.render(screen)
            break
        elif wrongcells == 0:
            break


v = 0
snake_v = 0
moved_down = False
cooldown = False
cooldown_v = 0
paused = False

if __name__ == '__main__':
    global fps_clock, screen, basic_font, big_font
    pg.init()
    startingscreen = True
    fps_clock = pg.time.Clock()
    screen = pg.display.set_mode((w, h))
    fon = pg.transform.scale(load_image('startbackground.png'), (w, h))
    screen.blit(fon, (0, 0))
    running = True
    instruction = False
    while startingscreen:
        pg.display.update()
        for event in pg.event.get():
            if event.type == pg.QUIT:  # выход из игры
                startingscreen = False
                running = False
            elif event.type == pg.KEYUP:
                if event.key == K_e and not instruction:
                    v_time = fps * 2
                    startingscreen = False
                elif event.key == K_n and not instruction:
                    v_time = fps
                    startingscreen = False
                elif event.key == K_h and not instruction:
                    v_time = fps // 2
                    startingscreen = False
                elif event.key == K_q:
                    if not instruction:
                        fon = pg.transform.scale(load_image('instructions_background.png'), (w, h))
                        screen.blit(fon, (0, 0))
                        instruction = True
                    else:
                        fon = pg.transform.scale(load_image('startbackground.png'), (w, h))
                        screen.blit(fon, (0, 0))
                        instruction = False
    tetradrawn = False
    board = Board(sqare_w, square_h)
    board.render(screen)
    animationframe = "frame1.png"
    anim_v = 0
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:  # выход из игры
                running = False
            elif event.type == pg.KEYUP:
                if event.key == K_i:
                    if paused:
                        paused = False
                    else:
                        paused = True
                if not paused:
                    if event.key == K_SPACE:
                        cell = choice(board.first_column)
                        while True:
                            rotate = choice([True, False])
                            lost = False
                            wrongcells = 0
                            board.rerender(screen)
                            tetramino = drawTetra(pixelx=(cell[2] - blocksize * 2), pixely=cell[3], rotated=rotate)
                            tetra, tetracolor, tblcoks = tetramino[0], tetramino[1], tetramino[2]
                            # отрисовка нового тетамино в случайном месте в верхних колоннах сетки
                            for block in tblcoks:  # проверяем, не вылезают ли блоки за сетку
                                if board.get_cell([block[0], block[1]]) == "None":
                                    wrongcells += 1
                                elif board.cells[int(board.get_cell([block[0], block[1]])[2])][-1] != "empty":
                                    lost = True
                            if lost:  # Смотрим, произошёл ли проигрышб перезапускаем доску
                                board.render(screen)
                                break
                            elif wrongcells == 0:
                                break
                    elif event.key == pg.K_r:
                        try:
                            board.rerender(screen)
                            tetramino = drawTetra(index=tetra, rotated=True, color=tetracolor,
                                                  pixelx=(cell[2] - blocksize * 2),
                                                  pixely=cell[3])  # Поворот тетрамино в одну сторону
                            rotate = True
                            tetra, tetracolor, tblcoks = tetramino[0], tetramino[1], tetramino[2]
                            for block in tblcoks:  # Если при повороте тетрамино уходит за пределы сетки, возвращаем старую
                                if (board.get_cell([block[0], block[1]]) == "None"
                                        or board.cells[int(board.get_cell([block[0], block[1]])[2])][-1] != "empty"):
                                    board.rerender(screen)
                                    rotate = False
                                    tetramino = drawTetra(index=tetra, color=tetracolor,
                                                          pixelx=(cell[2] - blocksize * 2),
                                                          pixely=cell[3], rotated=False)
                                    tetra, tetracolor, tblcoks = tetramino[0], tetramino[1], tetramino[2]
                        except NameError:
                            pass

                    elif event.key == pg.K_t:
                        try:
                            board.rerender(screen)
                            tetramino = drawTetra(index=tetra, rotated=False, color=tetracolor,
                                                  pixelx=(cell[2] - blocksize * 2),
                                                  pixely=cell[3])  # Поворот тетрамино в одну сторону
                            rotate = False
                            tetra, tetracolor, tblcoks = tetramino[0], tetramino[1], tetramino[2]
                            for block in tblcoks:  # Если при повороте тетрамино уходит за пределы сетки, возвращаем старую
                                if (board.get_cell([block[0], block[1]]) == "None"
                                        or board.cells[int(board.get_cell([block[0], block[1]])[2])][-1] != "empty"):
                                    board.rerender(screen)
                                    tetramino = drawTetra(index=tetra, color=tetracolor,
                                                          pixelx=(cell[2] - blocksize * 2),
                                                          pixely=cell[3], rotated=True)
                                    rotated = True
                                    tetra, tetracolor, tblcoks = tetramino[0], tetramino[1], tetramino[2]
                        except NameError:
                            pass
                    elif event.key == pg.K_j:
                        failed = False
                        try:
                            board.rerender(screen)
                            newcell = board.cells[board.cells.index(cell) - 1]
                            tetramino = drawTetra(index=tetra, color=tetracolor, pixelx=(newcell[2] - blocksize * 2),
                                                  pixely=cell[3], rotated=rotate)  # Перемещение тетрамино влево
                            tetra, tetracolor, tblcoks = tetramino[0], tetramino[1], tetramino[2]

                            for block in tblcoks:
                                # Если при перемещении тетрамино уходит за пределы сетки, возвращаем старую
                                if (board.get_cell([block[0], block[1]]) == "None" or (
                                        tetra == 8 and board.get_cell([block[0], block[1]])[1] == 9)
                                        or board.cells[int(board.get_cell([block[0], block[1]])[2])][-1] != "empty"):
                                    # Отдельный случай с прямой вертикальной формой, показавшей странное поведение
                                    board.rerender(screen)
                                    tetramino = drawTetra(index=tetra, color=tetracolor,
                                                          pixelx=(cell[2] - blocksize * 2),
                                                          pixely=cell[3], rotated=rotate)
                                    tetra, tetracolor, tblcoks = tetramino[0], tetramino[1], tetramino[2]
                                    failed = True
                            if not failed:
                                cell = newcell
                        except NameError:
                            pass
                    elif event.key == pg.K_l:
                        failed = False
                        try:
                            board.rerender(screen)
                            newcell = board.cells[board.cells.index(cell) + 1]
                            tetramino = drawTetra(index=tetra, color=tetracolor, pixelx=(newcell[2] - blocksize * 2),
                                                  pixely=cell[3], rotated=rotate)  # Перемещение тетрамино вправо
                            tetra, tetracolor, tblcoks = tetramino[0], tetramino[1], tetramino[2]

                            for block in tblcoks:
                                # Если при перемещении тетрамино уходит за пределы сетки, возвращаем старую
                                if (board.get_cell([block[0], block[1]]) == "None" or (
                                        tetra == 8 and board.get_cell([block[0], block[1]])[1] == 0)
                                        or board.cells[int(board.get_cell([block[0], block[1]])[2])][-1] != "empty"):
                                    # Отдельный случай с прямой вертикальной формой, показавшей странное поведение
                                    board.rerender(screen)
                                    tetramino = drawTetra(index=tetra, color=tetracolor,
                                                          pixelx=(cell[2] - blocksize * 2),
                                                          pixely=cell[3], rotated=rotate)
                                    tetra, tetracolor, tblcoks = tetramino[0], tetramino[1], tetramino[2]
                                    failed = True
                            if not failed:
                                cell = newcell
                        except NameError:
                            pass
                    elif event.key == pg.K_k:
                        failed = False
                        try:
                            board.rerender(screen)
                            try:
                                newcell = board.cells[board.cells.index(cell) + board.width]
                                tetramino = drawTetra(index=tetra, color=tetracolor, pixelx=(newcell[2] - blocksize * 2),
                                                      pixely=newcell[3], rotated=rotate)  # Перемещение тетрамино вниз
                                tetra, tetracolor, tblcoks = tetramino[0], tetramino[1], tetramino[2]

                                for block in tblcoks:
                                    # Если при перемещении тетрамино уходит за пределы сетки, возвращаем старую
                                    if (board.get_cell([block[0], block[1]]) == "None"
                                            or board.cells[int(board.get_cell([block[0], block[1]])[2])][-1] != "empty"):
                                        board.rerender(screen)
                                        tetramino = drawTetra(index=tetra, color=tetracolor,
                                                              pixelx=(cell[2] - blocksize * 2),
                                                              pixely=cell[3], rotated=rotate)
                                        tetra, tetracolor, tblcoks = tetramino[0], tetramino[1], tetramino[2]
                                        failed = True
                                if not failed:
                                    cell = newcell

                            except IndexError:
                                pass
                        except NameError:
                            pass
                    elif event.key == pg.K_w:
                        if board.snake[0][1] != "down":
                            board.snake[0][1] = "up"
                    elif event.key == pg.K_a:
                        if board.snake[0][1] != "right":
                            board.snake[0][1] = "left"
                    elif event.key == pg.K_s:
                        if board.snake[0][1] != "up":
                            board.snake[0][1] = "down"
                    elif event.key == pg.K_d:
                        if board.snake[0][1] != "left" and board.snake[0][1] != "none":
                            board.snake[0][1] = "right"
        if not paused:
            fps_clock.tick(30)
            pg.display.update()
            tick = fps_clock.tick()
            v += tick
            if cooldown:
                cooldown_v += 1
            snake_v += tick
            anim_v += tick
            if v >= v_time and not moved_down and not tetradrawn:
                v = 0
                moved_down = True
                failed = False
                try:  # перемещение тетрамино вниз каждую секунду
                    board.rerender(screen)
                    try:
                        colorproblem = False
                        newcell = board.cells[board.cells.index(cell) + board.width]
                        tetramino = drawTetra(index=tetra, color=tetracolor, pixelx=(newcell[2] - blocksize * 2),
                                              pixely=newcell[3], rotated=rotate)  # Перемещение тетрамино вниз
                        tetra, tetracolor, tblcoks = tetramino[0], tetramino[1], tetramino[2]
                        blocks = []

                        for block in tblcoks:
                            # Если при перемещении тетрамино уходит за пределы сетки, возвращаем старую
                            blocks.append(block[1])
                            if board.get_cell([block[0], block[1]]) == "None" or board.cells[int(board.get_cell([block[0], block[1]])[2])][-1] == "darkgreen":
                                board.rerender(screen)
                                tetramino = drawTetra(index=tetra, color=tetracolor,
                                                      pixelx=(cell[2] - blocksize * 2),
                                                      pixely=cell[3], rotated=rotate)
                                tetra, tetracolor, tblcoks = tetramino[0], tetramino[1], tetramino[2]
                            elif board.cells[int(board.get_cell([block[0], block[1]])[2])][-1] == "purple":
                                board.cells[int(board.get_cell([block[0], block[1]])[2])][-1] = "empty"
                                board.rerender(screen)
                                if not rotate:
                                    try:
                                        board.rerender(screen)
                                        tetramino = drawTetra(index=tetra, rotated=True, color=tetracolor,
                                                              pixelx=(cell[2] - blocksize * 2),
                                                              pixely=cell[3])  # Поворот тетрамино в одну сторону
                                        rotate = True
                                        tetra, tetracolor, tblcoks = tetramino[0], tetramino[1], tetramino[2]
                                        for block in tblcoks:  # Если при повороте тетрамино уходит за пределы сетки, возвращаем старую
                                            if (board.get_cell([block[0], block[1]]) == "None"
                                                    or board.cells[int(board.get_cell([block[0], block[1]])[2])][
                                                        -1] != "empty"):
                                                board.rerender(screen)
                                                rotate = False
                                                tetramino = drawTetra(index=tetra, color=tetracolor,
                                                                      pixelx=(cell[2] - blocksize * 2),
                                                                      pixely=cell[3], rotated=False)
                                                tetra, tetracolor, tblcoks = tetramino[0], tetramino[1], tetramino[2]
                                    except NameError:
                                        pass
                                board.spawnspinblock()
                            elif board.cells[int(board.get_cell([block[0], block[1]])[2])][-1] != "empty":
                                board.rerender(screen)
                                tetramino = drawTetra(index=tetra, color=tetracolor,
                                                      pixelx=(cell[2] - blocksize * 2),
                                                      pixely=cell[3], rotated=rotate)
                                tetra, tetracolor, tblcoks = tetramino[0], tetramino[1], tetramino[2]
                                colorproblem = True

                        if 461 in blocks or colorproblem and tetradrawn is False:
                            theblocks = []
                            for block in tblcoks:
                                co = (
                                    board.get_cell([block[0], block[1]]))
                                theblocks.append(co)
                                col = int(co[2])
                                try:
                                    del board.cells[col][-1]
                                    board.cells[col].append(tetracolor)
                                except Exception as e:
                                    print(e)
                            failed = True
                            tetradrawn = True
                            while True:
                                lost = False
                                cell = choice(board.first_column)
                                wrongcells = 0
                                board.rerender(screen)
                                rotate = choice([True, False])
                                tetramino = drawTetra(pixelx=(cell[2] - blocksize * 2), pixely=cell[3], rotated=rotate)
                                tetra, tetracolor, tblcoks = tetramino[0], tetramino[1], tetramino[2]
                                # отрисовка нового тетамино в случайном месте в верхних колоннах сетки
                                for block in tblcoks:  # проверяем, не вылезают ли блоки за сетку
                                    if board.get_cell([block[0], block[1]]) == "None":
                                        wrongcells += 1
                                    elif board.cells[int(board.get_cell([block[0], block[1]])[2])][-1] != "empty":
                                        lost = True
                                if lost:  # Смотрим, произошёл ли проигрышб перезапускаем доску
                                    board.render(screen)
                                    break
                                if wrongcells == 0:
                                    break
                            board.rerender(screen)
                            tetradrawn = False
                            colorproblem = False
                            board.tetraminos.append(theblocks)
                            board.check_completion()

                        if not failed:
                            cell = newcell
                    except IndexError:
                        pass
                except NameError:
                    pass
            else:
                moved_down = False
            if not cooldown:
                if snake_v >= fps // 8 :
                    snake_v = 0
                    if board.snake[0][1] == "left" and board.snake[0][0][1] != 0:
                        try:
                            usedblocks = []
                            for block in tblcoks:
                                usedblocks.append([board.get_cell(block)[0], board.get_cell(block)[1]])
                            tempcell1 = board.snake[0][0]
                            tempcell2 = board.cells[board.cells.index(tempcell1) - 1]
                            if board.cells[board.cells.index(tempcell1) - 1][-1] == "empty" and [tempcell1[0], tempcell1[1]] not in usedblocks and [tempcell2[0], tempcell2[1]] not in usedblocks:
                                board.cells[board.cells.index(tempcell1)][-1] = "empty"
                                board.cells[board.cells.index(tempcell1) - 1][-1] = "darkgreen"
                                board.snake[0][0] = board.cells[board.cells.index(tempcell1) - 1]
                                tempcell1[-1] = "empty"
                                for snackecell in board.snake[1:]:
                                    inde = board.snake.index(snackecell)
                                    tempcell2 = snackecell
                                    board.cells[board.cells.index(tempcell2)][-1] = "empty"
                                    board.cells[board.cells.index(tempcell1)][-1] = "darkgreen"
                                    board.snake[inde] = tempcell1
                                    tempcell1 = tempcell2
                                    board.rerender(screen)
                            elif [tempcell1[0], tempcell1[1]] in usedblocks or [tempcell2[0], tempcell2[1]] in usedblocks:
                                failed = False
                                cooldown = True
                                try:
                                    newcell = board.cells[board.cells.index(cell) - 1]
                                    tetramino = drawTetra(index=tetra, color=tetracolor,
                                                          pixelx=(newcell[2] - blocksize * 2),
                                                          pixely=cell[3], rotated=rotate)  # Перемещение тетрамино влево
                                    tetra, tetracolor, tblcoks = tetramino[0], tetramino[1], tetramino[2]

                                    for block in tblcoks:
                                        # Если при перемещении тетрамино уходит за пределы сетки, возвращаем старую
                                        if (board.get_cell([block[0], block[1]]) == "None" or (
                                                tetra == 8 and board.get_cell([block[0], block[1]])[1] == 9)
                                                or board.cells[int(board.get_cell([block[0], block[1]])[2])][
                                                    -1] != "empty"):
                                            snake_lose()
                                    board.rerender(screen)
                                    if not failed:
                                        cell = newcell
                                except NameError:
                                    pass
                            elif board.cells[board.cells.index(tempcell1) - 1][-1] == "purple":
                                if board.cells[board.cells.index(tempcell1) - 1][1] != 0:
                                    if board.cells[board.cells.index(tempcell1) - 2][-1] == "empty" and [board.cells[board.cells.index(tempcell1) - 2][0], board.cells[board.cells.index(tempcell1) - 2][1]] not in usedblocks:
                                        board.cells[board.cells.index(tempcell1) - 1][-1] = "empty"
                                        board.cells[board.cells.index(tempcell1) - 2][-1] = "purple"
                                    else:
                                        snake_lose()
                                else:
                                    snake_lose()

                        except Exception as e:
                            print(e)
                        board.rerender(screen)
                    elif board.snake[0][1] == "up" and board.snake[0][0][0] != 0:
                        tempcell1 = board.snake[0][0]
                        usedblocks = []
                        tempcell2 = board.cells[board.cells.index(tempcell1) - board.width]
                        for block in tblcoks:
                            usedblocks.append([board.get_cell(block)[0], board.get_cell(block)[1]])
                        if board.cells[board.cells.index(tempcell1) - board.width][-1] == "empty" and [tempcell1[0], tempcell1[1]] not in usedblocks and [tempcell2[0], tempcell2[1]] not in usedblocks:
                            board.cells[board.cells.index(tempcell1)][-1] = "empty"
                            board.cells[board.cells.index(tempcell1) - board.width][-1] = "darkgreen"
                            board.snake[0][0] = board.cells[board.cells.index(tempcell1) - board.width]
                            tempcell1[-1] = "empty"
                            for snackecell in board.snake[1:]:
                                inde = board.snake.index(snackecell)
                                tempcell2 = snackecell
                                board.cells[board.cells.index(tempcell2)][-1] = "empty"
                                board.cells[board.cells.index(tempcell1)][-1] = "darkgreen"
                                board.snake[inde] = tempcell1
                                tempcell1 = tempcell2
                        elif board.cells[board.cells.index(tempcell1) - board.width][-1] == "purple":
                            if board.cells[board.cells.index(tempcell1) - board.width][0] != 0:
                                if board.cells[board.cells.index(tempcell1) - board.width * 2][-1] == "empty" and [
                                    board.cells[board.cells.index(tempcell1) - 2 * board.width][0],
                                    board.cells[board.cells.index(tempcell1) - board.width * 2][1]] not in usedblocks:
                                    board.cells[board.cells.index(tempcell1) - board.width][-1] = "empty"
                                    board.cells[board.cells.index(tempcell1) - 2 * board.width][-1] = "purple"
                                else:
                                    snake_lose()
                            else:
                                snake_lose()
                        board.rerender(screen)
                    elif board.snake[0][1] == "down" and board.snake[0][0][0] != board.height - 1:
                        tempcell1 = board.snake[0][0]
                        tempcell2 = board.cells[board.cells.index(tempcell1) + board.width]
                        usedblocks = []
                        for block in tblcoks:
                            usedblocks.append([board.get_cell(block)[0], board.get_cell(block)[1]])
                        if board.cells[board.cells.index(tempcell1) + board.width][-1] == "empty" and [tempcell1[0], tempcell1[
                            1]] not in usedblocks and [tempcell2[0], tempcell2[1]] not in usedblocks:
                            board.cells[board.cells.index(tempcell1)][-1] = "empty"
                            board.cells[board.cells.index(tempcell1) + board.width][-1] = "darkgreen"
                            board.snake[0][0] = board.cells[board.cells.index(tempcell1) + board.width]
                            tempcell1[-1] = "empty"
                            for snackecell in board.snake[1:]:
                                inde = board.snake.index(snackecell)
                                tempcell2 = snackecell
                                board.cells[board.cells.index(tempcell2)][-1] = "empty"
                                board.cells[board.cells.index(tempcell1)][-1] = "darkgreen"
                                board.snake[inde] = tempcell1
                                tempcell1 = tempcell2
                        elif [tempcell1[0], tempcell1[1]] in usedblocks or [tempcell2[0], tempcell2[1]] in usedblocks:
                            failed = False
                            try:
                                board.rerender(screen)
                                try:
                                    newcell = board.cells[board.cells.index(cell) + board.width]
                                    tetramino = drawTetra(index=tetra, color=tetracolor,
                                                          pixelx=(newcell[2] - blocksize * 2),
                                                          pixely=newcell[3], rotated=rotate)  # Перемещение тетрамино вниз
                                    tetra, tetracolor, tblcoks = tetramino[0], tetramino[1], tetramino[2]

                                    for block in tblcoks:
                                        # Если при перемещении тетрамино уходит за пределы сетки, возвращаем старую
                                        if (board.get_cell([block[0], block[1]]) == "None"
                                                or board.cells[int(board.get_cell([block[0], block[1]])[2])][
                                                    -1] != "empty"):
                                            snake_lose()
                                    if not failed:
                                        cell = newcell

                                except IndexError:
                                    pass
                            except NameError:
                                pass
                        elif board.cells[board.cells.index(tempcell1) + board.width][-1] == "purple":
                            if board.cells[board.cells.index(tempcell1) + board.width][0] != board.height - 1:
                                if board.cells[board.cells.index(tempcell1) + board.width * 2][-1] == "empty" and [
                                    board.cells[board.cells.index(tempcell1) + 2 * board.width][0],
                                    board.cells[board.cells.index(tempcell1) + board.width * 2][1]] not in usedblocks:
                                    board.cells[board.cells.index(tempcell1) + board.width][-1] = "empty"
                                    board.cells[board.cells.index(tempcell1) + 2 * board.width][-1] = "purple"
                                else:
                                    snake_lose()
                            else:
                                snake_lose()
                        board.rerender(screen)
                    elif board.snake[0][1] == "right" and board.snake[0][0][1] != board.width - 1:
                        try:
                            usedblocks = []
                            for block in tblcoks:
                                usedblocks.append([board.get_cell(block)[0], board.get_cell(block)[1]])
                            tempcell1 = board.snake[0][0]
                            tempcell2 = board.cells[board.cells.index(tempcell1) + 1]
                            if board.cells[board.cells.index(tempcell1) + 1][-1] == "empty" and [tempcell1[0], tempcell1[1]] not in usedblocks and [tempcell2[0], tempcell2[1]] not in usedblocks:
                                board.cells[board.cells.index(tempcell1)][-1] = "empty"
                                board.cells[board.cells.index(tempcell1) + 1][-1] = "darkgreen"
                                board.snake[0][0] = board.cells[board.cells.index(tempcell1) + 1]
                                tempcell1[-1] = "empty"
                                for snackecell in board.snake[1:]:
                                    inde = board.snake.index(snackecell)
                                    tempcell2 = snackecell
                                    board.cells[board.cells.index(tempcell2)][-1] = "empty"
                                    board.cells[board.cells.index(tempcell1)][-1] = "darkgreen"
                                    board.snake[inde] = tempcell1
                                    tempcell1 = tempcell2
                                    board.rerender(screen)
                            elif [tempcell1[0], tempcell1[1]] in usedblocks or [tempcell2[0], tempcell2[1]] in usedblocks:
                                cooldown = True
                                failed = False
                                try:
                                    board.rerender(screen)
                                    newcell = board.cells[board.cells.index(cell) + 1]
                                    tetramino = drawTetra(index=tetra, color=tetracolor,
                                                          pixelx=(newcell[2] - blocksize * 2),
                                                          pixely=cell[3], rotated=rotate)  # Перемещение тетрамино вправо
                                    tetra, tetracolor, tblcoks = tetramino[0], tetramino[1], tetramino[2]

                                    for block in tblcoks:
                                        # Если при перемещении тетрамино уходит за пределы сетки, змейка умирает
                                        if (board.get_cell([block[0], block[1]]) == "None" or (
                                                tetra == 8 and board.get_cell([block[0], block[1]])[1] == 0)
                                                or board.cells[int(board.get_cell([block[0], block[1]])[2])][
                                                    -1] != "empty"):
                                            snake_lose()
                                    if not failed:
                                        cell = newcell
                                except Exception as e:
                                    print(e)
                            elif board.cells[board.cells.index(tempcell1) + 1][-1] == "purple":
                                if board.cells[board.cells.index(tempcell1) + 1][1] != (board.width - 1):
                                    if board.cells[board.cells.index(tempcell1) + 2][-1] == "empty" and [board.cells[board.cells.index(tempcell1) + 2][0], board.cells[board.cells.index(tempcell1) + 2][1]] not in usedblocks:
                                        board.cells[board.cells.index(tempcell1) + 1][-1] = "empty"
                                        board.cells[board.cells.index(tempcell1) + 2][-1] = "purple"
                                    else:
                                        snake_lose()
                                else:
                                    snake_lose()
                        except Exception as e:
                            print(e)
                        board.rerender(screen)
                    else:
                        board.render(screen)
                        cell = choice(board.first_column)
                        failed = True
                        while True:
                            rotate = choice([True, False])

                            wrongcells = 0
                            screen.fill("black")
                            board.rerender(screen)
                            tetramino = drawTetra(pixelx=(cell[2] - blocksize * 2), pixely=cell[3],
                                                  rotated=rotate)
                            tetra, tetracolor, tblcoks = tetramino[0], tetramino[1], tetramino[2]
                            # отрисовка нового тетамино в случайном месте в верхних колоннах сетки
                            for block in tblcoks:  # проверяем, не вылезают ли блоки за сетку
                                if board.get_cell([block[0], block[1]]) == "None":
                                    wrongcells += 1
                            if wrongcells == 0:
                                break
            if cooldown_v == fps // 2 or cooldown_v > fps // 2:
                cooldown = False
                cooldown_v = 0
            if anim_v >= fps // 2:
                anim_v = 0
                if animationframe == "frame1.png":
                    animationframe = "frame2.png"
                else:
                    animationframe = "frame1.png"
            board.rerender(screen)
    pg.quit()
    sys.exit()
# Проект в процессе разработки!
