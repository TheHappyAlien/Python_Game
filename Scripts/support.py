import os
import pygame

def import_folder(path):
    image_list = []
    for _, _, files in os.walk(path):
        for file in files:
            full_path = path + '/' + file
            image = pygame.image.load(full_path).convert_alpha()
            image_list.append(image)
    return image_list



def draw_text(text, font, text_col, pos, screen):
    img = font.render(text, True, text_col)
    screen.blit(img, pos)

def draw_number(number, font, text_col, pos, display_surface):     
    draw_text(str(number), font, text_col, pos, display_surface)     