import pygame


class Utilities:

    @staticmethod
    def clamp(value, minimum, maximum):
        return max(minimum, min(value, maximum))


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
        self.elements = []
        self.pos1 = pos1
        self.pos2 = pos2
        self.color = color
        self.current_page = 0
        self.rect = pygame.Rect(pos1, (pos2[0] - pos1[0], pos2[1] - pos1[1]))

    def previous_page(self):
        self.current_page = Utilities.clamp(self.current_page - 1, 0, len(self.elements) // 10)

    def next_page(self):
        self.current_page = Utilities.clamp(self.current_page + 1, 0, len(self.elements) // 10)

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
            for i in range(10):
                if pygame.rect.Rect(self.rect.left, self.rect.top + i * self.rect.height // 10, self.rect.width,
                                    self.rect.height // 10).collidepoint(pos):
                    try:
                        self.elements[self.current_page * 10 + i].function()
                    except IndexError:
                        pass


class ListElement(UIElement):

    def __init__(self, list_ui, text, function=lambda: None):
        super(ListElement, self).__init__(list_ui.controller)
        self.text = text
        self.function = function
