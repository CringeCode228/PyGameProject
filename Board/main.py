import sys
import pygame
from copy import deepcopy


class Board:
    # создание поля
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = [[0] * width for _ in range(height)]
        # значения по умолчанию
        self.left = 10
        self.top = 10
        self.cell_size = 100

    # настройка внешнего вида
    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def render(self, screen: pygame.Surface):
        for i in range(self.width):
            for j in range(self.height):
                pygame.draw.rect(screen, pygame.Color(255, 255, 255), pygame.Rect(i * self.cell_size + self.left,
                                                                                  j * self.cell_size + self.top,
                                                                                  self.cell_size, self.cell_size), 1)

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

    def __init__(self, width, height):
        super(GameField, self).__init__(width, height)
        self.inventory = GameFieldInventory(10)
        for i in range(width):
            for j in range(height):
                self.board[i][j] = GameObject(self, i, j, None)

    def render(self, screen: pygame.Surface):
        super(GameField, self).render(screen)
        for i in range(self.width):
            for j in range(self.height):
                self.board[i][j].render(screen)
        self.inventory.render(screen)

    def on_click(self, cell_coords):
        if type(self.board[cell_coords[0]][cell_coords[1]]) != Player:
            self.board[cell_coords[0]][cell_coords[1]] = GameObject(self, cell_coords[0], cell_coords[1],
                                                                    "textures/bricks.png", True)


class GameFieldInventory(Board):

    def __init__(self, width):
        super(GameFieldInventory, self).__init__(width, 1)
        self.active_cell = 0

    def on_click(self, cell_coords):
        self.active_cell = cell_coords[0]

    def render(self, screen: pygame.Surface):
        super(GameFieldInventory, self).render(screen)
        for i in range(self.width):
            self.board[0][0].render(screen)


class GameObject:

    def __init__(self, board: Board, x: int, y: int, texture: str, collide=False):
        self.x = x
        self.y = y
        self.game_field = board
        self.collide = collide
        if texture:
            self.texture = pygame.image.load(texture)
            self.texture = pygame.transform.scale(self.texture, (self.game_field.cell_size - 2,
                                                                 self.game_field.cell_size - 2))
        else:
            self.texture = pygame.Surface((self.game_field.cell_size - 2, self.game_field.cell_size - 2))
        self.game_field.board[x][y] = self

    def render(self, screen):
        screen.blit(self.texture, (self.game_field.left + self.x * self.game_field.cell_size + 1,
                                   self.game_field.top + self.y * self.game_field.cell_size + 1))

    def set_coords(self, x, y):
        self.x = x
        self.y = y
        self.game_field.board[x][y] = self


class Player(GameObject):

    def __init__(self, x: int, y: int, board: GameField, texture: str):
        super(Player, self).__init__(board, x, y, texture)
        self.rotate = 0

    def move(self, direction: int):
        if direction == 0:
            if not self.game_field.board[self.x - 1][self.y].collide:
                self.x -= 1
                if self.rotate == 1:
                    pygame.transform.flip(self.texture, False, True)
                self.rotate = 0
        elif direction == 0:
            if not self.game_field.board[self.x + 1][self.y].collide:
                self.x += 1
                if self.rotate == 0:
                    pygame.transform.flip(self.texture, False, True)
                self.rotate = 1
        elif direction == 0:
            if not self.game_field.board[self.x][self.y - 1].collide:
                self.y -= 1
        elif direction == 0:
            if not self.game_field.board[self.x][self.y + 1].collide:
                self.y += 1


class Block(GameObject):

    def __init__(self, x, y, board, texture: str):
        super(Block, self).__init__(board, x, y, texture, True)


pygame.init()
size = width, height = 1600, 900
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Game")
pygame.display.flip()
clock = pygame.time.Clock()
FPS = 60


game_field = GameField(25, 25)
game_field.set_view(10, 10, 32)
game_field.inventory.set_view(10, 32 * 25 + 20, 32)
player = Player(12, 12, game_field, "textures/player.png")
game_field.inventory.board[0][0] = Block(0, 0, game_field.inventory, "textures/bricks.png")

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                game_field.get_click(event.pos)
        elif event.type == pygame.KEYUP:
            if event.key == 32:
                pause = not pause
                if pause:
                    FPS = 60
                else:
                    FPS = 10
    screen.fill((0, 0, 0))

    game_field.render(screen)
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
