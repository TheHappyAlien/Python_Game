import pygame

class Platform():
    def __init__(self, x, y, width, height) -> None:
        self.sprite = pygame.transform.scale(pygame.image.load("Sprites/Rectangle.png"), (width, height))
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.collider = pygame.rect.Rect(x, y, width, height)

    def draw(self, screen) -> None:
        screen.blit(self.sprite, (self.x, self.y))

    def getCollider(self) -> pygame.rect.Rect:
        return self.collider        