import pygame
from tiles import Tile
from settings import tile_size
from player import Player
from settings import screen_width, screen_height


class Level:
    def __init__(self, level_data, surface) -> None:
        
        # level setup
        self.display_surface = surface
        self.setup_level(level_data)

        # camera movement variables
        self.camera_movement_bound_x = 0.2
        self.camera_movement_bound_y = 0.2

        self.tiles.update(self.world_shift_x, self.world_shift_y)
        self.passive_tiles.update(self.world_shift_x, self.world_shift_y)   

    def setup_level(self, layout):
        self.tiles = pygame.sprite.Group()
        self.player = pygame.sprite.GroupSingle()
        self.passive_tiles = pygame.sprite.Group()

        for row_index, row in enumerate(layout):
            for col_index, cell in enumerate(row):
                x = col_index*tile_size
                y = row_index*tile_size                
                
                if cell == 'X':
                    tile = Tile((x, y), tile_size)
                    self.tiles.add(tile)
                
                elif cell == '0':
                    tile = Tile((x, y), tile_size)
                    self.passive_tiles.add(tile)

                elif cell == 'P':
                    self.world_shift_x = -x+(screen_width*0.5)
                    self.world_shift_y = -y+(screen_height*0.5)
                    player_sprite = Player((screen_width*0.5, screen_height*0.5))
                    self.player.add(player_sprite)

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

    def run(self):
        # camera movement
        self.scroll_x()
        self.scroll_y() 

        # level tiles
        self.tiles.update(self.world_shift_x, self.world_shift_y)
        self.tiles.draw(self.display_surface)

        # level tiles that do not interact with entities (decorational purposes only, so inside of walls)
        self.passive_tiles.update(self.world_shift_x, self.world_shift_y)
        self.passive_tiles.draw(self.display_surface)

        # level player
        self.player.update()
        self.vertical_movement_collisions()
        self.horizontal_movement_collisions()        
        self.player.draw(self.display_surface)