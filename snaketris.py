# Это не финальная версия проекта, не оценивайте пожалуйста. Спасибо
import pygame as pg
import random
import sys
from pygame.locals import *
from random import choice

fps = 25
w, h = 600, 500
blocksize = 20  # размер одного блока
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
        self.tetraminos = []  # список для упадших тетрамино
        self.score = 0
        self.scoretext = f"Очки:{self.score}"
        self.font = pg.font.SysFont('arial', 20)
        self.display_score = pg.display.set_mode((w, h))
        self.fontcolor = "yellow"

    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def render(self, screen):
        nextSurf = self.font.render(self.scoretext, True, self.fontcolor)
        nextRect = nextSurf.get_rect()
        nextRect.topleft = (w - 150, 180)
        self.display_score.blit(nextSurf, nextRect)
        self.cells = []
        self.tetraminos = []
        self.score = 0
        self.scoretext = f"Очки:{self.score}"
        for i in range(self.height):
            for j in range(self.width):
                pg.draw.rect(screen, "white", (self.cell_size * j + self.top, self.cell_size * i + self.left,
                                               self.cell_size, self.cell_size), 1)
                self.cells.append([i, j, self.cell_size * j + self.top, self.cell_size * i + self.left, "empty"])
                if i == 0:
                    self.first_column.append(
                        [i, j, self.cell_size * j + self.top, self.cell_size * i + self.left, "empty"])

    def rerender(self, screen):
        nextSurf = self.font.render(self.scoretext, True, self.fontcolor)
        nextRect = nextSurf.get_rect()
        nextRect.topleft = (w - 150, 180)
        self.display_score.blit(nextSurf, nextRect)
        for i in range(self.height):
            for j in range(self.width):
                if board.cells[i * board.width + j][-1] == "empty":
                    pg.draw.rect(screen, "white", (self.cell_size * j + self.top, self.cell_size * i + self.left,
                                                   self.cell_size, self.cell_size), 1)
                else:
                    pg.draw.rect(screen, board.cells[i * board.width + j][-1],
                                 (self.cell_size * j + self.top, self.cell_size * i + self.left,
                                  self.cell_size, self.cell_size), 0)

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
            if cell[-1] == "empty": # Если клетка пустая, то ряд не заполнен
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
                    print(placedtetramino)
                    print(tetramino1)
                    print(tetramino2)
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


v = 0
moved_down = False

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
            if event.type == pg.QUIT:  # выход из игры
                running = False
            elif event.type == pg.KEYUP:
                if event.key == K_SPACE:
                    cell = choice(board.first_column)
                    while True:
                        rotate = choice([True, False])
                        lost = False
                        wrongcells = 0
                        screen.fill("black")
                        board.rerender(screen)
                        tetramino = drawTetra(pixelx=(cell[2] - blocksize * 2), pixely=cell[3])
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
                elif event.key == pg.K_a:
                    try:
                        screen.fill("black")
                        board.rerender(screen)
                        tetramino = drawTetra(index=tetra, rotated=True, color=tetracolor,
                                              pixelx=(cell[2] - blocksize * 2),
                                              pixely=cell[3])  # Поворот тетрамино в одну сторону
                        rotate = True
                        tetra, tetracolor, tblcoks = tetramino[0], tetramino[1], tetramino[2]
                        for block in tblcoks:  # Если при повороте тетрамино уходит за пределы сетки, возвращаем старую
                            if (board.get_cell([block[0], block[1]]) == "None"
                                    or board.cells[int(board.get_cell([block[0], block[1]])[2])][-1] != "empty"):
                                screen.fill("black")
                                board.rerender(screen)
                                rotate = False
                                tetramino = drawTetra(index=tetra, color=tetracolor,
                                                      pixelx=(cell[2] - blocksize * 2),
                                                      pixely=cell[3], rotated=False)
                                tetra, tetracolor, tblcoks = tetramino[0], tetramino[1], tetramino[2]
                    except NameError:
                        pass

                elif event.key == pg.K_d:
                    try:
                        screen.fill("black")
                        board.rerender(screen)
                        tetramino = drawTetra(index=tetra, rotated=False, color=tetracolor,
                                              pixelx=(cell[2] - blocksize * 2),
                                              pixely=cell[3])  # Поворот тетрамино в одну сторону
                        rotate = False
                        tetra, tetracolor, tblcoks = tetramino[0], tetramino[1], tetramino[2]
                        for block in tblcoks:  # Если при повороте тетрамино уходит за пределы сетки, возвращаем старую
                            if (board.get_cell([block[0], block[1]]) == "None"
                                    or board.cells[int(board.get_cell([block[0], block[1]])[2])][-1] != "empty"):
                                screen.fill("black")
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
                        screen.fill("black")
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
                                screen.fill("black")
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
                        screen.fill("black")
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
                                screen.fill("black")
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
                        screen.fill("black")
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
                                    screen.fill("black")
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
        fps_clock.tick(30)
        pg.display.update()
        v += fps_clock.tick()
        if v == fps and not moved_down and not tetradrawn:
            v = 0
            moved_down = True
            failed = False
            try:  # перемещение тетрамино вниз каждую секунду
                screen.fill("black")
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
                        if board.get_cell([block[0], block[1]]) == "None":
                            screen.fill("black")
                            board.rerender(screen)
                            tetramino = drawTetra(index=tetra, color=tetracolor,
                                                  pixelx=(cell[2] - blocksize * 2),
                                                  pixely=cell[3], rotated=rotate)
                            tetra, tetracolor, tblcoks = tetramino[0], tetramino[1], tetramino[2]
                        elif board.cells[int(board.get_cell([block[0], block[1]])[2])][-1] != "empty":
                            screen.fill("black")
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
                            screen.fill("black")
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
    pg.quit()
    sys.exit()
# Проект в процессе разработки!
