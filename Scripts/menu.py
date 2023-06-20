import pygame
from support import draw_text, draw_number
from settings import screen_width, screen_height
from button import Button

class Menu():
    def __init__(self, screen) -> None:
        self.font = pygame.font.SysFont("arialblack", 40)
        self.screen = screen
        self.text_colour = (10,10,10)

        # reseting level
        self.restart_level = False
        self.restart_button = Button((695, 400), 175, 60, (150, 150, 150), self.screen, hovered_scale=1.1)

    def draw_death_menu(self, score, high_score):
        # restart buttons
        self.restart_level = self.restart_button.button_logic()
        self.restart_button.draw()
        draw_text("Restart", self.font, self.text_colour, (self.restart_button.left+5, self.restart_button.top), self.screen)        

        # score
        draw_text("Score:", self.font, self.text_colour, (600, 300), self.screen) 
        draw_number(score, self.font, (255, 255, 255), (800, 300), self.screen)  
        if score > high_score:
            draw_text("NEW HIGH SCORE!", self.font, self.text_colour, (1000, 300), self.screen)

        # additional text
        draw_text("You Died :(", self.font, self.text_colour, (700, 200), self.screen)       

    def draw_start_menu(self, high_score):
        ...
        
    def draw(self):
        # restart button        
        self.restart_level = self.restart_button.button_logic()
        self.restart_button.draw()
        draw_text("Restart", self.font, self.text_colour, (self.restart_button.left+5, self.restart_button.top), self.screen)        
        
        # additional text        
        draw_text("Paused", self.font, self.text_colour, (700, 200), self.screen)

   