import pygame

import GameEngine

pygame.init()
display_info = pygame.display.Info()
screen = pygame.display.set_mode((display_info.current_w, display_info.current_h), pygame.FULLSCREEN)

scale_coefficient = GameEngine.Vector2(display_info.current_w, display_info.current_h)

pygame.display.set_caption("Example")

pygame.display.flip()

clock = pygame.time.Clock()

running = True

while running:
    for key in GameEngine.Input.pressed_keys:
        GameEngine.Input.pressed_keys[key] = 0
    for key in GameEngine.Input.pressed_keys:
        GameEngine.Input.pressed_keys[key] = 0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key in GameEngine.Input.codes_keys:
                GameEngine.Input.holding_keys[GameEngine.Input.codes_keys[event.key]] = 1
            if event.key in GameEngine.Input.codes_keys:
                GameEngine.Input.pressed_keys[GameEngine.Input.codes_keys[event.key]] = 1
        elif event.type == pygame.KEYUP:
            if event.key in GameEngine.Input.codes_keys:
                GameEngine.Input.holding_keys[GameEngine.Input.codes_keys[event.key]] = 0
            if event.key in GameEngine.Input.codes_keys:
                GameEngine.Input.released_keys[GameEngine.Input.codes_keys[event.key]] = 1
    clock.tick(60)
pygame.quit()
