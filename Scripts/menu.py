import pygame
from support import draw_text, draw_number
from settings import screen_width, screen_height
from button import Button
import platform

class Menu():
    def __init__(self, screen, game_started) -> None:
        system = platform.uname()[0]

        if system == "Windows":
            self.font = pygame.font.SysFont("arialblack", 40)
        else:
            self.font = pygame.font.SysFont("ubuntu", 40)
            
        self.screen = screen
        self.text_colour = (10,10,10)

        # reseting level
        self.restart_level = False
        self.quit = False
        self.game_started = game_started

        self.restart_button = Button((695, 400), 175, 60, (150, 150, 150), self.screen, hovered_scale=1.1)
        self.start_button = Button((695, 400), 175, 60, (150, 150, 150), self.screen, hovered_scale=1.1)
        self.quit_button = Button((695, 500), 175, 60, (150, 150, 150), self.screen, hovered_scale=1.1)

    def draw_death_menu(self, score, high_score):

        self.draw_restart_button()
        self.draw_quit_button()

        # score
        draw_text("Score:", self.font, self.text_colour, (600, 300), self.screen) 
        draw_number(score, self.font, (255, 255, 255), (800, 300), self.screen)

        # additional text
        if score > high_score:      
            draw_text("NEW HIGH SCORE!", self.font, self.text_colour, (600, 200), self.screen)               
        else:
            draw_text("You Died :(", self.font, self.text_colour, (700, 200), self.screen)    

    def draw_start_menu(self):
        self.draw_start_button()
        self.draw_quit_button()
        
    def draw(self):

        self.draw_restart_button()
        self.draw_quit_button() 

        # additional text        
        draw_text("Paused", self.font, self.text_colour, (700, 200), self.screen)

    def draw_restart_button(self):
        # restart buttons
        self.restart_level = self.restart_button.button_logic()
        self.restart_button.draw()
        draw_text("Restart", self.font, self.text_colour, (self.restart_button.left+5, self.restart_button.top), self.screen)

    def draw_quit_button(self):
        self.quit = self.quit_button.button_logic()
        self.quit_button.draw()
        draw_text("Quit", self.font, self.text_colour, (self.quit_button.left+40, self.quit_button.top), self.screen)    

    def draw_start_button(self):
        self.game_started = self.start_button.button_logic()
        self.start_button.draw()
        draw_text("Play", self.font, self.text_colour, (self.restart_button.left+40, self.restart_button.top), self.screen)
