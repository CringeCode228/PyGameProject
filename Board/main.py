import pygame
import json
from UI import *
from Scenes import *
from Boards import *
from GameObjects import *


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


class Level:

    def __init__(self):
        self.objects = []


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
