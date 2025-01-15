# Bataille Navale

## Description
Ceci est un jeu de Bataille Navale classique implémenté en Python avec Tkinter, proposant une interface 
graphique où les joueurs peuvent placer leurs navires et jouer contre un adversaire informatique. Le 
jeu offre deux niveaux de difficulté et une expérience de jeu interactive.

## Fonctionnalités
- Interface graphique utilisant Tkinter
- Deux niveaux de difficulté : Facile et Difficile
- Phase de placement des navires pour le joueur
- Intelligence artificielle informatique avec deux modes de difficulté
- Retour visuel pour les tirs, les manqués et les navires coulés
- Suivi de l'état du jeu et détection de fin de partie

## Règles du Jeu
1. **Placement des Navires**
   - Le joueur place ses navires sur sa grille
   - Navires disponibles :
     - 1 navire de taille 5
     - 1 navire de taille 4
     - 2 navires de taille 3
     - 2 navires de taille 2
   - Les navires peuvent être placés horizontalement ou verticalement
   - L'ia place ses navires aléatoirement

2. **Déroulement du Jeu**
   - Le joueur et l'ia tirent à tour de rôle sur la grille de l'adversaire
   - Les touches sont marquées en rouge
   - Les tirs manqués sont marqués en bleu
   - Les navires coulés sont marqués en rouge foncé
   - Le premier joueur à couler tous les navires de l'adversaire gagne

## Modes de Difficulté
- **Mode Facile** : 
  - L'ordinateur tire de manière aléatoire
- **Mode Difficile** :
  - Ciblage intelligent
  - Suit et analyse les touches de navires
  - Essaie de couler les navires de manière systématique

### Explication de l'algorithme de tir difficile

#### Au démarrage
- L'IA n'a aucune information sur les positions des bateaux
- Elle commence avec des tirs aléatoires

#### Lorsqu'un bateau est touché (case devient rouge)
- L'IA mémorise cette position comme point de départ
- Elle choisit une direction aléatoire parmi les cases adjacentes disponibles
- Elle continue de tirer dans cette direction tant qu'elle touche le bateau

#### Si un tir manque après avoir touché
- L'IA change de direction en partant du point initial
- Elle teste dans le sens opposé à la première direction
- Si cette direction ne fonctionne pas non plus, elle change d'axe
- Par exemple: Si vertical ne marche pas, elle passe à l'horizontal

#### Lorsqu'un bateau est coulé (cases deviennent rouge foncé)
- L'IA cherche parmi toutes les cases rouges restantes
- Elle sélectionne une case rouge qui a des cases adjacentes libres
- Elle reprend sa stratégie depuis cette nouvelle position
- Cela lui permet de poursuivre la destruction d'un bateau déjà touché

## Prérequis
- Python 3 au moins
- Tkinter (installé par défaut avec Python)

## Comment Lancer le Jeu
```bash
python main.py
```

## Commandes
- Cliquez sur le bouton "Changer Orientation" pour modifier l'orientation du placement des navires
- Sélectionnez le niveau de difficulté à l'aide des boutons radio avant de commencer le jeu
- Placez vos navires en cliquant sur votre grille
- Cliquez sur la grille de l'ordinateur pour tirer
