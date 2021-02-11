import pygame

class Bird(pygame.sprite.Sprite):
    g = 4
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.yOrigin = y
        self.w = 71
        self.h = 50
        self.imgs = []
        self.score = 0
        for i in range(1, 5):
            self.imgs.append(pygame.image.load("assets/bird" + str(i) + ".png"))
        birdimg = self.imgs[0]
        birdimg.set_colorkey((255, 255, 255))
        self.image = birdimg
        self.rect = self.image.get_rect()
        self.vely = 0

        self.rect.x = x
        self.rect.y = y
        self.imgsIndex = 0
        self.ypos = self.yOrigin

    def updateImgs(self):
        self.imgsIndex += 1
        if self.imgsIndex > 3:
            self.imgsIndex = 0
        birdimg = self.imgs[self.imgsIndex]
        birdimg.set_colorkey((255, 255, 255))
        self.image = birdimg

    def jump(self):
        self.vely = -25 # Modifie le vecteur vitesse de l'oiseau de -25 (Négatif car vers le haut)

    def affectGravity(self):
        self.vely += Bird.g # Loi de Newton : la gravité est simulé en affectant une constante au vecteur vitesse
        self.rect.y += self.vely # On applique le vecteur vitesse à la position de l'oiseau

    def collide(self, pipe):   
        if ((self.rect.x-5 >= pipe.rect.x - self.w and self.rect.x+5 <= pipe.rect.x + pipe.w) and ((self.rect.y+5 <= pipe.y-self.h*2) or self.rect.y-5 > pipe.y+self.h)) or self.rect.y-5 > 800-self.h:
            return True
        else:
            return False

    def draw(self, win):
        win.blit(self.imgs[self.imgsIndex], (self.rect.x, self.rect.y))
                
    def reset(self):
        self.rect.y = self.yOrigin
        self.time = 0
        self.vjump = 0
        self.imgsIndex = 0
        self.ypos = self.rect.y
