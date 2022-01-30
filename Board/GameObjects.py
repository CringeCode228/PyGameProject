import pygame
from Boards import *
import json


class GameObject(pygame.sprite.Sprite):

    def __init__(self, x, y, board, texture: str, collide=False):
        super(GameObject, self).__init__(board.objects)
        self.x = x
        self.y = y
        self.game_field = board
        if type(self.game_field) == GameField:
            self.game_field.board[x][y] = self
        else:
            self.game_field.board[y][x] = self
        self.collide = collide
        self.image = pygame.image.load(texture)
        self.image = pygame.transform.scale(self.image, (self.game_field.cell_size - 1, self.game_field.cell_size - 1))
        self.texture = texture
        self.rect = self.image.get_rect()
        self.rect.left = self.game_field.left + self.game_field.cell_size * x + 1
        self.rect.top = self.game_field.top + self.game_field.cell_size * y + 1

        self.screen = board.screen
        # if texture:
        #     self.texture = pygame.image.load(texture)
        #     self.texture = pygame.transform.scale(self.texture, (self.game_field.cell_size - 2,
        #                                                          self.game_field.cell_size - 2))
        # else:
        #     self.texture = pygame.Surface((self.game_field.cell_size - 2, self.game_field.cell_size - 2))
        # self.game_field.board[x][y] = self

    def update(self):
        pass

    def render(self):
        self.screen.blit(self.texture, (self.game_field.left + self.x * self.game_field.cell_size + 1,
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

    def clone(self, x, y, board):
        pass


class Player(GameObject, pygame.sprite.Sprite):

    def __init__(self, board: GameField, texture: str):
        super(Player, self).__init__(x, y, board, texture)
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
        super(Block, self).__init__(x, y, board, texture, True)

    @staticmethod
    def get_id():
        return 0

    def serialize(self):
        return json.dumps({"id": self.get_id(), "pos": [self.x, self.y], "texture": self.texture})

    def clone(self, x, y, board):
        return Block(x, y, board, self.texture)

    # def deserialize(self, data):
        # pass
        # return Block(data["pos"][0], data["pos"][1])
