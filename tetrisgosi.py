import pygame
from enum import Enum
from random import randint
import numpy as np
from PIL import Image
import colorsys

pygame.init()


class Direction(Enum):
    RIGHT = 0
    DOWN = 1
    LEFT = 2
    UP = 3


class Color(Enum):
    RED = 5
    CYAN = 3
    BLUE = 2
    ORANGE = 1
    YELLOW = 7
    MAGENTA = 4
    GREEN = 6


BOARD_WIDTH = 360
BOARD_HEIGHT = 540
MODULE_SIZE = 30
TOP_MARGIN = 30
LEFT_MARGIN = 30
LINE_THICK = 4
SCREEN_SIZE = 600


def prepare_window(screen):
    logo = pygame.image.load("tetris_logo.png")
    pygame.display.set_icon(logo)
    pygame.display.set_caption("Tetris Gosi")

    pygame.draw.rect(screen, (255, 255, 255), (
        LEFT_MARGIN - LINE_THICK, TOP_MARGIN - LINE_THICK, int(BOARD_WIDTH + 1.5 * LINE_THICK),
        int(BOARD_HEIGHT + 1.5 * LINE_THICK)), LINE_THICK)
    pygame.draw.rect(screen, (255, 255, 255), (420, 450, 150, 120), LINE_THICK)
    pygame.draw.rect(screen, (255, 255, 255), (420, 30, 150, 210), LINE_THICK)

    score_font = pygame.font.SysFont('Arial', 30)
    score_text = score_font.render('Your score:', True, (255, 255, 255))
    screen.blit(score_text, (430, 460))

    help_font = pygame.font.SysFont('Arial', 20)
    help_text = help_font.render('Press space to rotate', True, (255, 255, 255))
    screen.blit(help_text, (415, 255))
    help_text1 = help_font.render('Press arrows to move', True, (255, 255, 255))
    screen.blit(help_text1, (415, 285))

    next_block_text = score_font.render('Next block:', True, (255, 255, 255))
    screen.blit(next_block_text, (435, 40))


number_of_board_columns = BOARD_WIDTH // MODULE_SIZE
number_of_board_rows = BOARD_HEIGHT // MODULE_SIZE

board = np.empty((number_of_board_rows, number_of_board_columns, 3), int)
screen = pygame.display.set_mode(size=(SCREEN_SIZE, SCREEN_SIZE))

for row in range(number_of_board_rows):
    for column in range(number_of_board_columns):
        x = column * MODULE_SIZE + LEFT_MARGIN
        y = row * MODULE_SIZE + TOP_MARGIN
        s = 0
        board[row][column] = [x, y, s]


img = Image.open('module2.jpg')
img = img.resize((30, 30), Image.ANTIALIAS)
img.save('module.png')


def make_color_module_image(color):
    pil_module = Image.open("module.png")
    pil_module = pil_module.convert('RGB')
    pixel_array_module = np.array(pil_module, int)

    rgb_to_hls = np.vectorize(colorsys.rgb_to_hls)
    hls_to_rgb = np.vectorize(colorsys.hls_to_rgb)

    red, green, blue = pixel_array_module.T
    hue, light, saturation = rgb_to_hls(red, green, blue)

    def switch_color_hue(color):
        switcher = {
            1: 150,
            2: -60,
            3: 0,
            4: -110,
            5: 180,
            6: 70,
            7: 120
        }
        return switcher.get(color, 180)

    hue_value = switch_color_hue(color)
    hue = (180 - hue_value) / 360.0
    red, green, blue = hls_to_rgb(hue, light, saturation)
    module_array = np.dstack((red, green, blue))

    module_pil = Image.fromarray(module_array.astype('int8'), 'RGB')
    module_pil_rot270 = module_pil.rotate(270)
    file_name = (str(Color(color).name)).lower() + ".jpg"
    module_pil_rot270.save(file_name)


files = np.empty(8, pygame.Surface)

for color in range(1, 8):
    make_color_module_image(color)
    files[color] = pygame.image.load((str(Color(color).name)).lower() + ".jpg")


def draw_module(x_module, y_module, color):
    screen.blit(files[color], [x_module, y_module])


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
        self.modules_xy = np.empty((4, 3), int)
        self.block_set = False

    def do_after_block_set(self):
        for row in range(number_of_board_rows):
            for column in range(number_of_board_columns):
                for i in range(4):
                    if (self.modules_xy[i] == board[row][column]).all():
                        board[row][column][2] = self.number
        self.block_set = True

    def remove(self):
        for row in range(4):
            x_module = self.modules_xy[row][0]
            y_module = self.modules_xy[row][1]
            remove_module(x_module, y_module)
        pygame.display.update()

    def draw(self):  # uproszczona draw_new_block nie powoduje zacinania gry i wyswietla od razu nowy block
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

    def draw_new_block(self):
        i = 0
        for row in range(self.size_of_block):
            for column in range(number_of_board_columns // 2 - 3, number_of_board_columns // 2 + 3):
                for row1 in range(self.size_of_block):
                    for column1 in range(self.size_of_block):
                        if self.shape[row1][column1] == 1:
                            x_module = self.x_block - MODULE_SIZE + column1 * MODULE_SIZE
                            y_module = self.y_block - MODULE_SIZE + row1 * MODULE_SIZE
                            if board[row][column][0] == x_module and board[row][column][1] == y_module and \
                                    board[row][column][2] == 0:
                                self.modules_xy[i][0] = x_module
                                self.modules_xy[i][1] = y_module
                                draw_module(x_module, y_module, self.number)
                                pygame.display.update()
                                i += 1
                            elif board[row][column][0] == x_module and board[row][column][1] == y_module and \
                                    board[row][column][2] != 0:
                                game_over = True
                                print("game over")
                                return game_over
        game_over = False
        return game_over

    def rotate(self):
        shape_rotated = np.empty((self.size_of_block, self.size_of_block), int)
        moved_right, moved_left, moved_up, moved_down = False, False, False, False

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

        # sprawdzanie czy czesc shape z "0" wykracza poza plansze:
        if not self.block_set:
            if self.x_block < MODULE_SIZE + LEFT_MARGIN:
                self.x_block += MODULE_SIZE
                moved_right = True
                if np.array_equal(self.shape, block_I_180deg):
                    self.x_block += MODULE_SIZE
            if self.x_block > BOARD_WIDTH + LEFT_MARGIN - (self.size_of_block - 1) * MODULE_SIZE:
                self.x_block -= MODULE_SIZE
                moved_left = True
                if np.array_equal(self.shape, block_I):  # tutaj zmiana
                    self.x_block -= MODULE_SIZE
            if self.y_block > BOARD_HEIGHT + TOP_MARGIN - (self.size_of_block - 1) * MODULE_SIZE:
                self.y_block -= MODULE_SIZE
                moved_up = True
                if np.array_equal(self.shape, block_I_90deg):
                    self.y_block -= MODULE_SIZE
            if self.y_block < MODULE_SIZE + TOP_MARGIN:
                self.y_block += MODULE_SIZE
                moved_down = True
                if np.array_equal(self.shape, block_I_270deg):
                    self.y_block += MODULE_SIZE

            collision = False
            i, x_rotated, y_rotated = 0, 0, 0
            modules_xy_rotated = np.empty((4, 3), int)

            shape_rotated = (np.flip(self.shape, axis=0)).T

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
                self.shape = np.copy(shape_rotated)
                self.modules_xy = np.copy(modules_xy_rotated)
                for i in range(4):
                    x_module = modules_xy_rotated[i][0]
                    y_module = modules_xy_rotated[i][1]
                    draw_module(x_module, y_module, self.number)
            else:
                if moved_right:
                    self.x_block -= MODULE_SIZE
                    if np.array_equal(self.shape, block_I_180deg):
                        self.x_block -= MODULE_SIZE
                elif moved_left:
                    self.x_block += MODULE_SIZE
                    if np.array_equal(self.shape, block_I):
                        self.x_block += MODULE_SIZE
                elif moved_up:
                    self.y_block += MODULE_SIZE
                    if np.array_equal(self.shape, block_I_90deg):
                        self.y_block += MODULE_SIZE
                elif moved_down:
                    self.y_block -= MODULE_SIZE
                    if np.array_equal(self.shape, block_I_270deg):
                        self.y_block -= MODULE_SIZE
            pygame.display.update()

    def move(self, direction):
        def draw_moved_block():
            self.modules_xy = np.copy(modules_xy_moved)
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
                y_module_in_full_line = row * MODULE_SIZE + TOP_MARGIN
                remove_module(x_module_in_full_line, y_module_in_full_line)
            for row_above_full_line in range(row, 0, -1):
                for column_above_full_line in range(number_of_board_columns):
                    if board[row_above_full_line - 1][column_above_full_line][2] != 0:
                        x_module_above_full_line = column_above_full_line * MODULE_SIZE + LEFT_MARGIN
                        y_module_target = row_above_full_line * MODULE_SIZE + TOP_MARGIN
                        y_module_to_place_on_target = (row_above_full_line - 1) * MODULE_SIZE + TOP_MARGIN
                        draw_module(x_module_above_full_line, y_module_target,
                                    board[row_above_full_line - 1][column_above_full_line][2])
                        remove_module(x_module_above_full_line, y_module_to_place_on_target)
                    board[row_above_full_line][column_above_full_line][2] = \
                        board[row_above_full_line - 1][column_above_full_line][2]
            pygame.display.update()
            return full_line


class Button:
    def __init__(self, is_on, x_button, y_button):
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


def do_after_game_over(score):
    pygame.draw.rect(screen, (0, 0, 0), (SCREEN_SIZE // 4, SCREEN_SIZE // 4, SCREEN_SIZE // 2, SCREEN_SIZE // 2))
    pygame.draw.rect(screen, (255, 255, 255), (
        SCREEN_SIZE // 4 + LEFT_MARGIN - LINE_THICK, SCREEN_SIZE // 4 + TOP_MARGIN - LINE_THICK,
        SCREEN_SIZE // 2 - 2 * LEFT_MARGIN - int(1.5 * LINE_THICK),
        SCREEN_SIZE // 2 - 2 * TOP_MARGIN - int(1.5 * LINE_THICK)), LINE_THICK)
    game_over_font = pygame.font.SysFont('Arial', 30)
    game_over_font_20 = pygame.font.SysFont('Arial', 20)
    game_over_text = game_over_font.render('GAME OVER', True, (255, 255, 255))
    screen.blit(game_over_text, (int(SCREEN_SIZE * 0.36), int(SCREEN_SIZE * 0.33)))
    score_game_over_text = game_over_font_20.render('Your score:', True, (255, 255, 255))
    screen.blit(score_game_over_text, (int(SCREEN_SIZE * 0.41), int(SCREEN_SIZE * 0.43)))
    score_game_over_text2 = game_over_font.render(str(score), True, (255, 255, 255))
    screen.blit(score_game_over_text2, (int(SCREEN_SIZE * 0.46), int(SCREEN_SIZE * 0.5)))
    pygame.display.update()


def main():
    screen = pygame.display.set_mode(size=(SCREEN_SIZE, SCREEN_SIZE))
    running = True
    game_over = False

    prepare_window(screen)

    random_number = randint(1, 7)
    next_block_number = randint(1, 7)

    next_block = Block(480, 130, next_block_number)
    next_block.draw()

    block = Block(number_of_board_columns // 2 * MODULE_SIZE + LEFT_MARGIN, MODULE_SIZE + TOP_MARGIN, random_number)
    block.draw()

    sound_button_x, sound_button_y, sound_button_size = 450, 330, 60
    sound_is_on = True
    sound_button = Button(sound_is_on, sound_button_x, sound_button_y)
    sound_button.draw()
    pygame.mixer.music.load('Checkie_Brown_-_01_-_Funky_Banane_Nightclub_ID_210.mp3')
    pygame.mixer.music.play(0)

    fall_time_ms = 1000

    pygame.time.set_timer(pygame.USEREVENT, fall_time_ms)

    score = 0
    score_font2 = pygame.font.SysFont('Arial', 40)
    score_text2 = score_font2.render(str(score), True, (255, 255, 255))
    screen.blit(score_text2, (430, 505))

    pygame.key.set_repeat(200, 100)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            mouse = pygame.mouse.get_pos()
            if sound_button_x < mouse[0] < sound_button_x + sound_button_size and sound_button_y < mouse[
                1] < sound_button_y + sound_button_size:
                sound_button.draw_pointed()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    sound_is_on = not sound_is_on
                    sound_button = Button(sound_is_on, sound_button_x, sound_button_y)
                    sound_button.draw()
            else:
                sound_button.draw()
            if not game_over:
                if not block.block_set:
                    if event.type == pygame.USEREVENT:
                        block.move(Direction.DOWN)
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:
                            block.rotate()
                        if event.key == pygame.K_RIGHT:
                            block.move(Direction.RIGHT)
                        if event.key == pygame.K_LEFT:
                            block.move(Direction.LEFT)
                        if event.key == pygame.K_DOWN:
                            block.move(Direction.DOWN)
                else:
                    while delete_line():
                        score += 1
                        pygame.draw.rect(screen, (0, 0, 0), (425, 500, 140, 60))
                        score_text2 = score_font2.render(str(score), True, (255, 255, 255))
                        screen.blit(score_text2, (430, 505))
                    block = Block(number_of_board_columns // 2 * MODULE_SIZE + LEFT_MARGIN, MODULE_SIZE + TOP_MARGIN,
                                   next_block_number)
                    game_over = block.draw_new_block()
                    random_number = randint(1, 7)
                    next_block_number = random_number
                    next_block = Block(480, 130, next_block_number)
                    pygame.draw.rect(screen, (0, 0, 0), (425, 100, 140, 135))
                    next_block.draw()
                    if score%5 == 0 and score!=0:
                        if fall_time_ms > 200:
                            fall_time_ms -= 100
                            pygame.time.set_timer(pygame.USEREVENT, fall_time_ms)
                        elif fall_time_ms > 10:
                            fall_time_ms -=10
                            pygame.time.set_timer(pygame.USEREVENT, fall_time_ms)
            else:
                do_after_game_over(score)


if __name__ == "__main__":
    main()
