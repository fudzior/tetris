import pygame

pygame.init()

# 0. Ustawienia poczatkowe:

# 0.0 Ustawienia okna:

#logo = pygame.image.load("tetris_logo.png")
#pygame.display.set_icon(logo)
pygame.display.set_caption("Tetris Gosi")

screen = pygame.display.set_mode(size=(500, 500))

# 0.1 Tworzenie siatki obszaru gry

number_of_board_columns = 10
number_of_board_rows = 10

x, y, s = 0, 0, 0

board = [[[x, y, s]] * number_of_board_columns for i in range(number_of_board_rows)]

for row in range(number_of_board_rows):
    for column in range(number_of_board_columns):
        x = column * 50
        y = row * 50
        board[row][column] = [x, y, s]


# 0.2 Tworzenie modulu (kwadracika)

class Module:
    def __init__(self, x_module, y_module):
        self.x_module = x_module
        self.y_module = y_module

    def draw(self):
        pygame.draw.rect(screen, (255, 255, 255), (self.x_module, self.y_module, 50, 50))
        # full_or_empty_module = 1
        # return full_or_empty_module

    def remove(self):
        pygame.draw.rect(screen, (0, 0, 0), (self.x_module, self.y_module, 50, 50))
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
                    x_module = self.x_block - 50 + column * 50
                    y_module = self.y_block - 50 + row * 50
                    module = Module(x_module, y_module)
                    self.modules_xy[i][0] = x_module
                    self.modules_xy[i][1] = y_module
                    i += 1
                    module.draw()
                pygame.display.update()
        return self.modules_xy

    def rotate(self):
        shape_rotated = [[0] * self.size_of_block for i in range(self.size_of_block)]

        block_I_copy = [[0, 1, 0, 0],
                        [0, 1, 0, 0],
                        [0, 1, 0, 0],
                        [0, 1, 0, 0]]

        block_I_90deg = [[0, 0, 0, 0],
                         [1, 1, 1, 1],
                         [0, 0, 0, 0],
                         [0, 0, 0, 0]]

        block_I_270deg = [[0, 0, 1, 0],
                          [0, 0, 1, 0],
                          [0, 0, 1, 0],
                          [0, 0, 1, 0]]

        # sprawdzanie czy czesc shape z "0" wykracza poza plansze:
        if not self.block_set:
            if self.x_block < 50:
                self.move(0)
                if self.shape == block_I_270deg:
                    self.move(0)
            if self.x_block > 500 - (self.size_of_block - 1) * 50:
                self.move(2)
                if self.shape == block_I_copy:
                    self.move(2)
            if self.y_block > 500 - (self.size_of_block - 1) * 50:
                self.move(3)
                if self.shape == block_I_90deg:
                    self.move(3)

            for row in range(self.size_of_block):
                for column in range(self.size_of_block):
                    shape_rotated[column][self.size_of_block - row - 1] = self.shape[row][column]
            for row in range(self.size_of_block):
                for column in range(self.size_of_block):
                    self.shape[row][column] = shape_rotated[row][column]
            self.remove()
            self.draw()

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
            if direction == 0: #RIGHT
                for row in range(4):
                    if self.modules_xy[row][0] + 50 > 450:
                        collision = True
                if not collision:
                    for row in range(4):
                        modules_xy_moved[row][0] = self.modules_xy[row][0] + 50
                        modules_xy_moved[row][1] = self.modules_xy[row][1]
                    self.remove()
                    draw_moved_block()
                    self.x_block += 50
            elif direction == 1: #DOWN
                for row in range(4):
                    if self.modules_xy[row][1] + 50 > 450:
                        self.block_set = True
                        self.do_after_block_set()
                if not self.block_set:
                    for row in range(4):
                        modules_xy_moved[row][0] = self.modules_xy[row][0]
                        modules_xy_moved[row][1] = self.modules_xy[row][1] + 50
                    self.remove()
                    draw_moved_block()
                    self.y_block += 50
            elif direction == 2: #LEFT
                for row in range(4):
                    if self.modules_xy[row][0] - 50 < 0:
                        collision = True
                if not collision:
                    for row in range(4):
                        modules_xy_moved[row][0] = self.modules_xy[row][0] - 50
                        modules_xy_moved[row][1] = self.modules_xy[row][1]
                    self.remove()
                    draw_moved_block()
                    self.x_block -= 50
            elif direction == 3:  # UP tylko do uzycia w funkcji self.rotate()
                for row in range(4):
                    if self.modules_xy[row][1] - 50 < 0:
                        collision = True
                if not collision:
                    for row in range(4):
                        modules_xy_moved[row][0] = self.modules_xy[row][0]
                        modules_xy_moved[row][1] = self.modules_xy[row][1] - 50
                    self.remove()
                    draw_moved_block()
                    self.y_block -= 50

# 1. losowanie klocka, ktory zaraz spadnie

L1 = Block(100, 100, block_I)
L1.draw()

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
                L1.rotate()
            if event.key == pygame.K_RIGHT:
                L1.move(0)
            if event.key == pygame.K_DOWN:
                L1.move(1)
            if event.key == pygame.K_LEFT:
                L1.move(2)
            if event.key == pygame.K_UP:
                L1.move(3)
