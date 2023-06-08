import pygame
import Player

WIDTH, HEIGHT = 1600, 900
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Projekt")

WHITE = (255, 255, 255)
MAGENTA = (10, 200, 200)
PLAYER = Player.Player(speed=5, scale=0.2)
FPS = 60


def draw_window():
    WIN.fill(MAGENTA)
    PLAYER.draw(WIN)
    pygame.display.update()

def main():
    clock = pygame.time.Clock()
    run = True

    while run:
        clock.tick(FPS)
        draw_window()

        pressed_key = pygame.key.get_pressed()
        PLAYER.playerController(pressed_key)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False



    pygame.quit()


if __name__ == "__main__":
    main()