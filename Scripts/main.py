import pygame, sys
from settings import tile_size, screen_height, screen_width, level_map
from player import Player
from level import Level
from menu import Menu
from support import draw_number

pygame.init()

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Projekt")

# game variables
game_paused = True

clock = pygame.time.Clock()
level = Level(level_map, screen)

menu = Menu(screen)
# player = Player.Player(speed=25, scale=1.5, runSpeed=0.4, terminalVelocity=10, gravityScale=0.1)


if __name__ == "__main__":
    while(True):

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    game_paused = not game_paused
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.fill((200,200,200))

        if level.player.sprite.died:
            menu.draw_death_menu(level.score_object.score, level.score_object.high_score)
            level.score_object.save_score()
            if menu.restart_level:
                level = Level(level_map, screen)
                game_paused = False
                menu.restart_level = False

        else:            
            if game_paused:
                menu.draw()
                if menu.restart_level:
                    level = Level(level_map, screen)
                    game_paused = False
                    menu.restart_level = False
            else:
                level.run()
                draw_number(level.player_sprite.money, pygame.font.SysFont('arialblack', 30), (255, 255, 255), (screen_width*0.05, screen_height*0.9), screen)         

        pygame.display.update()
        clock.tick(60)
