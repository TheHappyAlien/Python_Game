import pygame
from GravityAffectedObject import GravityAffectedObject
from support import import_folder
from enum import Enum
from typing import List
from game_entity import Game_entity

class Player(Game_entity):
    def __init__(self, pos) -> None:

        # Images and animations
        self.import_player_assets()
        self.frame_index = 0
        self.animation_speed = 0.15
        super().__init__(pos, self.animations['idle'][self.frame_index], 5)

        # Used to turn off player movement on camera scroll
        self.can_move_x = True
        self.can_move_y = True

        self.jump_speed = -5

    def import_player_assets(self):
        player_path = '../Sprites/Player/'
        self.animations = {'idle':[], 'run':[], 'jump':[], 'fall':[]}

        for animation in self.animations.keys():
            full_path = player_path + animation
            self.animations[animation] = import_folder(full_path)


    def get_input(self):
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_d] and keys[pygame.K_a]:
            self.direction.x = 0
        elif keys[pygame.K_d]:
            self.direction.x = 1 # moving right
        elif keys[pygame.K_a]:
            self.direction.x = -1 # moving left
        else:
            self.direction.x = 0

        if keys[pygame.K_SPACE]:
            self.jump()

    def jump(self):
        self.y_velocity = self.jump_speed

    def update(self):
        self.get_input()
        super().update()

# playerStates = Enum('State', ['AboutToBeIdle','Running','Jumping','Falling','Shooting'])