import os
import pygame

def import_folder(path):
    image_list = []

    for _, _, files in os.walk(path):
        print(files)
        for file in files:
            full_path = path + '/' + file
            image = pygame.image.load(full_path).convert_alpha()
            image_list.append(image)
            print(full_path)
    return image_list