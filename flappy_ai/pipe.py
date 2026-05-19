import pygame
import random

class Pipe:
    """Représente les obstacles (Tuyaux) avec rendu pseudo-3D cylindrique."""
    GAP = 200 # Espace entre les tuyaux (ajusté pour apprentissage)
    VELOCITY = 5
    WIDTH = 70

    def __init__(self, x):
        self.x = x
        self.height = 0
        self.top = 0
        self.bottom = 0
        self.passed = False
        self.set_height()

    def set_height(self):
        """Définit aléatoirement la hauteur des tuyaux."""
        self.height = random.randrange(50, 450)
        self.top = self.height - 800  # -800 pour dessiner vers le haut hors écran
        self.bottom = self.height + self.GAP

    def move(self):
        """Fait avancer les tuyaux vers la gauche."""
        self.x -= self.VELOCITY

    def draw_cylinder_rect(self, win, x, y, w, h, base_color):
        """Dessine un rectangle avec un dégradé simulant un cylindre 3D."""
        # On divise le rectangle en plusieurs bandes verticales
        steps = 10
        r, g, b = base_color
        for i in range(steps):
            # Calcul d'un facteur d'ombre (centre plus clair, bords plus sombres)
            # Factor va de ~0.5 sur les bords à 1.2 au centre
            dist = abs(i - steps/2) / (steps/2)
            factor = 1.2 - (dist * 0.7)
            
            shade = (
                min(255, int(r * factor)),
                min(255, int(g * factor)),
                min(255, int(b * factor))
            )
            
            strip_width = w / steps
            pygame.draw.rect(win, shade, (x + i * strip_width, y, strip_width + 1, h))
            
    def draw(self, win):
        """Dessine le tuyau haut et bas."""
        base_green = (115, 191, 46)
        
        # Tuyau du haut
        # Corps
        self.draw_cylinder_rect(win, self.x, 0, self.WIDTH, self.height, base_green)
        # Bordure / Col (un peu plus large)
        self.draw_cylinder_rect(win, self.x - 4, self.height - 30, self.WIDTH + 8, 30, base_green)
        
        # Tuyau du bas
        # Corps
        self.draw_cylinder_rect(win, self.x, self.bottom, self.WIDTH, 800, base_green)
        # Bordure / Col
        self.draw_cylinder_rect(win, self.x - 4, self.bottom, self.WIDTH + 8, 30, base_green)

    def collide(self, bird):
        """Vérifie la collision entre l'oiseau et les tuyaux (hitbox circulaire/rectangulaire)."""
        bird_rect = pygame.Rect(bird.x - bird.RADIUS, bird.y - bird.RADIUS, bird.RADIUS*2, bird.RADIUS*2)
        
        # Rectangles des tuyaux
        top_rect = pygame.Rect(self.x, 0, self.WIDTH, self.height)
        bottom_rect = pygame.Rect(self.x, self.bottom, self.WIDTH, 800)
        
        # Tolérance de collision (pour être un peu plus permissif car visuel 3D)
        if bird_rect.colliderect(top_rect) or bird_rect.colliderect(bottom_rect):
            return True
        return False
