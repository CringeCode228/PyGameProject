import pygame
import json


class Game:

    def __init__(self):
        pygame.init()
        self.fps = 60
        self.game_name = "Our game"
        self.current_scene = 0
        self.running = True
        self.screen = pygame.display.set_mode(flags=pygame.FULLSCREEN)
        menu = Menu(self)
        editor = Editor(self)
        levels = Levels(self)
        self.scenes = [menu, editor, levels]
        self.start()

    def stop(self):
        self.running = False

    def set_scene(self, id):
        self.current_scene = id
        self.scenes[self.current_scene].restart()

    def start(self):
        pygame.display.set_caption(self.game_name)
        pygame.display.flip()
        clock = pygame.time.Clock()
        # menu = pygame_menu.menu.Menu(Game.GameName, width, height, pygame_menu.themes.THEME_DEFAULT)
        # menu.mainloop(screen)
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    self.get_key_down(event.key)
                elif event.type == pygame.KEYUP:
                    self.get_key_up(event.key)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.get_mouse_down(event.button, event.pos)
            self.screen.fill((0, 0, 0))
            self.update()
            pygame.display.flip()
            clock.tick(self.fps)
        pygame.quit()

    def update(self):
        self.scenes[self.current_scene].update()

    def get_key_down(self, key):
        self.scenes[self.current_scene].get_key_down(key)

    def get_key_up(self, key):
        self.scenes[self.current_scene].get_key_up(key)

    def get_mouse_down(self, key, pos):
        self.scenes[self.current_scene].get_mouse_down(key, pos)


class UIController:

    def __init__(self, screen):
        self.elements = []
        self.screen = screen
        self.width = self.screen.get_width()
        self.height = self.screen.get_height()

    def update(self):
        for element in self.elements:
            element.update()

    def get_click(self, pos):
        for element in self.elements:
            element.get_click(pos)


class UIElement:

    def __init__(self, controller):
        self.controller = controller
        self.controller.elements.append(self)

    def update(self):
        self.draw()

    def draw(self):
        pass

    def get_click(self, pos):
        pass


class Button(UIElement):

    def __init__(self, controller, text, function, pos1, pos2, color):
        super(Button, self).__init__(controller)
        self.text = text
        self.function = function
        self.pos1 = pos1
        self.pos2 = pos2
        self.color = color
        self.rect = pygame.Rect(pos1, (pos2[0] - pos1[0], pos2[1] - pos1[1]))

    def draw(self):
        pygame.draw.rect(self.controller.screen, self.color, pygame.Rect(self.pos1[0], self.pos1[1],
                                                                         self.pos2[0] - self.pos1[0],
                                                                         self.pos2[1] - self.pos1[1]))
        font = pygame.font.SysFont("Arial", (self.pos2[1] - self.pos1[1]) // 2)
        self.controller.screen.blit(font.render(self.text, True, pygame.Color(0, 0, 0)), self.pos1)

    def get_click(self, pos):
        if self.rect.collidepoint(pos):
            self.function()


class List(UIElement):

    def __init__(self, controller, pos1, pos2, color):
        super(List, self).__init__(controller)
        self.elements = [ListElement(self, "Test"), ListElement(self, "Test2"), ListElement(self, "Test3")]
        self.pos1 = pos1
        self.pos2 = pos2
        self.color = color
        self.current_page = 0
        self.rect = pygame.Rect(pos1, (pos2[0] - pos1[0], pos2[1] - pos1[1]))

    def previous_page(self):
        self.current_page -= 1

    def next_page(self):
        self.current_page += 1

    def draw(self):
        pygame.draw.rect(self.controller.screen, self.color, self.rect, 1)
        for i in range(10):
            try:
                font = pygame.font.SysFont("Arial", self.rect.height // 10)
                self.controller.screen.blit(font.render(self.elements[self.current_page * 10 + i].text, True,
                                                        self.color),
                                                        (self.pos1[0] + 5, self.pos1[1] + i * self.rect.height // 10))
                pygame.draw.line(self.controller.screen, self.color, (self.pos1[0],
                                                                      self.pos1[1] + self.rect.height // 10 * (i + 1)),
                                 (self.pos1[0] + self.rect.width - 1, self.pos1[1] + self.rect.height // 10 * (i + 1)))
            except IndexError:
                pass

    def get_click(self, pos):
        if self.rect.collidepoint(pos):
            pass


class ListElement(UIElement):

    def __init__(self, list, text, function=lambda: None):
        super(ListElement, self).__init__(list.controller)
        self.text = text
        self.function = function


class Level:

    def __init__(self):
        self.objects = []


class Scene:

    def __init__(self, game):
        self.game = game

    def update(self):
        pass

    def get_key_down(self, key):
        pass

    def get_key_up(self, key):
        pass

    def get_mouse_down(self, key, pos):
        pass

    def restart(self):
        pass


class Menu(Scene):

    def __init__(self, game):
        super(Menu, self).__init__(game)
        x = self.game.screen.get_width()
        y = self.game.screen.get_height()
        self.ui_controller = UIController(self.game.screen)
        button_editor = Button(self.ui_controller, "Редактор", lambda: self.game.set_scene(1),
                               (x // 2 - 50, y // 2 - 60),
                               (x // 2 + 50, y // 2 - 10), pygame.Color(255, 255, 255))
        button_quit = Button(self.ui_controller, "Выход", lambda: self.game.stop(),
                             (x // 2 - 50, y // 2 + 10),
                             (x // 2 + 50, y // 2 + 60), pygame.Color(255, 255, 255))
        button_levels = Button(self.ui_controller, "Уровни", lambda: self.game.set_scene(2),
                               (x // 2 - 50, y // 2 + 70),
                               (x // 2 + 50, y // 2 + 120), pygame.Color(255, 255, 255))

    def update(self):
        self.ui_controller.update()

    def get_mouse_down(self, key, pos):
        if key == 1:
            self.ui_controller.get_click(pos)


class Editor(Scene):

    def __init__(self, game):
        super(Editor, self).__init__(game)
        self.is_playing = False

        x = self.game.screen.get_width()
        y = self.game.screen.get_height()
        self.ui_controller = UIController(self.game.screen)
        button_quit_editor = Button(self.ui_controller, "Назад", lambda: self.quit_editor(),
                                    (x - 100, y - 50),
                                    (x - 10, y - 10), pygame.Color(255, 255, 255))

        button_play = Button(self.ui_controller, "Играть", lambda: self.is_playing != self.is_playing,
                             (x - 100, 10),
                             (x - 10, 50), pygame.Color(255, 255, 255))
        self.board = GameField(self.game.screen, 10, 10)
        self.board.set_view(10, 10, 50)
        self.inventory = GameFieldInventory(self.game.screen, 10)
        self.inventory.set_view(10, 50 * 11 + 10, 50)

    def restart(self):
        self.is_playing = False

    def quit_editor(self):
        self.is_playing = False
        self.game.set_scene(0)

    def update(self):
        self.ui_controller.update()
        self.board.render()
        self.inventory.render()

    def get_key_down(self, key):
        if key == pygame.K_w:
            pass

    def get_mouse_down(self, key, pos):
        if key == 1:
            self.ui_controller.get_click(pos)
            self.board.get_click(pos)
            self.inventory.get_click(pos)


class Levels(Scene):

    def __init__(self, game):
        super(Levels, self).__init__(game)
        x = self.game.screen.get_width()
        y = self.game.screen.get_height()
        self.ui_controller = UIController(self.game.screen)
        button_quit = Button(self.ui_controller, "Назад", lambda: self.game.set_scene(0),
                             (x - 100, 10),
                             (x - 10, 60), pygame.Color(255, 255, 255))
        list_levels = List(self.ui_controller, (100, 100), (x - 100, y - 100), pygame.Color(255, 255, 255))

    def update(self):
        self.ui_controller.update()

    def get_mouse_down(self, key, pos):
        if key == 1:
            self.ui_controller.get_click(pos)


class Board:
    # создание поля
    def __init__(self, screen, width, height):
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

    def __init__(self, screen, width, height):
        super(GameField, self).__init__(screen, width, height)
        # for i in range(width):
        #     for j in range(height):
        #         self.board[i][j] = GameObject(self, i, j, None)

    def render(self):
        super(GameField, self).render()

        # super(GameField, self).render(self.screen)
        # for i in range(self.width):
        #     for j in range(self.height):
        #         self.board[i][j].render(self.screen)
        # self.inventory.render(self.screen)

    def on_click(self, cell_coords):
        pass
        # if type(self.board[cell_coords[0]][cell_coords[1]]) != Player:
        #     self.board[cell_coords[0]][cell_coords[1]] = GameObject(self, cell_coords[0], cell_coords[1],
        #                                                             "textures/bricks.png", True)


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


class GameObject(pygame.sprite.Sprite):

    def __init__(self, board: Board, x: int, y: int, texture: str, collide=False):
        super(GameObject, self).__init__(self)
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

    @staticmethod
    def get_id():
        return -1

    def serialize(self):
        pass

    def deserialize(self):
        pass


class Player(GameObject, pygame.sprite.Sprite):

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

    @staticmethod
    def get_id():
        return 1


class Block(GameObject):

    def __init__(self, x, y, board, texture: str):
        super(Block, self).__init__(board, x, y, texture, True)

    @staticmethod
    def get_id():
        return 0

    def serialize(self):
        return json.dumps({"id": self.get_id(), "pos": [self.x, self.y], "texture": self.texture})

    def deserialize(self, data):
        pass
        # return Block(data["pos"][0], data["pos"][1])





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
