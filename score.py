import pygame
import os
import pickle

class Score:
    def __init__(self):
        self.score = 0
        self.numberMain = []
        for x in range(10):
            self.numberMain.append(pygame.image.load("assets/numbers/" + str(x) + ".png"))
        self.numberMini = []
        for x in range(10):
            self.numberMini.append(pygame.image.load("assets/gameover/" + str(x) + ".png"))
        self.panelImgs = []
        for material in ["Empty", "Bronze", "Iron", "Silver", "Gold"]:
            self.panelImgs.append(pygame.image.load("assets/gameover/panel" + material + ".png"))
        self.wPanel = 452
        self.hPanel = 228
        self.gameOverImg = pygame.image.load("assets/gameover/GameOver.png")
        self.wGO = 384
        self.new = pygame.image.load("assets/gameover/new.png")
        self.wMain = 48
        self.hMain = 72
        self.yMain = 50
        self.xMain = 287 - (self.wMain * 0.5)
        self.wMini = 28
        self.hMini = 40
        self.yMini = 1024//2 - self.hPanel//2 + 17*4
        self.xMini = 287 - self.wPanel//2 + 102*4 - self.wMini

        self.highScore = recupHighscore()
        self.yMiniHigh = 1024//2 - self.hPanel//2 + 38*4
        self.xMiniHigh = 287 - self.wPanel//2 + 102*4 - self.wMini * len(str(self.highScore))
        self.newHighscore = False
        

    def addscore(self):
        self.score += 1
        self.len = len(str(self.score))
        self.xMain = 287 - (self.wMain * 0.5 * self.len)
        self.xMini = 287 - self.wPanel//2 + 102*4 - self.wMini* self.len
    
    def draw(self, win):
        for i, number in enumerate(str(self.score)):
            win.blit(self.numberMain[int(number)], (self.xMain + i*self.wMain, self.yMain))

    def draw_panel(self, win):
        win.blit(self.panelImgs[self.score//10], (576//2-self.wPanel//2, 1024//2 - self.hPanel//2))
        win.blit(self.gameOverImg, (576//2-self.wGO//2, 250))
        for i, number in enumerate(str(self.score)):
            win.blit(self.numberMini[int(number)], (self.xMini + i*self.wMini, self.yMini))
        for i, number in enumerate(str(self.highScore)):
            win.blit(self.numberMini[int(number)], (self.xMiniHigh + i*self.wMini, self.yMiniHigh))
        if self.newHighscore:
            self.highScore = self.score
            win.blit(self.new, (576//2-self.wPanel//2 + 66*4, 1024//2 - self.hPanel//2 + 29*4))

    def updateNewHighscore(self, win):
        if self.score > self.highScore:
            self.newHighscore = True
            self.highScore = self.score
            saveHighscore(self.highScore)
            self.xMiniHigh = 287 - self.wPanel//2 + 102*4 - self.wMini * len(str(self.highScore))
    
    def reset(self):
        self.score = 0
        self.xMain = 287 - self.wMain * 0.5
        self.xMini = 287 - self.wPanel//2 + 102*4 - self.wMini
        self.newHighscore = False

def recupHighscore():
    if os.path.exists("highscoreFolder"): 
        fichier_scores = open("highscoreFolder", "rb")
        mon_depickler = pickle.Unpickler(fichier_scores)
        score = mon_depickler.load()
        fichier_scores.close()
    else:
        score = 0
    return score

def saveHighscore(score):
    fichier_scores = open("highscoreFolder", "wb")
    mon_pickler = pickle.Pickler(fichier_scores)
    mon_pickler.dump(score)
    fichier_scores.close()