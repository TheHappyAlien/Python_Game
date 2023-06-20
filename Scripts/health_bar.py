import pygame


class Health_bar():
    def __init__(self, pos, width, height, display_surface):
        self.left, self.top = pos
        self.width = width
        self.height = height

        self.empty_healthbar_rect = pygame.rect.Rect(self.left, self.top, self.width, self.height)
        self.empty_healthbar = pygame.draw.rect(display_surface, (10,10,10), self.empty_healthbar_rect)

        self.filled_healthbar_rect = pygame.rect.Rect(self.left, self.top, self.width, self.height)
        self.filled_healthbar = pygame.draw.rect(display_surface, (150, 200, 20), self.filled_healthbar_rect)

    def draw(self, helth_percentage, display_surface, pos):
        self.left, self.top = pos        
        self.empty_healthbar_rect = pygame.rect.Rect(self.left, self.top, self.width, self.height)        
        self.empty_healthbar = pygame.draw.rect(display_surface, (10,10,10), self.empty_healthbar_rect)

        self.filled_healthbar_rect = pygame.rect.Rect(self.left, self.top, self.width*helth_percentage, self.height)
        self.filled_healthbar = pygame.draw.rect(display_surface, (150, 200, 20), self.filled_healthbar_rect)       