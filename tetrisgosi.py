import pygame

pygame.init()

from enum import Enum
from random import randint
from copy import deepcopy


class Direction(Enum):
    RIGHT = 0
    DOWN = 1
    LEFT = 2
    UP = 3

# 0. Ustawienia poczatkowe:

# 0.0 Ustawienia okna:

BOARD_WIDTH = 300
BOARD_HEIGHT = 420
MODULE_SIZE = 30

# logo = pygame.image.load("tetris_logo.png")
# pygame.display.set_icon(logo)
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

module_green = pygame.image.load("module_green.jpg")
module_blue = pygame.image.load("module_blue.jpg")
module_orange = pygame.image.load("module_orange.jpg")
module_dark_blue = pygame.image.load("module_dark_blue.jpg")
module_yellow = pygame.image.load("module_yellow.jpg")
module_violet = pygame.image.load("module_violet.jpg")
module_red = pygame.image.load("module_red.jpg")

def draw_module(x_module, y_module, color):
    #pygame.draw.rect(screen, (255, 255, 255), (x_module, y_module, MODULE_SIZE, MODULE_SIZE))
    if color == 6:
        screen.blit(module_green, [x_module, y_module])
    elif color == 3:
        screen.blit(module_blue, [x_module, y_module])
    elif color == 2:
        screen.blit(module_dark_blue, [x_module, y_module])
    elif color == 1:
        screen.blit(module_orange, [x_module, y_module])
    elif color == 7:
        screen.blit(module_yellow, [x_module, y_module])
    elif color == 4:
        screen.blit(module_violet, [x_module, y_module])
    elif color == 5:
        screen.blit(module_red, [x_module, y_module])


def remove_module(x_module, y_module):
    pygame.draw.rect(screen, (0, 0, 0), (x_module, y_module, MODULE_SIZE, MODULE_SIZE))


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

#TODO wstadzic switchera do klasy block razem z mapami klockow


# 0.4 Manipulacja klockiem

class Block:
    def __init__(self, x_block, y_block, number):
        self.x_block = x_block
        self.y_block = y_block
        self.number = number

        def switch_number_shape(number):
            switcher = {
                1: block_L,
                2: block_J,
                3: block_I,
                4: block_T,
                5: block_Z,
                6: block_S,
                7: block_O
            }
            return switcher.get(number, block_O)

        self.shape = switch_number_shape(number)
        self.size_of_block = len(self.shape)
        self.modules_xy = [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]]
        self.block_set = False
        #number_color = {3: 'blue', 2: 'dark_blue', 1: 'orange',
        #              6: 'green', 4: 'violet', 5: 'red', 7: 'yellow'}
        #self.color = number_color[number]

    def do_after_block_set(self):
        for row in range(number_of_board_rows):
            for column in range(number_of_board_columns):
                for i in range(4):
                    if self.modules_xy[i] == board[row][column]:
                        board[row][column][2] = self.number
                        # print("block is set on board", board[row][column])
        self.block_set = True

    def remove(self):
        for row in range(4):
            x_module = self.modules_xy[row][0]
            y_module = self.modules_xy[row][1]
            remove_module(x_module, y_module)
        pygame.display.update()

    def draw(self):
        i = 0
        for row in range(self.size_of_block):
            for column in range(self.size_of_block):
                if self.shape[row][column] == 1:
                    x_module = self.x_block - MODULE_SIZE + column * MODULE_SIZE
                    y_module = self.y_block - MODULE_SIZE + row * MODULE_SIZE
                    self.modules_xy[i][0] = x_module
                    self.modules_xy[i][1] = y_module
                    i += 1
                    draw_module(x_module, y_module, self.number)
                pygame.display.update()

    def rotate(self):
        shape_rotated = [[0] * self.size_of_block for i in range(self.size_of_block)]
        moved_right = False
        moved_left = False
        moved_up = False
        moved_down = False

        block_I_90deg = [[0, 0, 0, 0],
                         [1, 1, 1, 1],
                         [0, 0, 0, 0],
                         [0, 0, 0, 0]]

        block_I_270deg = [[0, 0, 0, 0],
                          [0, 0, 0, 0],
                          [1, 1, 1, 1],
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
            if self.y_block < MODULE_SIZE:
                self.y_block += MODULE_SIZE
                moved_down = True
                if self.shape == block_I_270deg:
                    self.y_block += MODULE_SIZE

            # sprawdzanie czy klocek po obrocie (shape_rotated) bedzie kolidowal z innymi klockai na planszy (board)
            collision = False
            i, x_rotated, y_rotated = 0, 0, 0
            modules_xy_rotated = [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]]

            for row in range(self.size_of_block):
                for column in range(self.size_of_block):
                    shape_rotated[column][self.size_of_block - row - 1] = self.shape[row][column]

            for row in range(self.size_of_block):  # TODO A MOZE ZROBIC Z TEGO FUNKCJE ZEBY WYJSC JEDNYM RETURNEM
                if collision:
                    break
                for column in range(self.size_of_block):
                    if collision:
                        break
                    if shape_rotated[row][column] == 1:
                        x_rotated = self.x_block - MODULE_SIZE + column * MODULE_SIZE
                        y_rotated = self.y_block - MODULE_SIZE + row * MODULE_SIZE
                        for row1 in range(number_of_board_rows):
                            if collision:
                                break
                            for column1 in range(number_of_board_columns):
                                if x_rotated == board[row1][column1][0] and y_rotated == board[row1][column1][1]:
                                    if board[row1][column1][2] != 0:
                                        collision = True
                                        break
                                    else:
                                        modules_xy_rotated[i][0] = x_rotated
                                        modules_xy_rotated[i][1] = y_rotated
                        i += 1
            if not collision:
                self.remove()
                self.shape = deepcopy(shape_rotated)
                self.modules_xy = deepcopy(modules_xy_rotated)
                for i in range(4):
                    x_module = modules_xy_rotated[i][0]
                    y_module = modules_xy_rotated[i][1]
                    draw_module(x_module, y_module, self.number)
            else:
                if moved_right:
                    self.x_block -= MODULE_SIZE
                    if self.shape == block_I_180deg:
                        self.x_block -= MODULE_SIZE
                elif moved_left:
                    self.x_block += MODULE_SIZE
                    if self.shape == block_I_copy:  # MUSI BYC _copy ,BO INACZEJ NIE DZIALA
                        self.x_block += MODULE_SIZE
                elif moved_up:
                    self.y_block += MODULE_SIZE
                    if self.shape == block_I_90deg:
                        self.y_block += MODULE_SIZE
                elif moved_down:
                    self.y_block -= MODULE_SIZE
                    if self.shape == block_I_270deg:
                        self.y_block -= MODULE_SIZE
            pygame.display.update()

    def move(self, direction):
        def draw_moved_block():
            self.modules_xy = deepcopy(modules_xy_moved)
            for row in range(4):
                x_module = self.modules_xy[row][0]
                y_module = self.modules_xy[row][1]
                draw_module(x_module, y_module, self.number)
            pygame.display.update()

        def check_collision_after_move():
            collision1 = False
            for row in range(number_of_board_rows):
                for column in range(number_of_board_columns):
                    if x_moved == board[row][column][0] and y_moved == board[row][column][1]:
                        if board[row][column][2] != 0:
                            collision1 = True
                            return collision1

        modules_xy_moved = [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]]
        collision = False
        i, x_moved, y_moved = 0, 0, 0

        if not self.block_set:
            if direction == Direction.RIGHT:
                for i in range(4):
                    if self.modules_xy[i][0] + MODULE_SIZE >= BOARD_WIDTH:
                        collision = True
                        break
                if not collision:
                    for i in range(4):
                        x_moved = self.modules_xy[i][0] + MODULE_SIZE
                        y_moved = self.modules_xy[i][1]
                        if check_collision_after_move():
                            collision = True
                            break
                if not collision:
                    for i in range(4):
                        modules_xy_moved[i][0] = self.modules_xy[i][0] + MODULE_SIZE
                        modules_xy_moved[i][1] = self.modules_xy[i][1]
                    self.remove()
                    draw_moved_block()
                    self.x_block += MODULE_SIZE
            elif direction == Direction.DOWN:
                for i in range(4):
                    if self.modules_xy[i][1] + MODULE_SIZE >= BOARD_HEIGHT:
                        self.do_after_block_set()
                        break
                if not self.block_set:
                    for i in range(4):
                        x_moved = self.modules_xy[i][0]
                        y_moved = self.modules_xy[i][1] + MODULE_SIZE
                        if check_collision_after_move():
                            self.do_after_block_set()
                            break
                if not self.block_set:
                    for i in range(4):
                        modules_xy_moved[i][0] = self.modules_xy[i][0]
                        modules_xy_moved[i][1] = self.modules_xy[i][1] + MODULE_SIZE
                    self.remove()
                    draw_moved_block()
                    self.y_block += MODULE_SIZE
            elif direction == Direction.LEFT:
                for i in range(4):
                    if self.modules_xy[i][0] - MODULE_SIZE < 0:
                        collision = True
                        break
                if not collision:
                    for i in range(4):
                        x_moved = self.modules_xy[i][0] - MODULE_SIZE
                        y_moved = self.modules_xy[i][1]
                        if check_collision_after_move():
                            collision = True
                            break
                if not collision:
                    for i in range(4):
                        modules_xy_moved[i][0] = self.modules_xy[i][0] - MODULE_SIZE
                        modules_xy_moved[i][1] = self.modules_xy[i][1]
                    self.remove()
                    draw_moved_block()
                    self.x_block -= MODULE_SIZE


# 3. kasowanie lini, sprawdzanie czy przegrana



def delete_line():
    full_line = False
    for row in range(number_of_board_rows):
        for column in range(number_of_board_columns):
            if board[row][column][2] != 0:
                full_line = True
            else:
                full_line = False
                break
        if full_line:
            for column_in_full_line in range(number_of_board_columns):
                x_module_in_full_line = column_in_full_line * MODULE_SIZE
                y_module_in_full_line = row * MODULE_SIZE
                remove_module(x_module_in_full_line, y_module_in_full_line)
            # TODO jesli modul 'wisi w powietrzu' to ma opasc na inny modul
            for row_above_full_line in range(row, 0, -1):
                for column_above_full_line in range(number_of_board_columns):
                    if board[row_above_full_line - 1][column_above_full_line][2] != 0: #tu jest color ktory chceprzeniesc nizej
                        x_module_above_full_line = column_above_full_line * MODULE_SIZE
                        y_module_target = row_above_full_line * MODULE_SIZE
                        y_module_to_place_on_target = (row_above_full_line - 1) * MODULE_SIZE
                        draw_module(x_module_above_full_line, y_module_target, board[row_above_full_line - 1][column_above_full_line][2])
                        remove_module(x_module_above_full_line, y_module_to_place_on_target)
                    board[row_above_full_line][column_above_full_line][2] = board[row_above_full_line - 1][column_above_full_line][2]
            return full_line


# 4. Glowny program, obsluga zdarzen i klawiszy

def main():
    running = True
    block1 = Block(int(number_of_board_columns / 2 * MODULE_SIZE), MODULE_SIZE, 1)
    block1.draw()
    pygame.time.set_timer(pygame.USEREVENT, 1000)
    score = 0

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if not block1.block_set:
                if event.type == pygame.USEREVENT:  # 2. Automatyczne przesuwanie klocka w dol co okreslony czas
                    block1.move(Direction.DOWN)
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        block1.rotate()
                    if event.key == pygame.K_RIGHT:
                        block1.move(Direction.RIGHT)
                    if event.key == pygame.K_DOWN:
                        block1.move(Direction.DOWN)
                    if event.key == pygame.K_LEFT:
                        block1.move(Direction.LEFT)
            else:
                while delete_line():
                    score += 1
                    print("score:", score)
                # 1. losowanie klocka, ktory zaraz spadnie
                random_number = randint(1, 7)
                block1 = Block(int(number_of_board_columns / 2 * MODULE_SIZE), MODULE_SIZE, random_number) #TODO przekazywac numer do klasy block
                block1.draw()


if __name__ == "__main__":
    main()
