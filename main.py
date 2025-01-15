import tkinter as tk

from src.game import BattleshipGame

if __name__ == "__main__":
    root = tk.Tk()
    game = BattleshipGame(root)
    root.mainloop()