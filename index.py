import tkinter as tk
from tkinter import messagebox
import random

# Initialize the main application window
window = tk.Tk()
window.title("Tic-Tac-Toe")

# Styling the game window
window.configure(bg="#2b2b2b")

buttons = [[None for _ in range(3)] for _ in range(3)]
current_player = "X"
playing_with_ai = False

def check_winner():
    """Check for a winner or a tie in the game."""
    for i in range(3):
        # Check rows and columns
        if buttons[i][0]["text"] == buttons[i][1]["text"] == buttons[i][2]["text"] != "":
            return buttons[i][0]["text"]
        if buttons[0][i]["text"] == buttons[1][i]["text"] == buttons[2][i]["text"] != "":
            return buttons[0][i]["text"]

    # Check diagonals
    if buttons[0][0]["text"] == buttons[1][1]["text"] == buttons[2][2]["text"] != "":
        return buttons[0][0]["text"]
    if buttons[0][2]["text"] == buttons[1][1]["text"] == buttons[2][0]["text"] != "":
        return buttons[0][2]["text"]

    # Check for a tie
    for row in buttons:
        for button in row:
            if button["text"] == "":
                return None
    return "Tie"

def minimax(is_maximizing):
    """Minimax algorithm to choose the best move for the AI."""
    winner = check_winner()
    if winner == "X":
        return -1
    elif winner == "O":
        return 1
    elif winner == "Tie":
        return 0

    if is_maximizing:
        best_score = -float("inf")
        for i in range(3):
            for j in range(3):
                if buttons[i][j]["text"] == "":
                    buttons[i][j]["text"] = "O"
                    score = minimax(False)
                    buttons[i][j]["text"] = ""
                    best_score = max(score, best_score)
        return best_score
    else:
        best_score = float("inf")
        for i in range(3):
            for j in range(3):
                if buttons[i][j]["text"] == "":
                    buttons[i][j]["text"] = "X"
                    score = minimax(True)
                    buttons[i][j]["text"] = ""
                    best_score = min(score, best_score)
        return best_score

def ai_move():
    """Make a move for the AI using the Minimax algorithm."""
    best_score = -float("inf")
    best_move = None

    for i in range(3):
        for j in range(3):
            if buttons[i][j]["text"] == "":
                buttons[i][j]["text"] = "O"
                score = minimax(False)
                buttons[i][j]["text"] = ""
                if score > best_score:
                    best_score = score
                    best_move = (i, j)

    if best_move:
        i, j = best_move
        buttons[i][j]["text"] = "O"
        buttons[i][j]["state"] = "disabled"
        check_game_over()

def check_game_over():
    """Check if the game is over and display the result."""
    winner = check_winner()
    if winner:
        if winner == "Tie":
            messagebox.showinfo("Game Over", "It's a Tie!")
        else:
            messagebox.showinfo("Game Over", f"Player {winner} wins!")
        return_to_menu()  # Return to the main menu after the game ends

def button_click(i, j):
    """Handle button click events."""
    global current_player
    if buttons[i][j]["text"] == "":
        buttons[i][j]["text"] = current_player
        buttons[i][j]["state"] = "disabled"
        check_game_over()

        if playing_with_ai and current_player == "X":
            current_player = "O"
            ai_move()
            current_player = "X"
        else:
            current_player = "O" if current_player == "X" else "X"

def reset_board():
    """Reset the game board."""
    global current_player
    current_player = "X"
    for i in range(3):
        for j in range(3):
            buttons[i][j]["text"] = ""
            buttons[i][j]["state"] = "normal"

def play_with_ai():
    """Choose to play against AI and start the game."""
    global playing_with_ai
    playing_with_ai = True
    start_game()

def play_with_player():
    """Choose to play against another player and start the game."""
    global playing_with_ai
    playing_with_ai = False
    start_game()

def start_game():
    """Start the game by setting up the game board."""
    # Hide the main menu buttons
    menu_frame.pack_forget()

    # Show the game board
    game_frame.pack(pady=20)

    # Reset the game board for a new game
    reset_board()

def return_to_menu():
    """Return to the main menu after a game ends."""
    # Hide the game board
    game_frame.pack_forget()

    # Show the main menu buttons
    menu_frame.pack(pady=100)

# Create the main menu interface
menu_frame = tk.Frame(window, bg="#2b2b2b")
menu_frame.pack(pady=100)

menu_label = tk.Label(menu_frame, text="Choose Game Mode", font=("Arial", 18), bg="#2b2b2b", fg="#fafafa")
menu_label.pack(pady=20)

ai_button = tk.Button(menu_frame, text="Play with AI", font=("Arial", 14), command=play_with_ai, bg="#4caf50", fg="#fafafa")
ai_button.pack(side="left", padx=20)

player_button = tk.Button(menu_frame, text="Play with Player", font=("Arial", 14), command=play_with_player, bg="#2196f3", fg="#fafafa")
player_button.pack(side="right", padx=20)

# Create the game board
game_frame = tk.Frame(window, bg="#2b2b2b")

for i in range(3):
    for j in range(3):
        buttons[i][j] = tk.Button(game_frame, text="", font=("Arial", 24), width=5, height=2, bg="#fafafa", fg="#2b2b2b",
                                  command=lambda i=i, j=j: button_click(i, j))
        buttons[i][j].grid(row=i, column=j, padx=5, pady=5)

# Start the application
window.mainloop()
