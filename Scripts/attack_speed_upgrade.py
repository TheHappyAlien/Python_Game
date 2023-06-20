from typing import Any
import pygame
from upgrade_shop import Upgrade_shop
from support import draw_text

class Attack_speed_upgrade(Upgrade_shop):
    def __init__(self, pos, player, display_surface) -> None:
        super().__init__(pos, image=pygame.image.load("../Sprites/attack_speed_boost.png"), player=player, cost=10, display_surface=display_surface, rect_left_offset=-10, rect_top_offset=-20, rect_width=32, rect_height=32, text_x_offset=-8, text_y_offset=30)

    def update(self, x_shift, y_shift) -> None:
        super().update(x_shift, y_shift)

        if self.can_buy:
            if self.collision_rect.colliderect(self.player.collision_rect):
                keys = pygame.key.get_pressed()            
                if keys[pygame.K_b] and self.player.money >= self.cost:
                    self.can_buy = False
                    self.player.attack_speed += 0.1
                    self.player.money -= self.cost



