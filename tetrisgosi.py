import pygame

pygame.init()
pygame.mixer.init()

from enum import Enum
from random import randint
from copy import deepcopy


class Direction(Enum):
    RIGHT = 0
    DOWN = 1
    LEFT = 2
    UP = 3


BOARD_WIDTH = 360
BOARD_HEIGHT = 540
MODULE_SIZE = 30
TOP_MARGIN = 30
LEFT_MARGIN = 30
LINE_THICK = 4

logo = pygame.image.load("tetris_logo.png")
pygame.display.set_icon(logo)
pygame.display.set_caption("Tetris Gosi")
screen = pygame.display.set_mode(size=(600, 600))

pygame.draw.rect(screen, (255, 255, 255), (LEFT_MARGIN - LINE_THICK, TOP_MARGIN - LINE_THICK, int(BOARD_WIDTH + 1.5 * LINE_THICK), int(BOARD_HEIGHT + 1.5 * LINE_THICK)), LINE_THICK)
pygame.draw.rect(screen, (255, 255, 255), (420, 450, 150, 120), LINE_THICK)
pygame.draw.rect(screen, (255, 255, 255), (420, 30, 150, 210), LINE_THICK)


score_font = pygame.font.SysFont('Arial', 30)
score_text = score_font.render('Your score:', True, (255, 255, 255))
screen.blit(score_text, (430, 460))

score_font2 = pygame.font.SysFont('Arial', 40)

help_font = pygame.font.SysFont('Arial', 20)
help_text = help_font.render('Press space to rotate', True, (255, 255, 255))
screen.blit(help_text, (415, 255))
help_text1 = help_font.render('Press arrows to move', True, (255, 255, 255))
screen.blit(help_text1, (415, 285))

next_block_text = score_font.render('Next block:', True, (255, 255, 255))
screen.blit(next_block_text, (435, 40))

number_of_board_columns = int(BOARD_WIDTH / MODULE_SIZE)
number_of_board_rows = int(BOARD_HEIGHT / MODULE_SIZE)

x, y, s = 0, 0, 0

board = [[[x, y, s]] * number_of_board_columns for i in range(number_of_board_rows)]

for row in range(number_of_board_rows):
    for column in range(number_of_board_columns):
        x = column * MODULE_SIZE + LEFT_MARGIN
        y = row * MODULE_SIZE + TOP_MARGIN
        board[row][column] = [x, y, s]

module_green = pygame.image.load("module_green.jpg")
module_blue = pygame.image.load("module_blue.jpg")
module_orange = pygame.image.load("module_orange.jpg")
module_dark_blue = pygame.image.load("module_dark_blue.jpg")
module_yellow = pygame.image.load("module_yellow.jpg")
module_violet = pygame.image.load("module_violet.jpg")
module_red = pygame.image.load("module_red.jpg")


def draw_module(x_module, y_module, color):
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

    def do_after_block_set(self):
        for row in range(number_of_board_rows):
            for column in range(number_of_board_columns):
                for i in range(4):
                    if self.modules_xy[i] == board[row][column]:
                        board[row][column][2] = self.number
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
            if self.x_block < MODULE_SIZE + LEFT_MARGIN:
                self.x_block += MODULE_SIZE
                moved_right = True
                if self.shape == block_I_180deg:
                    self.x_block += MODULE_SIZE
            if self.x_block > BOARD_WIDTH + LEFT_MARGIN - (self.size_of_block - 1) * MODULE_SIZE:
                self.x_block -= MODULE_SIZE
                moved_left = True
                if self.shape == block_I_copy:
                    self.x_block -= MODULE_SIZE
            if self.y_block > BOARD_HEIGHT +TOP_MARGIN - (self.size_of_block - 1) * MODULE_SIZE:
                self.y_block -= MODULE_SIZE
                moved_up = True
                if self.shape == block_I_90deg:
                    self.y_block -= MODULE_SIZE
            if self.y_block < MODULE_SIZE + TOP_MARGIN:
                self.y_block += MODULE_SIZE
                moved_down = True
                if self.shape == block_I_270deg:
                    self.y_block += MODULE_SIZE

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
                    if self.modules_xy[i][0] + MODULE_SIZE >= BOARD_WIDTH + LEFT_MARGIN:
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
                    if self.modules_xy[i][1] + MODULE_SIZE >= BOARD_HEIGHT + TOP_MARGIN:
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
                    if self.modules_xy[i][0] - MODULE_SIZE < LEFT_MARGIN:
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
                x_module_in_full_line = column_in_full_line * MODULE_SIZE + LEFT_MARGIN
                y_module_in_full_line = row * MODULE_SIZE +TOP_MARGIN
                remove_module(x_module_in_full_line, y_module_in_full_line)
            for row_above_full_line in range(row, 0, -1):
                for column_above_full_line in range(number_of_board_columns):
                    if board[row_above_full_line - 1][column_above_full_line][2] != 0:
                        x_module_above_full_line = column_above_full_line * MODULE_SIZE + LEFT_MARGIN
                        y_module_target = row_above_full_line * MODULE_SIZE + TOP_MARGIN
                        y_module_to_place_on_target = (row_above_full_line - 1) * MODULE_SIZE +TOP_MARGIN
                        draw_module(x_module_above_full_line, y_module_target, board[row_above_full_line - 1][column_above_full_line][2])
                        remove_module(x_module_above_full_line, y_module_to_place_on_target)
                    board[row_above_full_line][column_above_full_line][2] = board[row_above_full_line - 1][column_above_full_line][2]
            pygame.display.update()
            return full_line


class Button:
    def __init__(self,is_on, x_button, y_button):
        self.is_on = is_on
        self.x_button = x_button
        self.y_button = y_button

    def draw(self):
        if self.is_on:
            sound_icon = pygame.image.load('sound_icon.jpg')
            screen.blit(sound_icon, [self.x_button, self.y_button])
            pygame.mixer.music.unpause()
        else:
            mute_icon = pygame.image.load('mute_icon.jpg')
            screen.blit(mute_icon, [self.x_button, self.y_button])
            pygame.mixer.music.pause()
        pygame.display.update()

    def draw_pointed(self):
        if self.is_on:
            sound_icon_pressed = pygame.image.load('sound_icon_pressed.jpg')
            screen.blit(sound_icon_pressed, [self.x_button, self.y_button])
        else:
            mute_icon_pressed = pygame.image.load('mute_icon_pressed.jpg')
            screen.blit(mute_icon_pressed, [self.x_button, self.y_button])
        pygame.display.update()


def main():
    running = True

    random_number = randint(1, 7)
    next_block_number = randint(1, 7)

    next_block = Block(480, 130, next_block_number)
    next_block.draw()

    block1 = Block(int(number_of_board_columns / 2 * MODULE_SIZE + LEFT_MARGIN), MODULE_SIZE + TOP_MARGIN, random_number)
    block1.draw()

    sound_button_x, sound_button_y, sound_button_size = 450, 330, 60
    sound_is_on = True
    sound_button = Button(sound_is_on, sound_button_x, sound_button_y)
    sound_button.draw()
    pygame.mixer.music.load('music.mp3')
    pygame.mixer.music.play(0)

    pygame.time.set_timer(pygame.USEREVENT, 100)

    score = 0
    i, j, k = 0, 0, 0

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            mouse = pygame.mouse.get_pos()
            if sound_button_x < mouse[0] < sound_button_x + sound_button_size and sound_button_y < mouse[1] < sound_button_y + sound_button_size:
                sound_button.draw_pointed()
                print("pointed")
                if event.type == pygame.MOUSEBUTTONDOWN:
                    sound_is_on = not sound_is_on
                    print("sound is on", sound_is_on)
                    sound_button = Button(sound_is_on, sound_button_x, sound_button_y)
                    sound_button.draw()
                    print("pressed")
            else:
                sound_button.draw()
            if not block1.block_set:
                keys_pressed = pygame.key.get_pressed()
                if event.type == pygame.USEREVENT:
                    if i == 10:
                        block1.move(Direction.DOWN)
                        i = 0
                    else:
                        i += 1
                if k == 2:
                    if keys_pressed[pygame.K_SPACE]:
                        block1.rotate()
                    k = 0
                else:
                    k += 1
                if j == 1:
                    if keys_pressed[pygame.K_RIGHT]:
                        block1.move(Direction.RIGHT)
                    if keys_pressed[pygame.K_LEFT]:
                        block1.move(Direction.LEFT)
                    j = 0
                else:
                    j += 1
                if keys_pressed[pygame.K_DOWN]:
                    block1.move(Direction.DOWN)
            else:
                while delete_line():
                    score += 1
                    pygame.draw.rect(screen, (0, 0, 0), (425, 500, 140, 60))
                    score_text2 = score_font2.render(str(score), True, (255, 255, 255))
                    screen.blit(score_text2, (430, 505))
                block1 = Block(int(number_of_board_columns / 2 * MODULE_SIZE + LEFT_MARGIN), MODULE_SIZE +TOP_MARGIN, next_block_number)
                block1.draw()
                random_number = randint(1, 7)
                next_block_number = random_number
                next_block = Block(480, 130, next_block_number)
                pygame.draw.rect(screen, (0, 0, 0), (425, 100, 140, 135))
                next_block.draw()


if __name__ == "__main__":
    main()
