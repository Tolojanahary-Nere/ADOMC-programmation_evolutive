from tensorboardX import SummaryWriter
import os

class StatsLogger:
    def __init__(self, log_dir="runs/flappy_neat"):
        """Gère la journalisation des statistiques avec TensorBoard."""
        self.writer = SummaryWriter(log_dir)

    def log_generation(self, gen, max_fitness, avg_fitness, max_score):
        """Enregistre les statistiques d'une génération."""
        self.writer.add_scalar("Fitness/Max", max_fitness, gen)
        self.writer.add_scalar("Fitness/Average", avg_fitness, gen)
        self.writer.add_scalar("Score/Max", max_score, gen)
        
    def close(self):
        """Ferme le writer."""
        self.writer.close()
