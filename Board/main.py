import sys
import pygame
from copy import deepcopy
import typing
import pygame_menu
import json


class Game:

    def __init__(self):
        pygame.init()
        self.size = pygame.display.get_desktop_sizes()[0]
        self.fps = 60
        self.game_name = "Our game"
        self.scene = 0
        self.init_ui()
        self.start()

    def init_ui(self):
        x = self.size[0]
        y = self.size[0]
        self.ui_controller = UIController()
        self.button_editor = Button(self.ui_controller, "Редактор", lambda: self.set_scene(1), (x // 2 - 50,
                                                                                                y // 2 - 10),
                                    (x // 2 + 50, y // 2 - 60))

    def set_scene(self, id):
        self.scene = id

    def start(self):
        screen = pygame.display.set_mode(flags=pygame.FULLSCREEN)
        pygame.display.set_caption(self.game_name)
        pygame.display.flip()
        clock = pygame.time.Clock()
        running = True
        # menu = pygame_menu.menu.Menu(Game.GameName, width, height, pygame_menu.themes.THEME_DEFAULT)
        # menu.mainloop(screen)
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    self.get_key_down(event.key)
                elif event.type == pygame.KEYUP:
                    self.get_key_up(event.key)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.get_mouse_down(event.button, event.pos)
            screen.fill((0, 0, 0))
            self.update()
            pygame.display.flip()
            clock.tick(self.fps)
        pygame.quit()

    def update(self):
        if self.scene == 0:
            self.draw_menu()
        elif self.scene == 1:
            self.draw_editor()
        elif self.scene == 2:
            pass

    def draw_menu(self):
        pass

    def draw_editor(self):
        pass

    def get_key_down(self, key: pygame):
        pass

    def get_key_up(self, key):
        pass

    def get_mouse_down(self, key, pos):
        pass


class UIController:

    def __init__(self, screen):
        self.elements = []
        self.screen = screen

    def update(self):
        for element in self.elements:
            element.update(self.screen)


class UIElement:

    def __init__(self, controller):
        self.controller = controller

    def update(self, screen):
        self.draw(screen)

    def draw(self, screen):
        pass


class Button(UIElement):

    def __init__(self, controller, text, function, pos1, pos2, color):
        super(Button, self).__init__(controller)
        self.text = text
        self.function = function
        self.pos1 = pos1
        self.pos2 = pos2
        self.color = color

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, pygame.Rect(screen.))

    def get_click(self, pos):
        if (self.pos1[0] <= pos[0] <= self.pos2[0]) and (self.pos1[1] <= pos[1] <= self.pos2[1]):
            self.function()


class TestMenu:

    def __init__(self, menu, screen):
        self.menu = menu
        self.menu.mainloop(screen)


class Menu:

    def __init__(self, screen: pygame.Surface, width: int, height: int):
        self.main = pygame_menu.Menu(Game.GameName, width, height, pygame_menu.themes.THEME_BLUE)
        self.main.mainloop(screen)
        self.pause_menu = pygame_menu.Menu(Game.GameName, width, height, pygame_menu.themes.THEME_GREEN)
        self.editor = pygame_menu.Menu(Game.GameName, width, height, pygame_menu.themes.THEME_SOLARIZED)
        self.playing = pygame_menu.Menu(Game.GameName, width, height, pygame_menu.themes.THEME_DEFAULT)
        self.menus = (self.main, self.pause_menu, self.editor, self.playing)
        self.current_scene = self.main
        self.screen = screen

        self.init_main()
        self.init_pause_menu()
        self.init_editor()
        self.init_playing()

        self.switch(self.main)

    def init_main(self):
        self.main.mainloop(self.screen)
        self.main.add.label(Game.GameName)

    def init_pause_menu(self):
        self.pause_menu.mainloop(self.screen)
        pass

    def init_editor(self):
        self.editor.mainloop(self.screen)
        pass

    def init_playing(self):
        self.playing.mainloop(self.screen)
        pass

    def switch(self, menu: pygame_menu.Menu):
        for m in self.menus:
            m.disable()
        menu.enable()

    def pause(self):
        self.switch(self.playing)

    def unpause(self):
        self.switch(self.current_scene)

    def quit(self):
        pygame.quit()


class Level:
    pass


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

    def serialize(self) -> str:
        pass


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

    def serialize(self) -> str:
        json.dump()


# pygame.init()
# size = width, height = 1600, 900
# screen = pygame.display.set_mode(size)
# pygame.display.set_caption("Game")
# pygame.display.flip()
# clock = pygame.time.Clock()
# FPS = 60
#
#
# game_field = GameField(25, 25)
# game_field.set_view(10, 10, 32)
# game_field.inventory.set_view(10, 32 * 25 + 20, 32)
# player = Player(12, 12, game_field, "textures/player.png")
# game_field.inventory.board[0][0] = Block(0, 0, game_field.inventory, "textures/bricks.png")
#
# running = True
#
# while running:
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             running = False
#         elif event.type == pygame.MOUSEBUTTONDOWN:
#             if event.button == 1:
#                 game_field.get_click(event.pos)
#         elif event.type == pygame.KEYUP:
#             if event.key == 32:
#                 pause = not pause
#                 if pause:
#                     FPS = 60
#                 else:
#                     FPS = 10
#     screen.fill((0, 0, 0))
#
#     game_field.render(screen)
#     pygame.display.flip()
#     clock.tick(FPS)
#
# pygame.quit()


game = Game()
