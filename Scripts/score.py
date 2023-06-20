import pygame
from os import path

class Score():
    def __init__(self) -> None:
        self.score = 0
        self.high_score = 0
        if path.exists('./high_score.txt'):
            with open('./high_score.txt') as f:
                self.high_score = int(f.read())

    def save_score(self):
        with open('./high_score.txt', 'w') as f:        
            if self.score > self.high_score:
                f.write(str(self.score))
            else:
                f.write(str(self.score))           