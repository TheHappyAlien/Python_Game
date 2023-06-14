import pygame, sys
from settings import tile_size, screen_height, screen_width, level_map
from player import Player
from level import Level 



screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Projekt")
clock = pygame.time.Clock()
level = Level(level_map, screen)


# player = Player.Player(speed=25, scale=1.5, runSpeed=0.4, terminalVelocity=10, gravityScale=0.1)

if __name__ == "__main__":
    pygame.init()

    while(True):
        pressed_key = pygame.key.get_pressed()
        # player.playerController(pressed_key, levelColliders)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.fill((40,40,40))
        level.run()

        pygame.display.update()
        clock.tick(60)
