from typing import Any
import pygame

class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, size) -> None:
        super().__init__()
        self.image = pygame.Surface((size, size))
        self.image.fill((40,40,40))
        self.rect = self.image.get_rect(topleft = pos)

    def update_x(self, x_shift):
        self.rect.x += x_shift

    def update_y(self, y_shift):
        self.rect.y += y_shift        
        
    def update(self, x_shift, y_shift) -> None:
        self.rect.x += x_shift
        self.rect.y += y_shift 