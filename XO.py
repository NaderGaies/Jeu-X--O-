import tkinter as tk
from tkinter import messagebox


class Player:
    def __init__(self, name, symbol):
        self.name = name
        self.symbol = symbol


class Board:
    def __init__(self):
        self.board = [["" for _ in range(3)] for _ in range(3)]

    def reset_board(self):
        self.board = [["" for _ in range(3)] for _ in range(3)]

    def update_board(self, row, col, symbol):
        if self.board[row][col] == "":
            self.board[row][col] = symbol
            return True
        return False

    def check_winner(self, symbol):
        
        for row in self.board:
            if all(cell == symbol for cell in row):
                return True

        for col in range(3):
            if all(self.board[row][col] == symbol for row in range(3)):
                return True

        if all(self.board[i][i] == symbol for i in range(3)) or all(self.board[i][2 - i] == symbol for i in range(3)):
            return True

        return False

    def is_draw(self):
        return all(cell != "" for row in self.board for cell in row)


class Game:
    def __init__(self, root):
        self.root = root
        self.root.title("Jeu {X - O}")
        self.board = Board()
        self.players = []
        self.current_player = None
        self.buttons = [[None for _ in range(3)] for _ in range(3)]
        self.main_menu()

    def main_menu(self):
        
        for widget in self.root.winfo_children():
            widget.destroy()

        
        tk.Label(self.root, text="Jeu {X - O}", font=("Arial", 24, "bold")).pack(pady=20)
        tk.Button(self.root, text="Nouvelle partie", font=("Arial", 16), width=20, command=self.setup_players).pack(pady=10)
        tk.Button(self.root, text="Quitter", font=("Arial", 16), width=20, command=self.root.quit).pack(pady=10)

    def setup_players(self):
        
        for widget in self.root.winfo_children():
            widget.destroy()

        tk.Label(self.root, text="Configuration des joueurs", font=("Arial", 20, "bold")).pack(pady=20)

        
        tk.Label(self.root, text="Nom du Joueur 1 (X):", font=("Arial", 14)).pack()
        self.player1_name = tk.Entry(self.root, font=("Arial", 14))
        self.player1_name.pack(pady=5)

        
        tk.Label(self.root, text="Nom du Joueur 2 (O):", font=("Arial", 14)).pack()
        self.player2_name = tk.Entry(self.root, font=("Arial", 14))
        self.player2_name.pack(pady=5)

        
        tk.Button(self.root, text="Commencer", font=("Arial", 16), command=self.start_game).pack(pady=20)

    def start_game(self):
       
        name1 = self.player1_name.get().strip() or "Joueur 1"
        name2 = self.player2_name.get().strip() or "Joueur 2"

        self.players = [
            Player(name1, "X"),
            Player(name2, "O")
        ]
        self.current_player = self.players[0]

        self.board.reset_board()
        self.create_game_interface()

    def create_game_interface(self):
        
        for widget in self.root.winfo_children():
            widget.destroy()

        
        tk.Label(self.root, text=f"Tour de {self.current_player.name} ({self.current_player.symbol})",
                 font=("Arial", 16), name="turn_label").pack(pady=10)

        frame = tk.Frame(self.root)
        frame.pack()

        for row in range(3):
            for col in range(3):
                btn = tk.Button(frame, text="", font=("Arial", 24), width=5, height=2,
                                command=lambda r=row, c=col: self.make_move(r, c))
                btn.grid(row=row, column=col)
                self.buttons[row][col] = btn

    def make_move(self, row, col):
        if self.board.update_board(row, col, self.current_player.symbol):
            self.buttons[row][col].config(text=self.current_player.symbol)

            if self.board.check_winner(self.current_player.symbol):
                messagebox.showinfo("Victoire", f"{self.current_player.name} a gagné!")
                self.main_menu()
                return

            if self.board.is_draw():
                messagebox.showinfo("Match nul", "Le jeu est terminé par un match nul! La partie recommence.")
                self.board.reset_board()
                self.reset_board_interface()
                return

           
            self.current_player = self.players[0] if self.current_player == self.players[1] else self.players[1]
            turn_label = self.root.nametowidget("turn_label")
            turn_label.config(text=f"Tour de {self.current_player.name} ({self.current_player.symbol})")
        else:
            messagebox.showwarning("Case occupée", "Cette case est déjà prise. Choisissez une autre.")

    def reset_board_interface(self):
        
        for row in range(3):
            for col in range(3):
                self.buttons[row][col].config(text="")

    def reset_game(self):
        self.start_game()


if __name__ == "__main__":
    root = tk.Tk()
    game = Game(root)
    root.mainloop()
