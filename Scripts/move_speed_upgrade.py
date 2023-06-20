from typing import Any
import pygame
from upgrade_shop import Upgrade_shop

class Move_speed_upgrade(Upgrade_shop):
    def __init__(self, pos, player, display_surface) -> None:
        super().__init__(pos, image=pygame.image.load("../Sprites/move_speed_boost.png"), player=player, cost=20, display_surface=display_surface, rect_left_offset=-10, rect_top_offset=-20, rect_width=32, rect_height=32, text_x_offset=-8, text_y_offset=40)

    def update(self, x_shift, y_shift) -> None:
        super().update(x_shift, y_shift)

        if self.can_buy:
            if self.collision_rect.colliderect(self.player.collision_rect):
                keys = pygame.key.get_pressed()            
                if keys[pygame.K_b] and self.player.money >= self.cost:
                    self.can_buy = False    
                    self.player.movement_speed += 0.4
                    self.player.money -= self.cost
