import pygame, sys
from settings import tile_size, screen_height, screen_width, level_map
from player import Player
from level import Level
from menu import Menu
from support import draw_number
from score import Score

pygame.init()

score_saved = False
game_started = False

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Python Shooter")

# game variables
game_paused = True

clock = pygame.time.Clock()
level = Level(level_map, screen)

menu = Menu(screen, game_started)

base_font = pygame.font.Font(None, 32)
username = ''
username_input_rect = pygame.Rect(690, 250, 200, 32)
active = False

color_active = pygame.Color('lightskyblue3')
color_passive = pygame.Color('chartreuse4')


if __name__ == "__main__":
    while(True):

        screen.fill((200,200,200))
        
        if menu.quit:
            pygame.quit()
            sys.exit()            

        for event in pygame.event.get():
            if not game_started:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if username_input_rect.collidepoint(event.pos):
                        active = True
                    else:
                        active = False

                if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_BACKSPACE:
                                username = username[:-1]
                            else:
                                username += event.unicode                        

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    game_paused = not game_paused  

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        if not game_started:

            if active:
                color = color_active
            else:
                color = color_passive      

            menu.draw_start_menu()            
            pygame.draw.rect(screen, color, username_input_rect)            
            text_surface = base_font.render(username, True, (0, 0, 0))
            screen.blit(text_surface, (username_input_rect.x+5, username_input_rect.y+5))            
            username_input_rect.w = max(200, text_surface.get_width()+10)            
            game_started = menu.game_started
            if game_started:
                level.score_object = Score(username)

        else:
            if level.player.sprite.died:
                menu.draw_death_menu(level.score_object.score, level.score_object.high_score)
                if not score_saved:
                    level.score_object.save_score()
                    score_saved = True

                if menu.restart_level:
                    level = Level(level_map, screen, Score(username))
                    menu = Menu(screen, game_started)
                    score_saved = False
                    game_paused = False
                    menu.restart_level = False

            else:            
                if game_paused:
                    menu.draw()
                    if menu.restart_level:
                        level = Level(level_map, screen, Score(username))                       
                        game_paused = False
                        menu.restart_level = False
                else:
                    level.run()
                    draw_number(level.player_sprite.money, pygame.font.SysFont('arialblack', 30), (255, 255, 255), (screen_width*0.05, screen_height*0.9), screen)         

        # pygame.display.update()
        pygame.display.flip()
        clock.tick(60)
