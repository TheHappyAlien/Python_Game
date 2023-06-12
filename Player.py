import pygame
from GravityAffectedObject import GravityAffectedObject
from enum import Enum
from typing import List

playerStates = Enum('State', ['AboutToBeIdle','Running','Jumping','Falling','Shooting'])

class Player(GravityAffectedObject):
    def __init__(self, x=0, y=0, speed=1, scale=1, runSpeed=1, attackSpeed=1, gravityScale=1, terminalVelocity = 1000) -> None:
        super().__init__(gravityScale, terminalVelocity)
        self.idleSprite = pygame.image.load("Sprites/Player/PlayerCharacter_idle.png")

        self.collider = pygame.rect.Rect(x + 5*scale, y + 5*scale, 4*scale, 9*scale)

        self.x = x
        self.y = y
        self.speed = speed
        self.scale = scale
        self.width = 16
        self.height = 16

        self.currentSprite: pygame.surface.Surface = self.idleSprite
        self.lookingLeft = False
        self.movingLeft = False
        self.runSpeed = runSpeed
        self.canRunRight = True
        self.canRunLeft = True

        self.attackSpeed = attackSpeed
        self.state = playerStates.AboutToBeIdle

        self.runSprites = [pygame.image.load("Sprites/Player/PlayerCharacter_run1.png"),
                           pygame.image.load("Sprites/Player/PlayerCharacter_run2.png"),
                           pygame.image.load("Sprites/Player/PlayerCharacter_run3.png"),
                           pygame.image.load("Sprites/Player/PlayerCharacter_run4.png")]
        self.animFrame = 0
                           

    def playerController(self, pressed_key: pygame.key.get_pressed, levelColliders: list = [pygame.rect.Rect(-1, -1, 0, 0)]) -> None:
        self.gravity()
        self.updateColliders()

        # If you drop onto a platform
        colliderIndexes = self.collider.collidelistall(levelColliders)

        foundGround = False
        foundWallLeft = False
        foundWallRight = False
        foundCeiling = False

        for colliderIndex in colliderIndexes:
            # Check for ground
            if levelColliders[colliderIndex].top > int(self.y + 14*self.scale):
                self.isGrounded = True
                self.yVelocity = 0

            # Check for wall


            # Check for celing

        if self.groundedCheckCollider.collidelist(levelColliders) != -1:

            print("es")
        else:
            self.isGrounded = False

        # If you run into a wall
        if () != -1:
            if for colliderIndex in colliderIndexes: :
            if levelColliders[colliderIndex].left <= self.x + 5*self.scale:
                self.canRunLeft = False

            else:
                self.canRunRight = False
        else:
            self.canRunRight = True
            self.canRunLeft = True

        # State based on current input
        if pressed_key[pygame.K_a] or pressed_key[pygame.K_d]:
            self.runLogic(pressed_key)
        else:
            self.state = playerStates.AboutToBeIdle
        # Settings depending on current state
        if self.state == playerStates.AboutToBeIdle:
            self.currentSprite = self.idleSprite
            self.animFrame = 0
        elif self.state == playerStates.Running:
            self.runAnim()


    def draw(self, screen) -> None:
        self.currentSprite = pygame.transform.scale(self.currentSprite, (self.width*self.scale, self.height*self.scale))
        
        if self.movingLeft == True:
            self.currentSprite = pygame.transform.flip(self.currentSprite, flip_x=True, flip_y=False)
        
        screen.blit(self.currentSprite, (self.x, self.y))


    def updateColliders(self):
        self.collider.update(self.x + 5*self.scale, self.y + 5*self.scale, 4*self.scale, 10*self.scale)
        self.groundedCheckCollider.update(self.x + 6*self.scale, self.y + 14*self.scale, 1*self.scale, 1*self.scale)


    def runLogic(self, pressed_key: pygame.key.get_pressed):
        if not pressed_key[pygame.K_a] and self.canRunRight:
            self.x += self.speed*self.runSpeed
            self.movingLeft = False
            self.state = playerStates.Running

        elif not pressed_key[pygame.K_d] and self.canRunLeft:
                self.x -= self.speed*self.runSpeed
                self.movingLeft = True
                self.state = playerStates.Running

        else:
            self.state = playerStates.AboutToBeIdle


    def runAnim(self) -> None:
        self.animFrame += self.runSpeed
        if self.animFrame >= len(self.runSprites):
            self.animFrame = 0
        self.currentSprite = self.runSprites[int(self.animFrame)]

