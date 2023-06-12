import pygame
import Player
from Platform import Platform

WIDTH, HEIGHT = 1600, 900
Scene = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Projekt")

WHITE = (255, 255, 255)
MAGENTA = (10, 200, 200)
PLAYER = Player.Player(speed=25, scale=2, runSpeed=0.2, terminalVelocity=10, gravityScale=0.1)
FPS = 60

platform1 = Platform(0, 150, 200, 20)

levelColliders = [platform1.getCollider()]

def draw_scene():
    Scene.fill(MAGENTA)
    PLAYER.draw(Scene)
    platform1.draw(Scene)
    pygame.display.update()

def main():
    clock = pygame.time.Clock()
    run = True

    while run:
        clock.tick(FPS)
        draw_scene()

        pressed_key = pygame.key.get_pressed()
        PLAYER.playerController(pressed_key, levelColliders)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False



    pygame.quit()


if __name__ == "__main__":
    main()