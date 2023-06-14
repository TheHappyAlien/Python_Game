import pygame

class Game_entity(pygame.sprite.Sprite):
    def __init__(self, pos, image, movement_speed=1, gravity_affected = True, gravity_force = 0.4, terminal_velocity = 1000, scale = 1, rect_top_offset = 0, rect_left_offset = 0, rect_width = 0, rect_height = 0) -> None:
        super().__init__()

        # preparing the image and rect
        self.image = image
        self.scale = scale
        self.facing_right = True

        # setting up the rect
        left, top = pos
        self.rect = pygame.rect.Rect(left, top, 0, 0) # rect from the image file, it is only used to place the sprite in the correct position

        # used to offset the proper rect from the image rect, and give the rect correct dimentions
        self.rect_top_offset = rect_top_offset
        self.rect_left_offset = rect_left_offset
        self.rect_width = rect_width
        self.rect_height = rect_height

        # the proper rect of the entity
        self.collision_rect = pygame.rect.Rect(left+self.rect_left_offset*self.scale, top+self.rect_top_offset*self.scale, self.rect_width*self.scale, self.rect_height*self.scale)

        # movement
        self.direction = pygame.math.Vector2(0, 0)
        self.movement_speed = movement_speed
        self.y_velocity = 0
        self.is_grounded = True

        # gravity
        self.gravity = 0
        self.terminal_velocity = terminal_velocity

        if gravity_affected:
            self.gravity = gravity_force

    def apply_gravity(self):
        self.y_velocity += self.gravity
        if self.y_velocity > self.terminal_velocity:
            self.y_velocity = self.terminal_velocity

    def movement_x(self):
        self.collision_rect.x += self.direction.x * self.movement_speed

    def movement_y(self):
        self.collision_rect.y += self.y_velocity

    def update(self):
        self.apply_gravity()
        self.image = pygame.transform.scale(self.image, (self.image.get_width()*self.scale, self.image.get_height()*self.scale))
        if not self.facing_right:
            self.image = pygame.transform.flip(self.image,flip_x=True, flip_y=False)

        self.rect.update(self.collision_rect.left-self.rect_left_offset*self.scale, self.collision_rect.top-self.rect_top_offset*self.scale, 0, 0)
