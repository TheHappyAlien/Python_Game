import pygame
from support import import_folder
from typing import List
from game_entity import Game_entity
from settings import tile_size, screen_height, screen_width
from health_bar import Health_bar
from menu import Menu

class Player(Game_entity):
    def __init__(self, pos, surface, score, enemies=None) -> None:

        # score obj
        self.score_object = score

        # for drawing elements belonging to the player
        self.display_surface = surface

        # Images and animations
        self.import_player_assets()
        self.frame_index = 0
        self.animation_speed = 0.2        
        self.status = 'idle'
        self.died = False

        super().__init__(pos, image=self.animations['idle'][self.frame_index], terminal_velocity=20, movement_speed=4, scale=1.5, rect_top_offset=5, rect_left_offset=7, rect_width=3, rect_height=10)

        # health
        self.healthbar_pos = screen_width*0.2, screen_height*0.92
        self.healthbar = Health_bar(self.healthbar_pos, 200, 20, self.display_surface)

        # attack
        self.enemies = enemies
        self.attack_range = 1000
        self.attack_hitbox = pygame.rect.Rect(self.collision_rect.centerx, self.collision_rect.centery, self.attack_range, 2)
        self.attack_about_to_finish = False
        self.attack_speed = 0.5
        self.attack_damage = 20
        self.hit = False

        self.hit_anim_frame_index = 0
        self.gunshot_sound = pygame.mixer.Sound('./SoundEffects/gunshot.wav')
        self.money = 100

        # Used to turn off player movement on camera scroll
        self.can_move_x = True
        self.can_move_y = True

        self.jump_speed = -0.3*tile_size

    def import_player_assets(self):
        player_path = './Sprites/Player/'
        self.animations = {'idle':[], 'run':[], 'jump':[], 'fall':[], 'attack':[], 'gun_hit':[]}

        for animation in self.animations.keys():
            full_path = player_path + animation
            self.animations[animation] = import_folder(full_path)

    def animate(self):
        self.get_status()
        animation = self.animations[self.status]

        # Cycling through frames
        if self.status == 'attack':
            self.frame_index += self.animation_speed*self.attack_speed
        elif self.status == 'run':
            self.frame_index += self.animation_speed*self.movement_speed/4
        else:
            self.frame_index += self.animation_speed
        
        if self.frame_index >= len(animation):
            self.frame_index = int(self.frame_index) % len(animation)

        self.image = animation[int(self.frame_index)]

    def animate_gun_hit(self, pos):
        animation = self.animations['gun_hit']
        self.hit_anim_frame_index += self.animation_speed*2
        offset_left, offset_top = -5, -8
        left, top = pos
        # Animating the gunshot
        if self.hit_anim_frame_index < len(animation):
            image = animation[int(self.hit_anim_frame_index)]
            if not self.facing_right:
                image = pygame.transform.flip(image, True, False)
            self.display_surface.blit(image, (left + offset_left, top + offset_top))

    def get_status(self):
        if self.status == 'attack':
            ...
        else:
            if self.y_velocity < 0:
                self.status = 'jump'
            elif self.y_velocity > 1:
                self.status = 'fall'
            elif self.is_grounded:
                if self.direction.x != 0:
                    self.status = 'run'
                else: 
                    self.status = 'idle'

    def get_input(self):
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_a]:
            self.facing_right = False
        elif keys[pygame.K_d]:
            self.facing_right = True
            
        if keys[pygame.K_e]:
            self.status = 'attack'
        else:
            if keys[pygame.K_d] and keys[pygame.K_a]:
                self.direction.x = 0
            elif keys[pygame.K_d]:
                self.direction.x = 1 # moving right
            elif keys[pygame.K_a]:
                self.direction.x = -1 # moving left
            else:
                self.direction.x = 0

            if keys[pygame.K_SPACE] and self.is_grounded:
                self.jump()
    
    def attack(self):
        self.can_move_x = False
        self.direction.x = 0 

        if not self.hit:
            # reseting git animation
            self.hit_anim_frame_index = 0
            self.frame_index = 0
            
            enemies_hit = []

            self.gunshot_sound.play(fade_ms=5)

            if self.facing_right:
                attack_len = self.attack_range
            else:
                attack_len = -self.attack_range

            self.attack_hitbox.update(self.collision_rect.centerx, self.collision_rect.centery, attack_len, 2)
            
            for enemy in self.enemies:
                if self.attack_hitbox.colliderect(enemy.collision_rect):
                    enemies_hit.append(enemy)

            enemies_hit.sort(key=lambda x: x.collision_rect.centerx)

            if len(enemies_hit) > 0:
                if self.facing_right:
                    enemy_hit = enemies_hit[0]
                    self.hit_pos = enemy_hit.collision_rect.left, self.attack_hitbox.top                    
                else:
                    enemy_hit = enemies_hit[-1]
                    self.hit_pos = enemy_hit.collision_rect.right, self.attack_hitbox.top
                
                enemy_hit.current_health -= self.attack_damage
                enemy_hit.is_stunned = True

                if enemy_hit.current_health <= 0:
                    enemy_hit.kill()
                    self.score_object.score += 1
                    self.money += 1
            else:
                self.hit_pos = None
            self.hit = True

        if self.hit_pos:
            self.animate_gun_hit(self.hit_pos)

        # reseting status after attack animation
        if int(self.frame_index) == 2:
            self.attack_about_to_finish = True

        elif self.attack_about_to_finish:
            self.status = 'idle'
            self.attack_about_to_finish = False
            self.hit = False

    def jump(self):
        self.y_velocity = self.jump_speed

    def update(self):
        if self.status != 'attack':
            self.get_input()
        else:
            self.attack()
        self.animate()
        super().update()
        self.healthbar.draw(self.health_percentage, self.display_surface, self.healthbar_pos)