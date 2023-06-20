import pygame
from game_entity import Game_entity
from support import draw_text
import platform
class Upgrade_shop(Game_entity):
    def __init__(self, pos, image, player, cost, display_surface, rect_left_offset, rect_top_offset, rect_width, rect_height, text_x_offset, text_y_offset,) -> None:
        super().__init__(pos, image, scale=1, rect_left_offset=rect_left_offset, rect_top_offset=rect_top_offset, rect_width=rect_width, rect_height=rect_height, max_health=1, gravity_affected=False)
        self.player = player
        self.cost = cost

        system = platform.uname()[0]
        if system == "Windows":
            self.font = pygame.font.SysFont("arialblack", 10)
        else:
            self.font = pygame.font.SysFont("ubuntu", 10)
            
        self.display_surface = display_surface
        self.text_x_offset = text_x_offset
        self.text_y_offset = text_y_offset
        
        self.buy_delay = 20
        self.frame_counter = 0
        self.can_buy = True


    def update(self, x_shift, y_shift) -> None:
        self.collision_rect.x += x_shift
        self.collision_rect.y += y_shift
        draw_text(str(self.cost), self.font, (255, 255, 255), (self.collision_rect.centerx + self.text_x_offset, self.collision_rect.y + self.text_y_offset), self.display_surface)

        if not self.can_buy:
            self.frame_counter += 1

        if self.frame_counter >= self.buy_delay:
            self.frame_counter = 0
            self.can_buy = True
            
        super().update() 