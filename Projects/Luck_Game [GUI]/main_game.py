import tkinter as tk
from random import *
from tkinter import messagebox

root = tk.Tk()
root.title("Player Names")


def show_stats():
    # Player One
    player1 = entry_player1.get()
    strength1 = randint(1, 9)
    agility1 = randint(1, 9)
    stamina1 = randint(1, 9)
    player1stats = {'Name': player1, 'Role': 'Marksman', 'Strength': strength1, 'Agility': agility1,
                    'Stamina': stamina1}
    for key, value in player1stats.items():
        print(f"{key}: {value}")

    # Player Two
    player2 = entry_player2.get()
    strength2 = randint(1, 9)
    agility2 = randint(1, 9)
    stamina2 = randint(1, 9)
    player2stats = {'Name': player2, 'Role': 'Marksman', 'Strength': strength2, 'Agility': agility2,
                    'Stamina': stamina2}
    for key, value in player2stats.items():
        print(f"{key}: {value}")


# Create menu bar
menubar = tk.Menu(root)
root.config(menu=menubar)

# Create File menu
file_menu = tk.Menu(menubar, tearoff=False)
menubar.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label="Exit", command=root.quit)

# Create Player menu
player_menu = tk.Menu(menubar, tearoff=False)
menubar.add_cascade(label="Players", menu=player_menu)

# Player Name input
player_frame = tk.Frame(root)
player_frame.pack(pady=20)

label_player1 = tk.Label(player_frame, text="Player 1:")
label_player1.grid(row=0, column=0, padx=10)
entry_player1 = tk.Entry(player_frame)
entry_player1.grid(row=0, column=1)

label_player2 = tk.Label(player_frame, text="Player 2:")
label_player2.grid(row=1, column=0, padx=10)
entry_player2 = tk.Entry(player_frame)
entry_player2.grid(row=1, column=1)

# Start button
start_button = tk.Button(root, text="Start Game", command=show_stats)
start_button.pack(pady=10)

root.mainloop()
