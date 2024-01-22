import tkinter as tk
from tkinter import messagebox
import random
import os

class TicTacToe:
    def __init__(self, master):
        self.master = master
        self.master.title("Tic Tac Toe")

        # Initialiser le système de gestion de compte utilisateur
        self.user_data = {}
        self.load_user_data()

        # Créer une liste pour représenter le plateau de jeu (3x3)
        self.board = [0] * 9

        # Variable pour suivre le tour du joueur
        self.current_player = 'X'

        # Niveaux d'IA disponibles
        self.ai_levels = {'Facile': self.easy_ai, 'Difficile': self.hard_ai,}

        # Variable pour stocker le niveau d'IA sélectionné
        self.selected_ai_level = tk.StringVar()
        self.selected_ai_level.set('Facile')  # Par défaut, l'IA est définie sur Facile

        # Créer le menu déroulant pour choisir la difficulté de l'IA
        self.ai_menu = tk.OptionMenu(master, self.selected_ai_level, *self.ai_levels.keys())
        self.ai_menu.grid(row=3, column=0, columnspan=3)

        # Créer les boutons du jeu
        self.buttons = [tk.Button(master, text=' ', font=('Helvetica', 24), width=5, height=2, command=lambda i=i: self.on_click(i)) for i in range(9)]

        # Placer les boutons sur la grille
        for row in range(3):
            for col in range(3):
                self.buttons[row * 3 + col].grid(row=row, column=col)

    def load_user_data(self):
        # Charger les données utilisateur depuis un fichier
        if os.path.exists("user_data.txt"):
            with open("user_data.txt", "r") as file:
                lines = file.readlines()
                for line in lines:
                    username, score = line.strip().split(',')
                    self.user_data[username] = int(score)

    def save_user_data(self):
        # Sauvegarder les données utilisateur dans un fichier
        with open("user_data.txt", "w") as file:
            for username, score in self.user_data.items():
                file.write(f"{username},{score}\n")

    def on_click(self, index):
        # Vérifier si la case est vide
        if self.board[index] == 0:
            # Mettre le symbole du joueur actuel dans la case
            self.board[index] = 'X'
            self.buttons[index].config(text='X')

            # Vérifier s'il y a un gagnant
            if self.check_winner():
                messagebox.showinfo("Fin du jeu", "Le joueur X gagne!")
                self.update_user_score('X')
                self.reset_game()
            else:
                # Vérifier s'il y a match nul
                if self.check_draw():
                    messagebox.showinfo("Fin du jeu", "Match nul!")
                    self.reset_game()
                else:
                    # Changer le joueur
                    self.current_player = 'O'

                    # Appeler l'IA pour jouer automatiquement
                    self.play_ai()

    def play_ai(self):
        # Vérifier si c'est le tour de l'IA
        if self.current_player == 'O':
            # Choisir l'IA en fonction du niveau sélectionné
            selected_ai = self.ai_levels[self.selected_ai_level.get()]
            choix_ia = selected_ai()

            if choix_ia is not None:
                # Mettre le symbole de l'IA sur le plateau et mettre à jour l'interface
                self.board[choix_ia] = 'O'
                self.buttons[choix_ia].config(text='O')

                # Vérifier s'il y a un gagnant ou un match nul après le coup de l'IA
                if self.check_winner():
                    messagebox.showinfo("Fin du jeu", "L'IA (O) gagne!")
                    self.update_user_score('O')
                    self.reset_game()
                elif self.check_draw():
                    messagebox.showinfo("Fin du jeu", "Match nul!")
                    self.reset_game()
                else:
                    # Changer le joueur
                    self.current_player = 'X'

    def easy_ai(self):
        # IA facile : choix aléatoire parmi les cases vides
        empty_cells = [i for i in range(9) if self.board[i] == 0]
        return random.choice(empty_cells) if empty_cells else None

    def hard_ai(self):
        # IA difficile : utiliser l'algorithme Minimax
        def minimax(b, depth, is_maximizing):
            scores = {'X': -1, 'O': 1, 'draw': 0}

            if self.check_winner(b, 'O'):
                return scores['O']
            elif self.check_winner(b, 'X'):
                return scores['X']
            elif self.check_draw(b):
                return scores['draw']

            if is_maximizing:
                max_eval = float('-inf')
                for i in range(9):
                    if b[i] == 0:
                        b[i] = 'O'
                        eval = minimax(b, depth + 1, False)
                        b[i] = 0
                        max_eval = max(max_eval, eval)
                return max_eval
            else:
                min_eval = float('inf')
                for i in range(9):
                    if b[i] == 0:
                        b[i] = 'X'
                        eval = minimax(b, depth + 1, True)
                        b[i] = 0
                        min_eval = min(min_eval, eval)
                return min_eval

        # Choisir le meilleur coup en utilisant l'algorithme Minimax
        best_score = float('-inf') if self.selected_ai_level.get() == 'Difficile' else float('inf')
        best_move = None
        for i in range(9):
            if self.board[i] == 0:
                self.board[i] = 'O'
                score = minimax(self.board, 0, False)
                self.board[i] = 0
                if (self.selected_ai_level.get() == 'Difficile' and score > best_score) or \
                        (self.selected_ai_level.get() == 'Facile' and score < best_score):
                    best_score = score
                    best_move = i

        return best_move

    def check_winner(self, b=None, player=None):
        if b is None:
            b = self.board
        if player is None:
            player = self.current_player

        # Vérifier les lignes, colonnes et diagonales pour un alignement de trois
        for i in range(3):
            if b[i * 3] == b[i * 3 + 1] == b[i * 3 + 2] == player or \
               b[i] == b[i + 3] == b[i + 6] == player:
                return True
        if b[0] == b[4] == b[8] == player or \
           b[2] == b[4] == b[6] == player:
            return True

        return False

    def check_draw(self, b=None):
        if b is None:
            b = self.board

        # Vérifier s'il y a match nul (le plateau est rempli)
        return all(cell != 0 for cell in b)

    def reset_game(self):
        # Réinitialiser le plateau de jeu et les boutons
        self.board = [0] * 9
        for button in self.buttons:
            button.config(text=' ')

    def update_user_score(self, winner):
        # Mettre à jour le score de l'utilisateur
        if winner in self.user_data:
            self.user_data[winner] += 1
        else:
            self.user_data[winner] = 1

        # Sauvegarder les données utilisateur
        self.save_user_data()


if __name__ == "__main__":
    root = tk.Tk()
    game = TicTacToe(root)
    root.mainloop()
