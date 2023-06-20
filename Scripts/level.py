import pygame
from tiles import Tile
from settings import tile_size
from player import Player
from settings import screen_width, screen_height
from enemy_cube import Enemy_cube
from random import Random
from score import Score
from attack_speed_upgrade import Attack_speed_upgrade
from move_speed_upgrade import Move_speed_upgrade
from attack_damage_upgrade import Attack_damage_upgrade


class Level:
    def __init__(self, level_data, surface) -> None:
        
        # score
        self.score_object = Score()

        # level setup
        self.display_surface = surface
        self.player_sprite = Player((screen_width*0.5, screen_height*0.5), self.display_surface, self.score_object)
        self.setup_level(level_data)

        # camera movement variables
        self.camera_movement_bound_x = 0.2
        self.camera_movement_bound_y = 0.2

        self.tiles.update(self.world_shift_x, self.world_shift_y)
        self.passive_tiles.update(self.world_shift_x, self.world_shift_y)
        self.enemies.update(self.world_shift_x, self.world_shift_y)
        self.upgrade_shops.update(self.world_shift_x, self.world_shift_y)
        
        self.number_of_enemies = 0
        # for tile in self.floor_tiles:
        #     tile.update(self.world_shift_x, self.world_shift_y)

        self.enemy_scaling_timer = 0
        self.spawn_timer = 0
        self.random = Random()
        self.floor_tiles_len = len(self.floor_tiles)

    def setup_level(self, layout):
        self.tiles = pygame.sprite.Group()
        self.player = pygame.sprite.GroupSingle()
        self.passive_tiles = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.upgrade_shops = pygame.sprite.Group()

        self.floor_tiles = []


        self.tile_map = []

        for row_index, row in enumerate(layout):
            self.tile_map.append([])
            for col_index, cell in enumerate(row):
                x = col_index*tile_size
                y = row_index*tile_size                
                
                if cell == 'X' or cell == '0' or cell == 'N' or cell =='A' or cell == 'M' or cell == 'D':
                    self.tile_map[row_index].append(True)                  
                    tile = Tile((x, y), tile_size)          

                    if cell == 'X':
                        self.tiles.add(tile)

                    elif cell == '0':
                        self.passive_tiles.add(tile)

                    elif cell == 'A':
                        attack_speed_upgrade = Attack_speed_upgrade((x+10, y+20), self.player_sprite, self.display_surface)
                        self.upgrade_shops.add(attack_speed_upgrade)
                        
                    elif cell == 'M':
                        move_speed_upgrade = Move_speed_upgrade((x+10, y+15), self.player_sprite, self.display_surface)
                        self.upgrade_shops.add(move_speed_upgrade)

                    elif cell == 'D':
                        attack_damage_upgrade = Attack_damage_upgrade((x+10, y+15), self.player_sprite, self.display_surface)
                        self.upgrade_shops.add(attack_damage_upgrade)
                else:
                    self.tile_map[row_index].append(False)                   
                    if cell == 'P':
                        self.world_shift_x = -x+(screen_width*0.5)
                        self.world_shift_y = -y+(screen_height*0.5)
                        self.player.add(self.player_sprite)
                    
                    elif cell == 'C':
                        enemy_sprite = Enemy_cube((x+16, y+16), self.display_surface, player=None)
                        self.enemies.add(enemy_sprite)



        # adding a pointer to the player to all enemies                    
        for enemy in self.enemies:
            enemy.player = self.player.sprite

        self.player.sprite.enemies = self.enemies

        for tile in self.tiles:
            column = int(tile.rect.left / tile_size)
            row = int(tile.rect.top / tile_size)

            if row == 0 or row > 37:
                continue
            
            if not self.tile_map[row-1][column]:
                # print(f"row: {row}, column{column}")                
                self.floor_tiles.append(tile)
                # print(f"row: {int(tile.rect.top/tile_size)}, col: {int(tile.rect.left/tile_size)}")
    
    def spawn_enemies(self):
        if len(self.enemies) < 50 and self.spawn_timer >= 1200/1+int(self.enemy_scaling_timer)*0.01:
            self.spawn_timer = 0

            spawn_tile: Tile = self.floor_tiles[self.random.randint(0, self.floor_tiles_len-1)]
            pos = spawn_tile.rect.centerx, spawn_tile.rect.top

            speed_scale_factor = 0.01*int(self.enemy_scaling_timer/1200)
            if speed_scale_factor > 1.5:
                speed_scale_factor = 1.5
            enemy_speed_scale = 1+speed_scale_factor+self.random.random()**0.1

            health_scale_factor = 0.01*int(self.enemy_scaling_timer/900)
            enemy_health_scale = 1+health_scale_factor

            enemy = Enemy_cube(pos, self.display_surface, self.player.sprite, movement_speed_scale=enemy_speed_scale, max_health_scale=enemy_health_scale)
            enemy.collision_rect.bottom = spawn_tile.rect.top
            self.enemies.add(enemy)

    def scroll_x(self):
        player = self.player.sprite
        player_x = player.collision_rect.centerx
        direction_x = player.direction.x

        if player_x < screen_width * self.camera_movement_bound_x and direction_x < 0:
            self.world_shift_x = player.movement_speed
            player.can_move_x = False
        elif player_x > screen_width - (screen_width * self.camera_movement_bound_x) and direction_x > 0:
            self.world_shift_x = -1 * player.movement_speed
            player.can_move_x = False
        else:
            self.world_shift_x = 0
            player.can_move_x = True

    def scroll_y(self):
        player = self.player.sprite
        player_y = player.collision_rect.centery
        
        if (player_y < screen_height * self.camera_movement_bound_y and player.y_velocity < 0) or (player_y > screen_height - (screen_height * self.camera_movement_bound_y) and player.y_velocity > 0):
            self.world_shift_y = -1 * player.y_velocity
            player.can_move_y = False
        else:
            self.world_shift_y = 0
            player.can_move_y = True

    def horizontal_movement_collisions(self):
        player = self.player.sprite

        if player.can_move_x:
            player.movement_x()

        for sprite in self.tiles.sprites():
            if sprite.rect.colliderect(player.collision_rect):
                if player.direction.x < 0:
                    player.collision_rect.left = sprite.rect.right
                elif player.direction.x > 0:
                    player.collision_rect.right = sprite.rect.left


        for enemy in self.enemies:
            enemy.movement_x()  
            for sprite in self.tiles.sprites():              
                if sprite.rect.colliderect(enemy.collision_rect):
                    if enemy.direction.x < 0:
                        enemy.collision_rect.left = sprite.rect.right
                    elif enemy.direction.x > 0:
                        enemy.collision_rect.right = sprite.rect.left
            
    def vertical_movement_collisions(self):
        player = self.player.sprite

        if player.can_move_y:
            player.movement_y()

        for sprite in self.tiles.sprites():
            if sprite.rect.colliderect(player.collision_rect):
                if player.y_velocity < 0:
                    player.y_velocity = 0 
                    player.collision_rect.top = sprite.rect.bottom
                elif player.y_velocity > 0:
                    player.y_velocity = 0                    
                    player.collision_rect.bottom = sprite.rect.top
                    player.is_grounded = True
        if player.is_grounded and (player.y_velocity < 0 or player.y_velocity > 1):
            player.is_grounded = False


        for enemy in self.enemies.sprites():
            enemy.movement_y()
            for sprite in self.tiles.sprites():                
                if sprite.rect.colliderect(enemy.collision_rect):
                    if enemy.y_velocity < 0:
                        enemy.y_velocity = 0 
                        enemy.collision_rect.top = sprite.rect.bottom
                    elif enemy.y_velocity > 0:
                        enemy.y_velocity = 0                    
                        enemy.collision_rect.bottom = sprite.rect.top            

    def run(self):
        self.spawn_timer += 1
        self.enemy_scaling_timer += 1

        # camera movement
        self.scroll_x()
        self.scroll_y() 

        # level tiles
        # need to do it this way, so that the collisions work properly        
        for tile in self.tiles:
            tile.update_x(self.world_shift_x)
        self.horizontal_movement_collisions() 
        
        for tile in self.tiles:
            tile.update_y(self.world_shift_y)          
        self.vertical_movement_collisions()      

        self.tiles.draw(self.display_surface)

        # level tiles that do not interact with entities (decorational purposes only, so inside of walls)
        self.passive_tiles.update(self.world_shift_x, self.world_shift_y)
        self.passive_tiles.draw(self.display_surface)

        # enemies
        self.enemies.update(self.world_shift_x, self.world_shift_y)
        self.enemies.draw(self.display_surface)

        self.spawn_enemies()

        # shops
        self.upgrade_shops.update(self.world_shift_x, self.world_shift_y)
        self.upgrade_shops.draw(self.display_surface)

        # player
        self.player.update()              
        self.player.draw(self.display_surface)
