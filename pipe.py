import pygame
import random

class Pipe(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.xDefault = 574
        self.xspeed = -4
        self.w = 104
        self.h = 1210
        birdimg = pygame.image.load("assets/pipes.png").convert_alpha()
        birdimg.set_colorkey((255, 255, 255))
        self.image = birdimg
        self.rect = self.image.get_rect()
        self.rect.x = self.xDefault
        self.y = random.randint(200, 600)
        self.rect.y = self.y - self.h/2


    def update(self):
        self.rect.x += self.xspeed
        
    def reset(self):
        self.listPipes = [(self.xDefault, random.randint(250, 550))]

    def draw(self, win):
        win.blit(self.image, (self.rect.x, self.rect.y))

    