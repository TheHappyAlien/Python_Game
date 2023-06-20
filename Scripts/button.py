import pygame


class Button():
    def __init__(self, pos, width, height, colour, display_surface, hovered_scale=1) -> None:
        self.width = width
        self.height = height
        self.left, self.top = pos
        self.display_surface = display_surface
        self.colour = colour
        self.rect = pygame.rect.Rect(self.left, self.top, self.width, self.height)
        
        self.scale = 1
        self.hovered_scale = hovered_scale

        self.hovered = False
        self.clicked = False

    def draw(self):
        if self.hovered:
            self.scale = self.hovered_scale
        else:
            self.scale = 1

        self.rect.update(self.left-self.width*((self.scale-1)/2), self.top-self.height*((self.scale-1)/2), self.width*self.scale, self.height*self.scale)    

        pygame.draw.rect(self.display_surface, self.colour, self.rect)

    def button_logic(self):
        action = False
        self.hovered = False

        mouse_pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(mouse_pos):
            self.hovered = True
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                action = True
            
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        return action
