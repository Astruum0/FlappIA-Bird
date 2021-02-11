import pygame

class Ground(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.w = 672
        self.h = 224
        self.xspeed = -4
        self.margin = 672 - 576
        groundimg = pygame.image.load("assets/ground.png").convert_alpha()
        groundimg.set_colorkey((255, 255, 255))
        self.image = groundimg
        self.rect = self.image.get_rect()
        self.rect.y = 800
        self.rect.x = 0

    def update(self):
        self.rect.x += self.xspeed
        if self.rect.x < -self.margin:
            self.rect.x = 0
        
    def reset(self):
        self.x = 0

    def draw(self, win):
        win.blit(self.image, (self.rect.x, self.rect.y))