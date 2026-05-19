import os
import pickle

class ModelManager:
    def __init__(self, save_dir="models"):
        """Gère la sauvegarde et le chargement des modèles NEAT."""
        self.save_dir = save_dir
        if not os.path.exists(self.save_dir):
            os.makedirs(self.save_dir)

    def save_model(self, genome, filename="best_model.pkl"):
        """Sauvegarde le meilleur génome via pickle."""
        path = os.path.join(self.save_dir, filename)
        with open(path, "wb") as f:
            pickle.dump(genome, f)
        print(f"Modèle sauvegardé : {path}")

    def load_model(self, filename="best_model.pkl"):
        """Charge un génome sauvegardé."""
        path = os.path.join(self.save_dir, filename)
        if not os.path.exists(path):
            print(f"Aucun modèle trouvé à : {path}")
            return None
            
        with open(path, "rb") as f:
            genome = pickle.load(f)
        print(f"Modèle chargé : {path}")
        return genome
