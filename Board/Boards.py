import pygame


class Board:
    # создание поля
    def __init__(self, screen: pygame.Surface, width, height):
        self.width = width
        self.height = height
        self.board = [[0] * width for _ in range(height)]
        # значения по умолчанию
        self.left = 10
        self.top = 10
        self.cell_size = 100
        self.screen = screen

    # настройка внешнего вида
    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def render(self):
        for i in range(self.width + 1):
            pygame.draw.line(self.screen, pygame.Color(255, 255, 255), (self.left + i * self.cell_size, self.top),
                             (self.left + i * self.cell_size, self.top + self.height * self.cell_size))
        for i in range(self.height + 1):
            pygame.draw.line(self.screen, pygame.Color(255, 255, 255), (self.left, self.top + i * self.cell_size),
                             (self.left + self.width * self.cell_size, self.top + i * self.cell_size))

    def get_cell(self, mouse_pos):
        x, y = mouse_pos
        cell = ((x - self.left) // self.cell_size, (y - self.top) // self.cell_size)
        if (0 <= cell[0] <= self.width) and (0 <= cell[1] <= self.height):
            return cell
        else:
            return None

    def on_click(self, cell_coords):
        pass

    def get_click(self, mouse_pos):
        cell = self.get_cell(mouse_pos)
        if cell:
            self.on_click(self.get_cell(mouse_pos))


class GameField(Board):

    def __init__(self, screen, width, height, inventory):
        super(GameField, self).__init__(screen, width, height)
        self.inventory = inventory
        # for i in range(width):
        #     for j in range(height):
        #         self.board[i][j] = GameObject(self, i, j, None)
        self.fon = pygame.image.load("textures\\stone.png")
        self.fon = pygame.transform.scale(self.fon, (self.cell_size, self.cell_size))

    def render(self):
        for i in range(self.width):
            for j in range(self.height):
                self.screen.blit(self.fon, (self.left + self.cell_size * i, self.top + self.cell_size * j))
        self.screen.blit(self.fon, (self.left, self.top))
        super(GameField, self).render()

        # super(GameField, self).render(self.screen)
        # for i in range(self.width):
        #     for j in range(self.height):
        #         self.board[i][j].render(self.screen)
        # self.inventory.render(self.screen)

    def on_click(self, cell_coords):
        self.board[cell_coords[0]][cell_coords[1]] = self.inventory.board[self.inventory.active_cell].clone()

        # if type(self.board[cell_coords[0]][cell_coords[1]]) != Player:
        #     self.board[cell_coords[0]][cell_coords[1]] = GameObject(self, cell_coords[0], cell_coords[1],
        #                                                             "textures/bricks.png", True)

    def set_view(self, left, top, cell_size):
        super(GameField, self).set_view(left, top, cell_size)
        self.fon = pygame.transform.scale(self.fon, (self.cell_size, self.cell_size))


class GameFieldInventory(Board):

    def __init__(self, screen, width):
        super(GameFieldInventory, self).__init__(screen, width, 1)
        self.active_cell = 0

    def on_click(self, cell_coords):
        self.active_cell = cell_coords[0]

    def render(self):
        super(GameFieldInventory, self).render()
        # for i in range(self.width):
        #     self.board[0][0].render(self.screen)
