import pygame

pygame.init()

from enum import Enum

class Direction(Enum):
    RIGHT = 0
    DOWN = 1
    LEFT = 2
    UP = 3


# 0. Ustawienia poczatkowe:

# 0.0 Ustawienia okna:

BOARD_WIDTH = 480
BOARD_HEIGHT = 480
MODULE_SIZE = 30

#logo = pygame.image.load("tetris_logo.png")
#pygame.display.set_icon(logo)
pygame.display.set_caption("Tetris Gosi")
screen = pygame.display.set_mode(size=(BOARD_WIDTH, BOARD_HEIGHT))

# 0.1 Tworzenie siatki obszaru gry

number_of_board_columns = int(BOARD_WIDTH / MODULE_SIZE)
number_of_board_rows = int(BOARD_HEIGHT / MODULE_SIZE)

x, y, s = 0, 0, 0

board = [[[x, y, s]] * number_of_board_columns for i in range(number_of_board_rows)]

for row in range(number_of_board_rows):
    for column in range(number_of_board_columns):
        x = column * MODULE_SIZE
        y = row * MODULE_SIZE
        board[row][column] = [x, y, s]

# 0.2 Tworzenie modulu (kwadracika)

class Module:
    def __init__(self, x_module, y_module):
        self.x_module = x_module
        self.y_module = y_module

    def draw(self):
        pygame.draw.rect(screen, (255, 255, 255), (self.x_module, self.y_module, MODULE_SIZE, MODULE_SIZE))
        # full_or_empty_module = 1
        # return full_or_empty_module

    def remove(self):
        pygame.draw.rect(screen, (0, 0, 0), (self.x_module, self.y_module, MODULE_SIZE, MODULE_SIZE))
        # full_empty_module = 0
        # return full_empty_module


# 0.3 Tworzenie map klockow

block_O = [[1, 1],
           [1, 1]]

block_L = [[0, 1, 0],
           [0, 1, 0],
           [0, 1, 1]]

block_J = [[0, 1, 0],
           [0, 1, 0],
           [1, 1, 0]]

block_I = [[0, 1, 0, 0],
           [0, 1, 0, 0],
           [0, 1, 0, 0],
           [0, 1, 0, 0]]

block_T = [[0, 1, 0],
           [0, 1, 1],
           [0, 1, 0]]

block_Z = [[0, 0, 1],
           [0, 1, 1],
           [0, 1, 0]]

block_S = [[1, 0, 0],
           [1, 1, 0],
           [0, 1, 0]]


# 0.4 Manipulacja klockiem

class Block:
    def __init__(self, x_block, y_block, shape):
        self.x_block = x_block
        self.y_block = y_block
        self.size_of_block = len(shape)
        self.shape = shape
        self.modules_xy = [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]]
        self.block_set = False

    def do_after_block_set(self):
        for row in range(number_of_board_rows):
            for column in range(number_of_board_columns):
                for i in range(4):
                    if self.modules_xy[i] == board[row][column]:
                        board[row][column][2] = 1
                        print("board", board[row][column])

    def remove(self):
        for row in range(4):
            x_module = self.modules_xy[row][0]
            y_module = self.modules_xy[row][1]
            module = Module(x_module, y_module)
            module.remove()
        pygame.display.update()

    def draw(self):
        i = 0
        for row in range(self.size_of_block):
            for column in range(self.size_of_block):
                if self.shape[row][column] == 1:
                    x_module = self.x_block - MODULE_SIZE + column * MODULE_SIZE
                    y_module = self.y_block - MODULE_SIZE + row * MODULE_SIZE
                    module = Module(x_module, y_module)
                    self.modules_xy[i][0] = x_module
                    self.modules_xy[i][1] = y_module
                    i += 1
                    module.draw()
                pygame.display.update()

    def rotate(self): #WYGLADA NA TO ZE DZIALA I TRZEBA TESTOWAC
        shape_rotated = [[0] * self.size_of_block for i in range(self.size_of_block)]
        moved_right = False
        moved_left = False
        moved_up = False

        block_I_90deg = [[0, 0, 0, 0],
                         [1, 1, 1, 1],
                         [0, 0, 0, 0],
                         [0, 0, 0, 0]]

        block_I_180deg = [[0, 0, 1, 0],
                          [0, 0, 1, 0],
                          [0, 0, 1, 0],
                          [0, 0, 1, 0]]

        block_I_copy = [[0, 1, 0, 0],
                        [0, 1, 0, 0],
                        [0, 1, 0, 0],
                        [0, 1, 0, 0]]

        # sprawdzanie czy czesc shape z "0" wykracza poza plansze:
        if not self.block_set:
            if self.x_block < MODULE_SIZE:
                self.x_block += MODULE_SIZE
                moved_right = True
                if self.shape == block_I_180deg:
                    self.x_block += MODULE_SIZE
            if self.x_block > BOARD_WIDTH - (self.size_of_block - 1) * MODULE_SIZE:
                self.x_block -= MODULE_SIZE
                moved_left = True
                if self.shape == block_I_copy:
                    self.x_block -= MODULE_SIZE
            if self.y_block > BOARD_HEIGHT - (self.size_of_block - 1) * MODULE_SIZE:
                self.y_block -= MODULE_SIZE
                moved_up = True
                if self.shape == block_I_90deg:
                    self.y_block -= MODULE_SIZE

            #sprawdzanie czy klocek po obrocie (shape_rotated) będzie kolidowal z innymi klockai na planszy (board)
            collision = False
            i, x_rotated, y_rotated = 0, 0, 0
            modules_xy_rotated = [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]]

            for row in range(self.size_of_block):
                for column in range(self.size_of_block):
                    shape_rotated[column][self.size_of_block - row - 1] = self.shape[row][column]
            for row in range(self.size_of_block):
                for column in range(self.size_of_block):
                    if shape_rotated[row][column] == 1:
                        x_rotated = self.x_block - MODULE_SIZE + column * MODULE_SIZE
                        y_rotated = self.y_block - MODULE_SIZE + row * MODULE_SIZE
                        for row1 in range(number_of_board_rows):
                            for column1 in range(number_of_board_columns):
                                if x_rotated == board[row1][column1][0] and y_rotated == board[row1][column1][1]:
                                    if board[row1][column1][2] == 1:
                                        collision = True
                                        #NIC NIE ROBIC JAK JEST KOLIZKA
                                    else: #JESLI JEDEN MODUL MA KOLIZJE TO modules_xy_rotated WPROWADZI TYLKO
                                        # 3 WARTOSCI, A POZOSTALY BEDZIE 0,0,0, ALE PO WYJSCIU Z PETLI TE
                                        # WARTOSCI NIE BEDA UZYWANE,BO NASTAPILA KOLIZJA, I TABLICA modules_xy_rotated
                                        # BEDZIE WYPELNIANA NA NOWO W KOLEJNEJITERACJI PETLI
                                        modules_xy_rotated[i][0] = x_rotated
                                        modules_xy_rotated[i][1] = y_rotated
                        i += 1
            print("modules_xy_rotated", modules_xy_rotated)
            print("collision", collision)
            if not collision:
                self.remove()
                for row in range(self.size_of_block):
                    for column in range(self.size_of_block):
                        self.shape[row][column] = shape_rotated[row][column]
                for i in range(4):
                    self.modules_xy[i] = modules_xy_rotated[i]
                for i in range(4):
                    x_module = modules_xy_rotated[i][0]
                    y_module = modules_xy_rotated[i][1]
                    module = Module(x_module, y_module)
                    module.draw()
            else:
                if moved_right:
                    self.x_block -= MODULE_SIZE
                    if self.shape == block_I_180deg: #CIEKAWE ZE DZIALA, POPOROWNUJE WSKAZNIKI NA TABICE, NEI TABLICE
                        self.x_block -= MODULE_SIZE
                elif moved_left:
                    self.x_block += MODULE_SIZE
                    if self.shape == block_I_copy: #MUSI BYC _copy ,BO INACZEJ NEI DZIALA
                        self.x_block += MODULE_SIZE
                elif moved_up:
                    self.y_block += MODULE_SIZE
                    if self.shape == block_I_90deg:
                        self.y_block += MODULE_SIZE
            pygame.display.update()

            """for row in range(self.size_of_block):
                for column in range(self.size_of_block):
                    shape_rotated[column][self.size_of_block - row - 1] = self.shape[row][column]
            for row in range(self.size_of_block):
                for column in range(self.size_of_block):
                    self.shape[row][column] = shape_rotated[row][column]
            self.remove()
            self.draw()"""

    def move(self, direction):
        def draw_moved_block():
            for row in range(4):
                for column in range(2):
                    self.modules_xy[row][column] = modules_xy_moved[row][column]
            for row in range(4):
                x_module = self.modules_xy[row][0]
                y_module = self.modules_xy[row][1]
                module = Module(x_module, y_module)
                module.draw()
            pygame.display.update()

        modules_xy_moved = [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]]
        collision = False

        if not self.block_set:
            if direction == Direction.RIGHT:
                for row in range(4):
                    if self.modules_xy[row][0] + MODULE_SIZE >= BOARD_WIDTH:
                        collision = True
                if not collision:
                    for row in range(4):
                        modules_xy_moved[row][0] = self.modules_xy[row][0] + MODULE_SIZE
                        modules_xy_moved[row][1] = self.modules_xy[row][1]
                    self.remove()
                    draw_moved_block()
                    self.x_block += MODULE_SIZE
            elif direction == Direction.DOWN:
                for row in range(4):
                    if self.modules_xy[row][1] + MODULE_SIZE >= BOARD_HEIGHT:
                        self.block_set = True
                        self.do_after_block_set()
                if not self.block_set:
                    for row in range(4):
                        modules_xy_moved[row][0] = self.modules_xy[row][0]
                        modules_xy_moved[row][1] = self.modules_xy[row][1] + MODULE_SIZE
                    self.remove()
                    draw_moved_block()
                    self.y_block += MODULE_SIZE
            elif direction == Direction.LEFT:
                for row in range(4):
                    if self.modules_xy[row][0] - MODULE_SIZE < 0:
                        collision = True
                if not collision:
                    for row in range(4):
                        modules_xy_moved[row][0] = self.modules_xy[row][0] - MODULE_SIZE
                        modules_xy_moved[row][1] = self.modules_xy[row][1]
                    self.remove()
                    draw_moved_block()
                    self.x_block -= MODULE_SIZE
            elif direction == Direction.UP:  # tylko do uzycia w funkcji self.rotate()
                for row in range(4):
                    if self.modules_xy[row][1] - MODULE_SIZE < 0:
                        collision = True
                if not collision:
                    for row in range(4):
                        modules_xy_moved[row][0] = self.modules_xy[row][0]
                        modules_xy_moved[row][1] = self.modules_xy[row][1] - MODULE_SIZE
                    self.remove()
                    draw_moved_block()
                    self.y_block -= MODULE_SIZE

# 1. losowanie klocka, ktory zaraz spadnie

block1 = Block( 1 * MODULE_SIZE, 1 * MODULE_SIZE, block_I)
block1.draw()

#board to test:
print("board[5][1]", board[5][1])
board[5][1] = [30, 150, 1]
module = Module(30, 150)
module.draw()
print("board[5][3]", board[5][3])
board[5][3] = [90, 150, 1]
module = Module(90, 150)
module.draw()
pygame.display.update()

# 2. Automatyczne przesuwanie klocka w dol co okreslony czas

# 3. kasowanie lini, sprawdzanie czy przegrana
#to chyba bedzie w class Block

# 4. Glowny program, obsluga zdarzen i klawiszy

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                block1.rotate()
            if event.key == pygame.K_RIGHT:
                block1.move(Direction.RIGHT)
            if event.key == pygame.K_DOWN:
                block1.move(Direction.DOWN)
            if event.key == pygame.K_LEFT:
                block1.move(Direction.LEFT)


