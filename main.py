import tkinter as tk
from tkinter import messagebox
import random


class Ship:
    def __init__(self, size):
        self.size = size
        self.positions = []
        self.hits = []

    def is_sunk(self):
        return len(self.hits) == self.size


class Board:
    def __init__(self, is_computer=False):
        self.size = 10
        self.grid = [[0 for _ in range(self.size)] for _ in range(self.size)]
        self.ships = []
        self.is_computer = is_computer

    def can_place_ship(self, ship_size, x, y, horizontal):
        if horizontal:
            if x + ship_size > self.size:
                return False
            return all(self.grid[y][x + i] == 0 for i in range(ship_size))
        else:
            if y + ship_size > self.size:
                return False
            return all(self.grid[y + i][x] == 0 for i in range(ship_size))

    def place_ship(self, ship, x, y, horizontal):
        if horizontal:
            for i in range(ship.size):
                self.grid[y][x + i] = 1
                ship.positions.append((y, x + i))
        else:
            for i in range(ship.size):
                self.grid[y + i][x] = 1
                ship.positions.append((y + i, x))
        self.ships.append(ship)


class BattleshipGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Bataille Navale")

        self.player_board = Board()
        self.computer_board = Board(is_computer=True)
        self.setup_gui()
        self.current_ship_size = None
        self.ships_to_place = [(5, 1), (4, 1), (3, 2), (2, 2)]  # (taille, quantité)
        self.horizontal_placement = True
        self.game_started = False
        self.winner = None

        # Variables pour la difficulté
        self.difficulty = "facile"  # "facile" ou "difficile"
        self.last_hit = None  # Pour le mode difficile
        self.adjacent_cells = []  # Cases à cibler en mode difficile
        self.is_computer_turn = False  # Nouvelle variable pour bloquer les clics

        # Variables pour le mode difficile
        self.first_hit = None  # Première touche d'un navire
        self.current_direction = None  # 'N', 'S', 'E', 'W'
        self.current_axis = 'H'  # 'H' ou 'V'
        self.tried_directions = []  # Directions déjà essayées pour ce navire

        # Placement des navires de l'ordinateur
        self.place_computer_ships()

    def setup_gui(self):
        # Configuration de la fenêtre principale
        self.root.configure(bg='white')

        # Frame pour la difficulté
        difficulty_frame = tk.Frame(self.root, bg='white')
        difficulty_frame.pack(pady=5)

        tk.Label(difficulty_frame, text="Difficulté : ", bg='white').pack(side=tk.LEFT)
        self.difficulty_var = tk.StringVar(value="facile")
        tk.Radiobutton(difficulty_frame, text="Facile", variable=self.difficulty_var,
                       value="facile", command=self.change_difficulty, bg='white').pack(side=tk.LEFT)
        tk.Radiobutton(difficulty_frame, text="Difficile", variable=self.difficulty_var,
                       value="difficile", command=self.change_difficulty, bg='white').pack(side=tk.LEFT)

        # Frame pour les grilles
        grids_frame = tk.Frame(self.root, bg='white')
        grids_frame.pack(expand=True, fill='both', padx=20, pady=10)

        # Frame pour la grille du joueur
        player_container = tk.Frame(grids_frame, bg='white')
        player_container.pack(side=tk.LEFT, padx=10)

        # Grilles avec relief="groove" pour avoir l'aspect visuel de l'image
        tk.Label(player_container, text="Votre grille", bg='white').pack()
        self.player_frame = tk.Frame(player_container, relief="groove", borderwidth=1)
        self.player_frame.pack()

        # Frame pour les contrôles au centre
        control_frame = tk.Frame(grids_frame, bg='white', width=150, height=100)
        control_frame.pack(side=tk.LEFT, padx=10)
        control_frame.pack_propagate(False)  # Empêche la frame centrale de s'adapter à son contenu

        self.orientation_btn = tk.Button(control_frame, text="Changer Orientation",
                                         command=self.toggle_orientation)
        self.orientation_btn.pack(pady=5)

        # Label pour les messages de jeu au centre
        self.game_status_label = tk.Label(control_frame, text="", bg='white')
        self.game_status_label.pack(pady=5)

        # Frame du bas pour les instructions
        bottom_frame = tk.Frame(self.root, bg='white')
        bottom_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=5)

        self.instruction_label = tk.Label(bottom_frame, text="Placez vos navires", bg='white')
        self.instruction_label.pack()

        # Grille de l'ordinateur
        computer_container = tk.Frame(grids_frame, bg='white')
        computer_container.pack(side=tk.LEFT, padx=10)

        tk.Label(computer_container, text="Grille ordinateur", bg='white').pack()
        self.computer_frame = tk.Frame(computer_container, relief="groove", borderwidth=1)
        self.computer_frame.pack()

        # Configuration des grilles
        for i in range(10):
            for j in range(10):
                btn = tk.Button(self.player_frame, width=3, height=1, relief="groove", bg='light blue',
                                command=lambda x=i, y=j: self.handle_player_click(x, y))
                btn.grid(row=i, column=j, sticky="nsew")
                if not hasattr(self, 'player_buttons'):
                    self.player_buttons = []
                if len(self.player_buttons) <= i:
                    self.player_buttons.append([])
                self.player_buttons[i].append(btn)

                btn = tk.Button(self.computer_frame, width=3, height=1, relief="groove", bg='light blue',
                                command=lambda x=i, y=j: self.handle_computer_click(x, y))
                btn.grid(row=i, column=j, sticky="nsew")
                if not hasattr(self, 'computer_buttons'):
                    self.computer_buttons = []
                if len(self.computer_buttons) <= i:
                    self.computer_buttons.append([])
                self.computer_buttons[i].append(btn)

    def toggle_orientation(self):
        self.horizontal_placement = not self.horizontal_placement

    def handle_player_click(self, x, y):
        if not self.game_started and self.ships_to_place:
            self.try_place_ship(x, y)

    def try_place_ship(self, x, y):
        if not self.ships_to_place:
            return

        ship_size, count = self.ships_to_place[0]
        if self.player_board.can_place_ship(ship_size, y, x, self.horizontal_placement):
            ship = Ship(ship_size)
            self.player_board.place_ship(ship, y, x, self.horizontal_placement)

            # Mise à jour visuelle
            positions = ship.positions
            for pos in positions:
                self.player_buttons[pos[0]][pos[1]].configure(bg='gray')

            # Mise à jour des navires à placer
            if count > 1:
                self.ships_to_place[0] = (ship_size, count - 1)
            else:
                self.ships_to_place.pop(0)

            if not self.ships_to_place:
                self.start_game()

    def place_computer_ships(self):
        ships_to_place = [(5, 1), (4, 1), (3, 2), (2, 2)]

        for ship_size, count in ships_to_place:
            for _ in range(count):
                placed = False
                while not placed:
                    x = random.randint(0, 9)
                    y = random.randint(0, 9)
                    horizontal = random.choice([True, False])

                    if self.computer_board.can_place_ship(ship_size, y, x, horizontal):
                        ship = Ship(ship_size)
                        self.computer_board.place_ship(ship, y, x, horizontal)
                        placed = True

        self.print_ai_board()  # Déboggage

    # Gestion des clics sur la grille de l'ordinateur (par le joueur)
    def handle_computer_click(self, x, y):
        if not self.game_started or self.is_computer_turn:  # Vérifie si c'est le tour de l'IA
            return

        if self.computer_board.grid[x][y] == 1:
            self.computer_buttons[x][y].configure(bg='red')
            self.computer_board.grid[x][y] = 2
            self.game_status_label.configure(text="Le joueur a touché un navire!")

            # Vérification navire coulé
            hit_ship = None
            for ship in self.computer_board.ships:
                if (x, y) in ship.positions:
                    ship.hits.append((x, y))
                    hit_ship = ship
                    if ship.is_sunk():
                        for pos in ship.positions:
                            self.computer_buttons[pos[0]][pos[1]].configure(bg='dark red')
                        self.game_status_label.configure(text="Le joueur a coulé un navire!")

            self.print_ai_board()  # Déboggage
            # Si touché mais pas coulé, le joueur peut rejouer
            if hit_ship and not hit_ship.is_sunk():
                return  # On ne passe pas au tour de l'ordinateur
        # Si la case est déjà touchée on ne fait rien sauf dire que la case est déjà touchée et qu'il faut tirer ailleurs
        elif self.computer_board.grid[x][y] == 2 or self.computer_board.grid[x][y] == 3:
            self.game_status_label.configure(text="Vous avez déjà tiré ici!")
            self.print_ai_board() # Déboggage
            return
        else:
            self.computer_buttons[x][y].configure(bg='blue')
            self.computer_board.grid[x][y] = 3
            self.game_status_label.configure(text="Le joueur a manqué!")
            self.print_ai_board()  # Déboggage

        # Tour de l'ordinateur
        self.is_computer_turn = True  # Active le blocage
        self.computer_turn()

        # Vérification de fin de partie
        self.check_game_end()

    def get_adjacent_cells(self, x, y):
        """Retourne les cases adjacentes valides"""
        adjacent = []
        for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            new_x, new_y = x + dx, y + dy
            if 0 <= new_x < 10 and 0 <= new_y < 10 and self.player_board.grid[new_x][new_y] in [0, 1]:
                adjacent.append((new_x, new_y))
        return adjacent

    def change_difficulty(self):
        """Change le niveau de difficulté"""
        self.difficulty = self.difficulty_var.get()
        self.last_hit = None
        self.adjacent_cells = []

    def computer_turn(self):
        def do_turn():
            while True:
                if self.difficulty == "difficile":
                    x, y = self.get_next_target()
                else:
                    x = random.randint(0, 9)
                    y = random.randint(0, 9)

                if self.player_board.grid[x][y] in [0, 1]:
                    if self.player_board.grid[x][y] == 1:
                        self.player_buttons[x][y].configure(bg='red')
                        self.player_board.grid[x][y] = 2
                        self.game_status_label.configure(text="L'IA a touché un navire!")

                        # Si c'est la première touche d'un nouveau navire
                        if not self.first_hit:
                            self.first_hit = (x, y)
                            self.current_direction = self.choose_initial_direction(x, y)
                            self.last_hit = (x, y)
                        else:
                            self.last_hit = (x, y)

                        hit_ship = None
                        for ship in self.player_board.ships:
                            if (x, y) in ship.positions:
                                ship.hits.append((x, y))
                                hit_ship = ship
                                if ship.is_sunk():
                                    for pos in ship.positions:
                                        self.player_buttons[pos[0]][pos[1]].configure(bg='dark red')
                                    self.game_status_label.configure(text="L'IA a coulé un navire!")
                                    # Reset de la stratégie
                                    self.first_hit = None
                                    self.last_hit = None
                                    self.current_direction = None
                                    self.tried_directions = []
                                    self.current_axis = 'H'
                                    self.is_computer_turn = False
                                    return False

                        if hit_ship and not hit_ship.is_sunk():
                            self.root.after(300, computer_turn)
                            return True
                    else:
                        self.player_buttons[x][y].configure(bg='blue')
                        self.player_board.grid[x][y] = 3
                        self.game_status_label.configure(text="L'IA a manqué!")
                        # Changer de direction après un tir manqué
                        self.change_direction()
                        self.is_computer_turn = False
                    break

        def computer_turn():
            should_continue = do_turn()

            # Vérification de fin de partie
            if self.check_game_end():
                return

            # Si le joueur a coulé un navire ou touché sans couler l'ordinateur rejoue
            if should_continue:
                return

        computer_turn()

    def get_next_target(self):
        # Si on n'a pas de point de départ, chercher une case rouge non coulée
        if not self.first_hit:
            for i in range(10):
                for j in range(10):
                    if self.player_buttons[i][j].cget('bg') == 'red':
                        self.first_hit = (i, j)
                        self.last_hit = (i, j)
                        self.current_direction = self.choose_initial_direction(i, j)
                        self.tried_directions = []
                        break
                if self.first_hit:
                    break

        if not self.first_hit:
            return random.randint(0, 9), random.randint(0, 9)

        if not self.current_direction:
            self.current_direction = self.choose_initial_direction(*self.first_hit)

        x, y = self.last_hit
        if self.current_direction == 'N':
            dx, dy = 0, -1
        elif self.current_direction == 'S':
            dx, dy = 0, 1
        elif self.current_direction == 'E':
            dx, dy = 1, 0
        else:
            dx, dy = -1, 0  # 'W'

        new_x, new_y = x + dx, y + dy

        # Si la nouvelle position est invalide ou déjà touchée
        if not (0 <= new_x < 10 and 0 <= new_y < 10) or \
                self.player_board.grid[new_x][new_y] in [2, 3]:
            self.change_direction()
            return self.get_next_target()

        return new_x, new_y

    def change_direction(self):
        opposites = {'N': 'S', 'S': 'N', 'E': 'W', 'W': 'E'}

        # Vérifier que current_direction existe avant d'accéder à opposites
        if self.current_direction and opposites.get(self.current_direction) not in self.tried_directions:
            self.tried_directions.append(self.current_direction)
            self.current_direction = opposites[self.current_direction]
            self.last_hit = self.first_hit  # Repartir du premier tir
        else:
            # Si on a déjà essayé les deux directions sur cet axe
            if self.current_axis == 'H':
                self.current_axis = 'V'
                self.current_direction = 'N'
            else:
                self.current_axis = 'H'
                self.current_direction = 'E'
            self.tried_directions = []
            self.last_hit = self.first_hit

    def choose_initial_direction(self, x, y):
        possible = []
        if x > 0: possible.append('W')
        if x < 9: possible.append('E')
        if y > 0: possible.append('N')
        if y < 9: possible.append('S')
        return random.choice(possible)

    def check_game_end(self):
        result = False
        player_lost = all(ship.is_sunk() for ship in self.player_board.ships)
        computer_lost = all(ship.is_sunk() for ship in self.computer_board.ships)

        # si l'un des joueurs a perdu, on désactive les grilles
        if player_lost or computer_lost:
            result = True
            for i in range(10):
                for j in range(10):
                    self.player_buttons[i][j].configure(state='disabled')
                    self.computer_buttons[i][j].configure(state='disabled')

        if player_lost:
            messagebox.showinfo("Fin de partie", "L'ordinateur a gagné!")
            self.game_status_label.configure(text="L'ordinateur a gagné!")
            self.instruction_label.configure(text="Fin de partie")
            self.game_started = False
        elif computer_lost:
            messagebox.showinfo("Fin de partie", "Vous avez gagné!")
            self.game_status_label.configure(text="Vous avez gagné!")
            self.instruction_label.configure(text="Fin de partie")
            self.game_started = False

        return result

    def start_game(self):
        self.game_started = True
        self.instruction_label.configure(text="C'est parti! Cliquez sur la grille de droite pour tirer")
        self.orientation_btn.pack_forget()


    # fonctions de déboggage
    def print_ai_board(self):
        print("AI Board:")
        for row in self.computer_board.grid:
            print(row)

if __name__ == "__main__":
    root = tk.Tk()
    game = BattleshipGame(root)
    root.mainloop()