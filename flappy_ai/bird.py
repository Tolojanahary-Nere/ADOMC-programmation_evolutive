import pygame

class Bird:
    """Représente l'oiseau (l'agent IA) avec un style sphérique 3D."""
    MAX_ROTATION = 25
    ROT_VEL = 20
    ANIMATION_TIME = 5
    RADIUS = 15

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.tilt = 0
        self.tick_count = 0
        self.vel = 0
        self.height = self.y

    def jump(self):
        """L'oiseau saute."""
        self.vel = -10.5
        self.tick_count = 0
        self.height = self.y

    def move(self):
        """Gère la physique (gravité et mouvement vertical)."""
        self.tick_count += 1

        # Equation de mouvement (parabole)
        d = self.vel * self.tick_count + 1.5 * self.tick_count**2

        # Terminal velocity
        if d >= 16:
            d = 16
        if d < 0:
            d -= 2

        self.y = self.y + d

        # Tilt up
        if d < 0 or self.y < self.height + 50:
            if self.tilt < self.MAX_ROTATION:
                self.tilt = self.MAX_ROTATION
        else:
            # Tilt down
            if self.tilt > -90:
                self.tilt -= self.ROT_VEL

    def draw(self, win):
        """Dessine l'oiseau comme une sphère pseudo-3D."""
        # Couleur principale jaune/orangé
        base_color = (255, 200, 0)
        
        # On va utiliser des cercles concentriques pour créer un effet de sphère éclairée
        for r in range(self.RADIUS, 0, -2):
            # Plus le cercle est petit, plus il est clair, et on le décale légèrement en haut à gauche
            factor = 1.0 + ((self.RADIUS - r) / self.RADIUS) * 0.8
            color = (
                min(255, int(base_color[0] * factor)),
                min(255, int(base_color[1] * factor)),
                min(255, int(base_color[2] * factor))
            )
            
            offset_x = int((self.RADIUS - r) * 0.3)
            offset_y = int((self.RADIUS - r) * 0.3)
            
            pygame.draw.circle(win, color, (int(self.x) - offset_x, int(self.y) - offset_y), r)
            
        # Oeil
        eye_x = int(self.x + self.RADIUS * 0.4)
        eye_y = int(self.y - self.RADIUS * 0.2)
        pygame.draw.circle(win, (255, 255, 255), (eye_x, eye_y), 6) # Blanc de l'oeil
        pygame.draw.circle(win, (0, 0, 0), (eye_x + 2, eye_y), 3) # Pupille
        
        # Bec (simple triangle)
        pygame.draw.polygon(win, (255, 100, 0), [
            (self.x + self.RADIUS * 0.8, self.y + 2),
            (self.x + self.RADIUS * 1.5, self.y + 5),
            (self.x + self.RADIUS * 0.8, self.y + 10)
        ])

    def get_mask(self):
        """Pour la compatibilité de collision parfaite, bien que l'on utilise un cercle."""
        # Not strictly needed since we use circular collision in Pipe, 
        # but kept if we switch to image masks later.
        pass
