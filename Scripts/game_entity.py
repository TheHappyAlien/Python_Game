import pygame

class Game_entity(pygame.sprite.Sprite):
    def __init__(self, pos, image, movement_speed=1, gravity_affected = True, gravity_force = 0.2, terminal_velocity = 1000) -> None:
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(topleft = pos)
        self.direction = pygame.math.Vector2(0, 0)
        self.movement_speed = movement_speed
        
        self.gravity = 0
        self.terminal_velocity = terminal_velocity

        if gravity_affected:
            self.gravity = gravity_force

        self.y_velocity = 0

    def apply_gravity(self):
        self.y_velocity += self.gravity

    def movement_x(self):
        self.rect.x += self.direction.x * self.movement_speed

    def movement_y(self):
        self.rect.y += self.y_velocity

    def update(self):
        self.apply_gravity()
