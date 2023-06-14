import pygame
from support import import_folder
from enum import Enum
from typing import List
from game_entity import Game_entity
from settings import tile_size

class Player(Game_entity):
    def __init__(self, pos) -> None:

        # Images and animations
        self.import_player_assets()
        self.frame_index = 0
        self.animation_speed = 0.2
        super().__init__(pos, image=self.animations['idle'][self.frame_index], terminal_velocity=20, movement_speed=5, scale=2, rect_top_offset=5, rect_left_offset=7, rect_width=3, rect_height=10)
        self.staus = 'idle'


        # Used to turn off player movement on camera scroll
        self.can_move_x = True
        self.can_move_y = True

        self.jump_speed = -0.3*tile_size

    def import_player_assets(self):
        player_path = './Sprites/Player/'
        self.animations = {'idle':[], 'run':[], 'jump':[], 'fall':[]}

        for animation in self.animations.keys():
            full_path = player_path + animation
            self.animations[animation] = import_folder(full_path)

    def animate(self):
        self.get_status()
        animation = self.animations[self.staus]

        # Cycling through frames
        self.frame_index += self.animation_speed

        if self.frame_index >= len(animation):
            self.frame_index = int(self.frame_index) % len(animation)

        self.image = animation[int(self.frame_index)]

    def get_status(self):
        if self.y_velocity < 0:
            self.staus = 'jump'
        elif self.y_velocity > 1:
            self.staus = 'fall'
        elif self.is_grounded:
            if self.direction.x != 0:
                self.staus = 'run'
            else: 
                self.staus = 'idle'

    def get_input(self):
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_d] and keys[pygame.K_a]:
            self.direction.x = 0
        elif keys[pygame.K_d]:
            self.direction.x = 1 # moving right
            self.facing_right = True
        elif keys[pygame.K_a]:
            self.direction.x = -1 # moving left
            self.facing_right = False
        else:
            self.direction.x = 0

        if keys[pygame.K_SPACE] and self.is_grounded:
            self.jump()

    def jump(self):
        self.y_velocity = self.jump_speed

    def update(self):
        self.get_input()
        self.animate()
        super().update()
