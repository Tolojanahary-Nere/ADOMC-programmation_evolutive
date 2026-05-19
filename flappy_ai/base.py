import pygame

class Base:
    """Représente le sol défilant avec un effet pseudo-3D."""
    VELOCITY = 5
    WIDTH = 500  # Largeur typique de l'écran

    def __init__(self, y):
        self.y = y
        self.x1 = 0
        self.x2 = self.WIDTH
        self.height = 100

    def move(self):
        """Déplace le sol vers la gauche."""
        self.x1 -= self.VELOCITY
        self.x2 -= self.VELOCITY

        if self.x1 + self.WIDTH < 0:
            self.x1 = self.x2 + self.WIDTH

        if self.x2 + self.WIDTH < 0:
            self.x2 = self.x1 + self.WIDTH

    def draw(self, win):
        """Dessine le sol avec des ombres pour l'effet 3D."""
        # Couleur de base
        pygame.draw.rect(win, (222, 216, 149), (self.x1, self.y, self.WIDTH, self.height))
        pygame.draw.rect(win, (222, 216, 149), (self.x2, self.y, self.WIDTH, self.height))
        
        # Ombre supérieure pour la profondeur
        pygame.draw.rect(win, (115, 191, 46), (self.x1, self.y, self.WIDTH, 15))
        pygame.draw.rect(win, (115, 191, 46), (self.x2, self.y, self.WIDTH, 15))
        
        # Ligne d'ombre
        pygame.draw.line(win, (84, 140, 33), (self.x1, self.y + 15), (self.x1 + self.WIDTH, self.y + 15), 3)
        pygame.draw.line(win, (84, 140, 33), (self.x2, self.y + 15), (self.x2 + self.WIDTH, self.y + 15), 3)

        # Motifs pour voir le mouvement (lignes diagonales ou hachures)
        for i in range(0, self.WIDTH, 40):
            pygame.draw.line(win, (200, 190, 130), (self.x1 + i, self.y + 18), (self.x1 + i - 20, self.y + self.height), 3)
            pygame.draw.line(win, (200, 190, 130), (self.x2 + i, self.y + 18), (self.x2 + i - 20, self.y + self.height), 3)
