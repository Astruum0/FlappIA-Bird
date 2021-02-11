from game import game
import neat
import os

def Learn():
    jeu = game()
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "config-feedforward.txt")
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation, config_path)
    p = neat.Population(config)
    
    winner = p.run(jeu.runBot, 50)
    
if __name__ == "__main__":
    Learn()