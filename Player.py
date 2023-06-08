import pygame

class Player():
    def __init__(self, xPos=0, yPos=0, speed=1, scale=1) -> None:
        self.playerImg = pygame.image.load("Sprites/Player.png")
        self.x = xPos
        self.y = yPos
        self.speed = speed
        self.scale = scale
        self.width = 150
        self.height = 300
        self.sprite = pygame.transform.scale(self.playerImg, (self.width*scale, self.height*scale))
        self.lookingLeft = False
        self.movingLeft = False

    def playerController(self, pressed_key: pygame.key.get_pressed) -> None:
        if pressed_key[pygame.K_a] or pressed_key[pygame.K_d]:
            if pressed_key[pygame.K_a]: 
                if not pressed_key[pygame.K_d]:
                    self.x -= self.speed
                    self.movingLeft = True
            else:
                self.x += self.speed
                self.movingLeft = False
        
        if self.lookingLeft != self.movingLeft:
            self.sprite = pygame.transform.flip(self.sprite, flip_x=True, flip_y=False)
            self.lookingLeft = self.movingLeft

    def draw(self, screen) -> None:
        screen.blit(self.sprite, (self.x, self.y))
