import pygame
import neat
import os
import sys
from bird import Bird
from ground import Ground
from pipe import Pipe
from score import Score

class game:
    def __init__(self):
        pygame.init()
        self.w = 576
        self.h = 1024
        self.clock = pygame.time.Clock() 
        self.win = pygame.display.set_mode((self.w, self.h))
        
        self.gameOverBoucle = False
        pygame.display.set_caption("Flappy Bird")
        self.bg = pygame.image.load("assets/bg1.png").convert_alpha()
        self.startingimage = pygame.image.load("assets/startingscreen.png").convert_alpha()
        self.launch = False
        self.list_pipes = []
        self.bird = Bird(self.w//6, 400 - 25)
        self.ground = Ground()
        self.score = Score()
        
        

    def runSolo(self):
        self.timeClock = 0
        self.game = True
        self.all_sprites_list = pygame.sprite.RenderUpdates()
        self.all_sprites_list.add(self.bird)
        self.all_sprites_list.add(self.ground)
        self.win.blit(self.bg, (0, 0))
        pygame.display.update()

        while self.game: 
            for event in pygame.event.get():
                if event.type == pygame.QUIT: 
                    self.game = False
                    sys.exit()

            self.updateScore()
            self.ground.update()
            self.bird.updateImgs()
            self.all_sprites_list.remove(self.bird)
            self.all_sprites_list.add(self.bird)

            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE] and not self.launch and self.timeClock > 5:
                self.bird.jump()
                self.launch = True
                self.win.blit(self.bg, (0, 0))
                self.list_pipes.append(Pipe())
                self.all_sprites_list.add(self.list_pipes[-1])
            

            if keys[pygame.K_SPACE] and self.launch: # Le joueur appuie sur espace et la partie est lancée
                self.bird.jump() # Utilise la méthode "Jump" de l'instance bird du jeu

            if self.launch:
                self.bird.affectGravity() # On affecte la gravité à l'oiseau
                if self.list_pipes[-1].rect.x <= (2*self.w)//5: # Si le dernier Pipe a passé l'oiseau 
                    self.list_pipes.append(Pipe()) # On créé un nouveau Pipe qui sera généré tout à droite
                    self.all_sprites_list.add(self.list_pipes[-1])
                if self.list_pipes[0].rect.x <= -self.list_pipes[0].w: # Si le Pipe sort de l'écran
                    self.list_pipes.pop(0) # Supprime le Pipe de la liste
                    
                    self.all_sprites_list.remove(self.list_pipes[0])
                    
                for pipe in self.list_pipes: # Itère dans la liste de tous les Pipes
                    pipe.update() # Met à jour la position X des Pipes en utilsant leur méthode correspondante
                    if self.bird.collide(pipe): # Si la méthode collide de Bird renvoie True = L'oiseau entre en contact avec le Pipe
                        self.launch = False 
                        self.game = False
                        self.gameOverScreen() # Arrete toutes les variables et lance l'écran de fin
                        return
            else:
                self.win.blit(self.startingimage, (117, 150))

            self.all_sprites_list.remove(self.ground)
            self.all_sprites_list.add(self.ground)

            
            if self.game:                
                self.all_sprites_list.update()
                self.all_sprites_list.clear(self.win, self.bg)
                spriteslist = self.all_sprites_list.draw(self.win)
                pygame.display.update(spriteslist)
                self.score.draw(self.win)
                self.timeClock += 1
            self.clock.tick(30)
    
    def runBot(self, genomes, config):
        nets = []
        ge = []
        birds = []
        
        for i, g in genomes:
            net = neat.nn.FeedForwardNetwork.create(g, config)
            nets.append(net)
            birds.append(Bird(self.w//6, 400 - 25))
            g.fitness = 0
            ge.append(g)
        
        self.timeClock = 0
        self.game = True

        
        self.list_pipes.append(Pipe())


        while self.game: 
            for event in pygame.event.get():
                if event.type == pygame.QUIT: 
                    self.game = False
                    sys.exit()
                    
                
            pipe_ind = 0
            if len(birds) > 0:
                if len(self.list_pipes) > 1 and birds[0].rect.x > self.list_pipes[0].rect.x + self.list_pipes[0].rect.w:
                    pipe_ind = 1
            else:
                self.game = False
                self.reset()
                break
            
            
                    
            for x, bird in enumerate(birds):
                bird.updateImgs()
                bird.affectGravity()
                for pipe in self.list_pipes:
                    if pipe.rect.x <= bird.rect.x and pipe.rect.x >= bird.rect.x + self.ground.xspeed:
                        bird.score += 1
                ge[x].fitness += 0.01
                output = nets[x].activate((bird.rect.y, abs(bird.rect.y - (self.list_pipes[pipe_ind].y + 100)), abs(bird.rect.y - (self.list_pipes[pipe_ind].y - 100))))
                
                if output[0] > 0.5:
                    bird.jump()
                            

            self.ground.update()
            
            
            
                
            if self.list_pipes[-1].rect.x <= (2*self.w)//5:    
                self.list_pipes.append(Pipe())
            if self.list_pipes[0].rect.x <= -self.list_pipes[0].w:

                self.list_pipes.pop(0)
            for pipe in self.list_pipes:
                pipe.update()
                for i, bird in enumerate(birds):
                    if bird.collide(pipe):
                        ge[i].fitness -= 1
                        birds.pop(i)
                        nets.pop(i)
                        ge.pop(i)
                        
                    if pipe.rect.x <= bird.rect.x and pipe.rect.x >= bird.rect.x + self.ground.xspeed:
                        for g in ge:
                            g.fitness += 5

            
            if self.game:        
                self.win.blit(self.bg, (0, 0))
                for pipe in self.list_pipes:
                    pipe.draw(self.win)
                self.ground.draw(self.win)
                
                for bird in birds:
                    bird.draw(self.win)
                
                
                pygame.display.update()
                self.timeClock += 1
            self.clock.tick(30)

    def reset(self):
        self.score.reset()
        self.bird.reset()
        self.list_pipes = []
        self.ground.reset()
        self.win.blit(self.bg, (0, 0))

    def updateScore(self):
        for pipe in self.list_pipes:
            if pipe.rect.x <= self.bird.rect.x and pipe.rect.x >= self.bird.rect.x + self.ground.xspeed:
                self.score.addscore()
                self.win.blit(self.bg, (0, 0))

    def gameOverScreen(self):
        self.gameOverBoucle = True
        self.timeClock = 0
        while self.gameOverBoucle:
            for event in pygame.event.get():
                if event.type == pygame.QUIT: 
                    self.gameOverBoucle = False
                    return
            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE] and self.timeClock >= 20:
                self.gameOverBoucle = False
                for pipe in self.list_pipes:
                    self.all_sprites_list.remove(pipe)    
                self.reset()
                self.runSolo()
                return
            self.score.updateNewHighscore(self.win)
            self.all_sprites_list.clear(self.win, self.bg)
            self.bird.draw(self.win)
            for pipe in self.list_pipes:
                pipe.draw(self.win)
            self.ground.draw(self.win)
            self.score.draw(self.win)
            self.score.draw_panel(self.win)
            pygame.display.update()

            self.timeClock += 1
        pygame.quit()
 
if __name__ == "__main__":    
    jeu = game()
    jeu.runSolo()
