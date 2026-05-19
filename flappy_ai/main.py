import pygame
import neat
import os
import sys

from bird import Bird
from pipe import Pipe
from base import Base
from utils.stats_logger import StatsLogger
from utils.model_manager import ModelManager

# Initialisation Pygame
pygame.font.init()
WIN_WIDTH = 500
WIN_HEIGHT = 800
WIN = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption("Flappy Bird AI - 3D NEAT")

STAT_FONT = pygame.font.SysFont("comicsans", 30)
TITLE_FONT = pygame.font.SysFont("comicsans", 50, bold=True)

# Variables globales pour le suivi
gen = 0
logger = StatsLogger()
model_manager = ModelManager()

def draw_background(win):
    """Dessine un fond avec un dégradé bleu (ciel)."""
    color_top = (135, 206, 235)  # Sky blue
    color_bottom = (255, 255, 255) # White
    for y in range(WIN_HEIGHT):
        ratio = y / WIN_HEIGHT
        r = int(color_top[0] * (1 - ratio) + color_bottom[0] * ratio)
        g = int(color_top[1] * (1 - ratio) + color_bottom[1] * ratio)
        b = int(color_top[2] * (1 - ratio) + color_bottom[2] * ratio)
        pygame.draw.line(win, (r, g, b), (0, y), (WIN_WIDTH, y))

def draw_window(win, birds, pipes, base, score, gen, pipe_ind, mode="Train"):
    """Gère l'affichage principal."""
    draw_background(win)

    for pipe in pipes:
        pipe.draw(win)

    base.draw(win)

    for bird in birds:
        bird.draw(win)

    # UI Stats
    text = STAT_FONT.render("Score: " + str(score), 1, (255, 255, 255))
    win.blit(text, (WIN_WIDTH - 10 - text.get_width(), 10))

    if mode == "Train":
        text = STAT_FONT.render("Génération: " + str(gen), 1, (255, 255, 255))
        win.blit(text, (10, 10))
        
        text = STAT_FONT.render("Vivants: " + str(len(birds)), 1, (255, 255, 255))
        win.blit(text, (10, 50))

    pygame.display.update()

def eval_genomes(genomes, config):
    """Fonction de fitness de NEAT, entraîne les réseaux neuronaux."""
    global gen
    gen += 1
    
    nets = []
    birds = []
    ge = []

    for _, genome in genomes:
        genome.fitness = 0  # Départ avec fitness 0
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        nets.append(net)
        birds.append(Bird(230, 350))
        ge.append(genome)

    base = Base(730)
    pipes = [Pipe(600)]
    score = 0

    clock = pygame.time.Clock()
    
    run = True
    while run and len(birds) > 0:
        clock.tick(60) # Limité à 60 FPS

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                sys.exit()

        pipe_ind = 0
        if len(birds) > 0:
            if len(pipes) > 1 and birds[0].x > pipes[0].x + pipes[0].WIDTH:
                pipe_ind = 1

        for x, bird in enumerate(birds):
            bird.move()
            ge[x].fitness += 0.1 # Récompense pour rester en vie

            # Output du réseau
            output = nets[x].activate((
                bird.y,
                abs(bird.y - pipes[pipe_ind].height),
                abs(bird.y - pipes[pipe_ind].bottom)
            ))

            if output[0] > 0.5:
                bird.jump()

        base.move()

        rem = []
        add_pipe = False
        for pipe in pipes:
            pipe.move()
            # Collision
            for bird in birds:
                if pipe.collide(bird):
                    ge[birds.index(bird)].fitness -= 1 # Pénalité
                    nets.pop(birds.index(bird))
                    ge.pop(birds.index(bird))
                    birds.pop(birds.index(bird))
                elif not pipe.passed and pipe.x < bird.x:
                    pipe.passed = True
                    add_pipe = True

            if pipe.x + pipe.WIDTH < 0:
                rem.append(pipe)

        if add_pipe:
            score += 1
            for genome in ge:
                genome.fitness += 5 # Récompense de passage
            pipes.append(Pipe(WIN_WIDTH))
            
            # Si le score est suffisant, on considère que l'IA est parfaite
            # Cela permet de terminer la génération et de valider l'entraînement
            if score >= 50:
                break
                
        for r in rem:
            pipes.remove(r)

        # Collision avec le sol ou le plafond
        for bird in birds:
            if bird.y + bird.RADIUS >= 730 or bird.y - bird.RADIUS < 0:
                nets.pop(birds.index(bird))
                ge.pop(birds.index(bird))
                birds.pop(birds.index(bird))

        draw_window(WIN, birds, pipes, base, score, gen, pipe_ind)
        
    # Fin de la génération, on log les stats
    if genomes:
        max_fit = max([g.fitness for _, g in genomes])
        avg_fit = sum([g.fitness for _, g in genomes]) / len(genomes)
        logger.log_generation(gen, max_fit, avg_fit, score)

def train_ai(config_path):
    """Configuration et lancement de l'entraînement."""
    config = neat.config.Config(
        neat.DefaultGenome, neat.DefaultReproduction,
        neat.DefaultSpeciesSet, neat.DefaultStagnation,
        config_path
    )

    p = neat.Population(config)
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)

    # Entraînement sur 50 générations max
    try:
        best_genome = p.run(eval_genomes, 50)
    except (Exception, KeyboardInterrupt):
        print("\nEntraînement interrompu. Récupération du meilleur modèle actuel...")
        best_genome = p.best_genome
    
    # Sauvegarde du meilleur modèle
    if best_genome is not None:
        print("Sauvegarde du meilleur modèle...")
        model_manager.save_model(best_genome)
    else:
        print("Aucun modèle à sauvegarder.")
    
def play_best_ai(config_path):
    """Joue avec le meilleur modèle sauvegardé."""
    genome = model_manager.load_model()
    if not genome:
        print("Veuillez d'abord entraîner un modèle.")
        return
        
    config = neat.config.Config(
        neat.DefaultGenome, neat.DefaultReproduction,
        neat.DefaultSpeciesSet, neat.DefaultStagnation,
        config_path
    )
    
    net = neat.nn.FeedForwardNetwork.create(genome, config)
    bird = Bird(230, 350)
    base = Base(730)
    pipes = [Pipe(600)]
    score = 0
    clock = pygame.time.Clock()
    
    run = True
    while run:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                sys.exit()

        pipe_ind = 0
        if len(pipes) > 1 and bird.x > pipes[0].x + pipes[0].WIDTH:
            pipe_ind = 1
            
        bird.move()
        output = net.activate((
            bird.y,
            abs(bird.y - pipes[pipe_ind].height),
            abs(bird.y - pipes[pipe_ind].bottom)
        ))

        if output[0] > 0.5:
            bird.jump()
            
        base.move()
        
        rem = []
        add_pipe = False
        for pipe in pipes:
            pipe.move()
            if pipe.collide(bird):
                run = False # Perd le jeu
                
            if not pipe.passed and pipe.x < bird.x:
                pipe.passed = True
                add_pipe = True
                
            if pipe.x + pipe.WIDTH < 0:
                rem.append(pipe)

        if add_pipe:
            score += 1
            pipes.append(Pipe(WIN_WIDTH))

        for r in rem:
            pipes.remove(r)
            
        if bird.y + bird.RADIUS >= 730 or bird.y - bird.RADIUS < 0:
            run = False

        draw_window(WIN, [bird], pipes, base, score, 0, pipe_ind, mode="Play")
        
def main_menu():
    """Interface utilisateur principale."""
    run = True
    while run:
        draw_background(WIN)
        
        title = TITLE_FONT.render("Flappy Bird AI 3D", 1, (255, 255, 255))
        WIN.blit(title, (WIN_WIDTH//2 - title.get_width()//2, 150))
        
        opt1 = STAT_FONT.render("[1] Entraîner l'IA", 1, (200, 200, 200))
        opt2 = STAT_FONT.render("[2] Jouer le Meilleur Agent", 1, (200, 200, 200))
        opt3 = STAT_FONT.render("[3] Quitter", 1, (200, 200, 200))
        
        WIN.blit(opt1, (WIN_WIDTH//2 - opt1.get_width()//2, 350))
        WIN.blit(opt2, (WIN_WIDTH//2 - opt2.get_width()//2, 450))
        WIN.blit(opt3, (WIN_WIDTH//2 - opt3.get_width()//2, 550))
        
        pygame.display.update()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.KEYDOWN:
                local_dir = os.path.dirname(__file__)
                config_path = os.path.join(local_dir, 'config-feedforward.txt')
                
                if event.key == pygame.K_1:
                    train_ai(config_path)
                elif event.key == pygame.K_2:
                    play_best_ai(config_path)
                elif event.key == pygame.K_3:
                    run = False
                    pygame.quit()
                    sys.exit()

if __name__ == '__main__':
    main_menu()
