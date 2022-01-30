import pygame
from UI import *
from Boards import *
from GameObjects import *


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
        self.inventory = GameFieldInventory(self.game.screen, 3)
        self.inventory.set_view(10, 50 * 11 + 10, 50)
        self.board = GameField(self.game.screen, 10, 10, self.inventory)
        self.board.set_view(10, 10, 50)
        Block(0, 0, self.inventory, "textures\\bricks.png")
        Block(1, 0, self.inventory, "textures\\wood.png")
        Block(2, 0, self.inventory, "textures\\grass.png")

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
            self.board.get_click(pos, key)
            self.inventory.get_click(pos, key)
        elif key == 3:
            self.board.get_click(pos, key)


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
        list_levels.elements.extend([ListElement(list_levels, "Test", lambda: print("1")),
                                     ListElement(list_levels, "Test2", lambda: print("2")),
                                     ListElement(list_levels, "Устнове собеседование", lambda: print("3"))])
        button_previous = Button(self.ui_controller, "Предыдущая страница", lambda: list_levels.previous_page(),
                                 (10, y - 60),
                                 (250, y - 10), pygame.Color(255, 255, 255))
        button_next = Button(self.ui_controller, "Следующая страница", lambda: list_levels.next_page(),
                             (x - 250, y - 60),
                             (x - 10, y - 10), pygame.Color(255, 255, 255))

    def update(self):
        self.ui_controller.update()

    def get_mouse_down(self, key, pos):
        if key == 1:
            self.ui_controller.get_click(pos)
