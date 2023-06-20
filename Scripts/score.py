import pygame
from os import path

class Score():
    def __init__(self, username) -> None:
        self.score = 0
        self.high_score = 0
        self.username = username
        if path.exists('./high_score.txt'):
            with open('./high_score.txt') as f:
                for line in f:
                    line_split = line.split(':')
                    if line_split[0] == self.username:
                        self.high_score = int(line_split[1])

    def save_score(self):
        score_saved = False
        with open('./high_score.txt', 'r') as f:
            lines = f.readlines()

        with open('./high_score.txt', 'w') as f: 
            for line in lines:
                line_split = line.strip('\n').split(':')

                if line_split[0] == self.username:
                    if self.score > self.high_score:
                        f.write(f"{self.username}:{self.score}\n")
                    else:
                        f.write(line)                        
                    score_saved = True 
                else:
                    f.write(line)
            if not score_saved:

                f.write(f"{self.username}:{self.score}\n")
                              