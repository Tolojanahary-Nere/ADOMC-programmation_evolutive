# Flappy Bird AI avec Programmation Évolutive (NEAT)

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Pygame](https://img.shields.io/badge/Pygame-2.5+-green.svg)
![NEAT](https://img.shields.io/badge/NEAT-Python-orange.svg)

Un projet complet d'intelligence artificielle appliquant l'algorithme génétique **NEAT (NeuroEvolution of Augmenting Topologies)** pour apprendre à jouer à Flappy Bird, avec un rendu visuel **pseudo-3D** et un suivi des performances via **TensorBoard**.

## 🎯 Objectif du Projet

L'objectif est d'entraîner une population d'agents (oiseaux) à naviguer à travers des tuyaux générés aléatoirement sans intervention humaine. À chaque génération, les meilleurs individus sont sélectionnés, croisés et mutés pour améliorer les performances globales de l'espèce.

## ✨ Fonctionnalités

- **Jeu Complet :** Physique de gravité, sauts, génération infinie de tuyaux, système de score.
- **Rendu 3D (Pseudo-3D) :** Tuyaux cylindriques avec ombrage, oiseaux sphériques éclairés, défilement avec profondeur.
- **Menu Interactif :** Interface claire pour lancer l'entraînement ou jouer avec le meilleur agent.
- **Algorithme NEAT :** Réseaux de neurones *FeedForward* évoluant génération après génération.
- **TensorBoard :** Suivi en temps réel de la *Fitness* maximale, moyenne, et des scores.
- **Exportation des Modèles :** Sauvegarde et rechargement automatique du meilleur cerveau IA via `pickle`.

## 🧠 Explications Pédagogiques (Algorithme NEAT)

1. **Fitness (Score de santé) :** Chaque oiseau gagne +0.1 point par frame de survie, et +5 points lorsqu'il passe un tuyau. S'il touche un obstacle, il est pénalisé (-1) et éliminé.
2. **Réseau de Neurones :**
   - **Inputs (3) :** Position Y de l'oiseau, distance jusqu'au prochain tuyau, hauteur de l'ouverture du tuyau.
   - **Output (1) :** Probabilité de sauter (si > 0.5, l'oiseau saute).
3. **Sélection Naturelle :** À la fin d'une génération, les réseaux ayant la meilleure fitness sont conservés.
4. **Croisement (Crossover) & Mutation :** Les "gènes" (poids, biais, connexions) des meilleurs oiseaux sont combinés, avec une probabilité de mutation (modification aléatoire d'une valeur) pour créer la génération suivante.

## 🛠️ Installation et Lancement

### 1. Prérequis

Assurez-vous d'avoir Python 3.8+ installé. 

### 2. Cloner et installer les dépendances

Ouvrez un terminal et exécutez les commandes exactes suivantes :

```bash
pip install pygame neat-python matplotlib tensorboard tensorboardX
```

Ou via le fichier requirements :
```bash
pip install -r requirements.txt
```

### 3. Lancer le projet

```bash
python main.py
```

- Appuyez sur **[1]** pour lancer l'entraînement (les oiseaux apprendront à jouer).
- Appuyez sur **[2]** pour lancer une partie avec le meilleur modèle pré-entraîné (s'il a été sauvegardé).
- Appuyez sur **[3]** pour quitter.

### 4. Suivre les statistiques avec TensorBoard

Pendant ou après l'entraînement, ouvrez un nouveau terminal dans le dossier du projet et lancez :

```bash
tensorboard --logdir=runs/flappy_neat
```
Ouvrez ensuite votre navigateur à l'adresse http://localhost:6006.

## 🚀 Améliorations Possibles

- **Topologie Visuelle :** Afficher le réseau de neurones en direct sur l'écran.
- **Modes de difficulté :** Réduire l'espacement des tuyaux (gap) au fil des générations pour forcer une meilleure précision.
- **Apprentissage par Renforcement :** Comparer les performances de NEAT avec un algorithme Deep Q-Learning (DQN).

## 🗂️ Structure du Code

```text
/flappy_ai
│
├── main.py                # Point d'entrée, Menu, Boucle de jeu et NEAT
├── bird.py                # Classe Oiseau (Physique et rendu sphérique 3D)
├── pipe.py                # Classe Tuyau (Rendu cylindrique)
├── base.py                # Classe Sol (Défilement et profondeur)
├── config-feedforward.txt # Configuration de l'algorithme NEAT
├── requirements.txt       # Liste des dépendances Python
├── README.md              # Documentation
├── utils/                 
│   ├── model_manager.py   # Gestion de l'enregistrement Pickle
│   └── stats_logger.py    # Suivi TensorBoard
```
