import pygame
from game_entity import Game_entity
from settings import tile_size
from player import Player
from support import import_folder
from health_bar import Health_bar

class Enemy_cube(Game_entity):
    def __init__(self, pos, surface, player: Player, movement_speed_scale=1, max_health_scale=1) -> None:

        super().__init__(pos, image=pygame.image.load('../Sprites/Enemy_cube/idle.png'), rect_width=16, rect_height=16, movement_speed=2*movement_speed_scale, max_health=50*max_health_scale)    
        self.display_surface = surface

        self.movement_speed_scale = movement_speed_scale
        self.max_health_scale = max_health_scale

        self.player: Player = player
        self.can_change_direction = True

        self.is_attacking = False
        self.attack_anim_playing = False
        self.frame_counter = 0
        self.hit_player = False
        self.attack_damage = 10
        self.is_stunned = False
        self.stun_playing = False

        self.health_bar = Health_bar((self.collision_rect.left, self.collision_rect.bottom + 10), 16, 2, self.display_surface)

    def set_movement_direction(self):

        if self.collision_rect.centerx < self.player.collision_rect.centerx and (self.is_attacking or self.collision_rect.centerx < self.player.collision_rect.centerx-5):
            self.direction.x = 1
            self.facing_right = True
        elif self.collision_rect.centerx > self.player.collision_rect.centerx and (self.is_attacking or self.collision_rect.centerx > self.player.collision_rect.centerx+5):
            self.direction.x = -1
            self.facing_right = False
        else:
            self.direction.x = 0

    def stun(self, frames):
        if not self.stun_playing:
            self.frame_counter = 0
            self.stun_playing = True
            self.direction.x = 0
            self.is_attacking = False
            self.attack_anim_playing = False

        elif self.frame_counter >= frames:
            self.stun_playing = False
            self.is_stunned = False
            self.frame_counter = 0
            self.can_change_direction = True
            
        self.frame_counter += 1
        
    def attack_conditions(self):
        within_range_above = self.collision_rect.centery < self.player.rect.centery and self.collision_rect.centery > self.player.collision_rect.centery-40
        within_range_below = self.collision_rect.centery > self.player.rect.centery and self.collision_rect.centery < self.player.collision_rect.centery+30

        within_range_left = self.collision_rect.centerx < self.player.rect.centerx and self.collision_rect.centerx > self.player.collision_rect.centerx-60
        within_range_right = self.collision_rect.centerx > self.player.rect.centerx and self.collision_rect.centerx < self.player.collision_rect.centerx+60

        if within_range_above or within_range_below:
            if within_range_left or within_range_right:
                self.is_attacking = True

    def attack(self):
        # setup
        if not self.attack_anim_playing:
            self.frame_counter = 0

            self.attack_delay_end_frame = 15
            self.windup_end_frame = self.attack_delay_end_frame+10
            self.attack_end_frame = self.windup_end_frame+5
            self.attack_break_end_frame = self.attack_end_frame+8

            self.attack_anim_playing = True
        
        self.frame_counter += 1

        # attack sequence
        if self.frame_counter < self.attack_delay_end_frame:
            self.direction.x = 0
            self.can_change_direction = False
        elif self.frame_counter >= self.attack_delay_end_frame and self.frame_counter < self.windup_end_frame:          
            self.movement_speed = -1*self.movement_speed_scale
            self.can_change_direction = True
        elif self.frame_counter >= self.windup_end_frame and self.frame_counter < self.attack_end_frame:
            self.movement_speed = 10*self.movement_speed_scale
            self.can_change_direction = False
        elif self.frame_counter >= self.attack_end_frame and self.frame_counter < self.attack_break_end_frame:
            self.movement_speed -= 1*self.movement_speed_scale
        else:
            self.can_change_direction = True

        # checking for collisions with the player
        if not self.hit_player and self.frame_counter >= self.windup_end_frame and self.frame_counter < self.attack_break_end_frame:
            if self.collision_rect.colliderect(self.player.collision_rect):
                self.player.current_health -= self.attack_damage
                self.hit_player = True
                if self.player.current_health <= 0:
                    self.player.died = True

        # reseting the attack state
        if self.frame_counter >= self.attack_break_end_frame+30:
            self.is_attacking = False
            self.attack_anim_playing = False
            self.hit_player = False
    
    def update_x(self, x_shift):
        self.collision_rect.x += x_shift

    def update_y(self, y_shift):
        self.collision_rect.y += y_shift   

    def update(self, x_shift, y_shift):
        super().update()
        # self.collision_rect.x += x_shift
        # self.collision_rect.y += y_shift
      
        self.image = pygame.image.load('../Sprites/Enemy_cube/idle.png')
        
        if not self.is_stunned:
            if self.can_change_direction:
                self.set_movement_direction()

            if not self.is_attacking:
                self.attack_conditions()
            else:
                self.attack()

        else: 
            self.stun(20)

        if self.health_percentage < 1:
            self.health_bar.draw(self.health_percentage, self.display_surface, (self.collision_rect.left, self.collision_rect.bottom + 10))        