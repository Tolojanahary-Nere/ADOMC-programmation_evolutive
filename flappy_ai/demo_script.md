# 🎓 Guide de Soutenance : Flappy Bird AI (NEAT)

Ce document est votre antisèche pour présenter le projet à vos professeurs. Vous pouvez le garder ouvert pendant votre démo.

## 1. Introduction (Théorie & Objectif)
*Gardez le jeu ouvert sur le Menu Principal.*

**Ce qu'il faut dire :**
> "Bonjour, pour mon projet, j'ai implémenté une Intelligence Artificielle capable d'apprendre à jouer à Flappy Bird, en partant de zéro. 
> Je n'ai programmé aucune règle du type 'S'il y a un obstacle, tu sautes'. J'ai utilisé **NEAT (NeuroEvolution of Augmenting Topologies)**. C'est un algorithme génétique qui simule la sélection naturelle de Darwin sur des réseaux de neurones."

## 2. Lancement & Explication (La phase d'apprentissage)
*Appuyez sur **[1] (Entraîner l'IA)**.*

**Ce qu'il faut dire (pendant que la génération 1 s'écrase) :**
> "Voici la première génération avec 50 oiseaux. Au départ, leurs 'cerveaux' (réseaux de neurones) sont générés aléatoirement, c'est pour cela qu'ils s'écrasent tous. 
> Chaque oiseau possède :
> - **3 Capteurs (Inputs) :** Sa hauteur actuelle, la distance du tuyau, et la hauteur du tuyau.
> - **1 Action (Output) :** Une probabilité de sauter. S'il s'active à plus de 50%, l'oiseau saute."

## 3. L'Évolution (La sélection naturelle)
*Laissez l'IA atteindre la génération 3 ou 4, où elle commence à réussir.*

**Ce qu'il faut dire :**
> "À la fin de chaque génération, l'algorithme évalue la 'Fitness' (le score de survie) de chaque oiseau. Il récompense la durée de vie et le franchissement des tuyaux.
> Les pires sont éliminés. Les meilleurs sont sélectionnés, leurs 'gènes' sont croisés, et de petites mutations aléatoires sont ajoutées. Regardez, après quelques générations, l'espèce a évolué et comprend la physique du jeu !"

## 4. Preuve Graphique (TensorBoard)
*Basculez sur votre navigateur web (http://localhost:6006) pour montrer TensorBoard.*

**Ce qu'il faut dire :**
> "Pour valider scientifiquement cet apprentissage, j'ai mis en place un suivi en temps réel avec TensorBoard.
> Sur le graphique 'Fitness', vous pouvez voir la courbe monter drastiquement, ce qui prouve mathématiquement que la population optimise son comportement génération après génération. L'IA apprend bel et bien."

## 5. Le Résultat (Le 'Top Agent')
*Fermez la fenêtre du jeu, relancez `python main.py`, et appuyez sur **[2] (Jouer le Meilleur Agent)**.*

**Ce qu'il faut dire :**
> "Puisque l'IA a trouvé la solution optimale, mon programme a automatiquement sauvegardé le cerveau du meilleur individu. Plus besoin de ré-entraîner. 
> Voici cet agent parfait qui joue maintenant indéfiniment de manière autonome."

## 🌟 Points Bonus à mentionner si les profs posent des questions :
- **Le Style 3D :** "Pour rendre le projet visuellement professionnel, je n'ai pas utilisé de simples images plates. J'ai programmé un rendu **pseudo-3D** avec Pygame, en générant mathématiquement des dégradés cylindriques (pour les tuyaux) et des ombrages sphériques (pour les oiseaux), tout en gérant un effet de profondeur sur le sol."
- **Exportation :** "Le modèle neuronal est sérialisé et sauvegardé au format binaire (Pickle), permettant une utilisation immédiate en production."
