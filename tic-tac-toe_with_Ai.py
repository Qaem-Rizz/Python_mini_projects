import customtkinter as ctk
from tkinter import messagebox
import random
import math

# Window setup and theme
ctk.set_appearance_mode("Dark")  # for dark mode look
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("Tic Tac Toe - Simple & Clean")
app.geometry("380x480")
app.resizable(False, False)

# Defining some global variables for the game, which will be remembered throughout the game session:

# "Board" is a list of 9 items with all the boxes empty initially. Each box can be "X", "O", or "" (empty).
board = ["", "", "", "", "", "", "", "", ""]
human = "X"      # my symbol
ai = "O"         # Computer symbol

game_over = False
current_difficulty = "Hard"  # Default difficulty

buttons = []     # to store 9 buttons - a list
status_label = None


# function to check if any player has won the game:

def check_win(current_board, player):
    # Jeetne k 8 ways hote hai Tic-Tac-Toe me (3 row, 3 column, 2 diagonal):
    win_combos = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Rows (Horizontal)
        [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Columns (Vertical)
        [0, 4, 8], [2, 4, 6]              # Diagonals
    ]
    
    # to check if ksi bhi combo ke teeno boxes mein same player ka symbol hai:
    for combo in win_combos:
        pos1 = combo[0]
        pos2 = combo[1]
        pos3 = combo[2]
        if current_board[pos1] == player and current_board[pos2] == player and current_board[pos3] == player:
            return True
    return False


# To check if the board is full (tie situation):
def is_board_full(current_board):
    for spot in current_board:
        if spot == "":
            return False   #empty box available
    return True #all filled, tie ho gaya


# 5. Minimax Algorithm (for Hard Mode AI)
def minimax(current_board, depth, is_maximizing):
    # Base cases: Check karo agar game pehle hi jeet ya haar par khatam ho gaya ho
    if check_win(current_board, ai):
        return 10 - depth
    if check_win(current_board, human):
        return depth - 10
    if is_board_full(current_board):
        return 0

    # AI finds the biggest score on its turn (Maximizing)
    if is_maximizing:
        max_eval = -math.inf
        for i in range(9):
            if current_board[i] == "":
                current_board[i] = ai  # Temporary turn
                eval = minimax(current_board, depth + 1, False)
                current_board[i] = ""  # undo karo
                max_eval = max(max_eval, eval)
        return max_eval
    
    # Human ki turn par AI thinks human minimum score dega (Minimizing)
    else:
        min_eval = math.inf
        for i in range(9):
            if current_board[i] == "":
                current_board[i] = human  # Temporary turn
                eval = minimax(current_board, depth + 1, True)
                current_board[i] = ""  # undo karo
                min_eval = min(min_eval, eval)
        return min_eval


# to decide AI ki Move:
def ai_move():
    global game_over
    if game_over:
        return

    # Sabhi khali dabbo ki list:
    empty_indices = []
    for i in range(9):
        if board[i] == "":
            empty_indices.append(i)

    if not empty_indices:
        return

    best_move = None

    # choosing random box for Easy mode:
    if current_difficulty == "Easy":
        best_move = random.choice(empty_indices)
    
    # If Mode is Hard, then use Minimax algorithm to find the best move:
    else:
        best_score = -math.inf
        for i in empty_indices:
            board[i] = ai
            score = minimax(board, 0, False)
            board[i] = ""
            if score > best_score:
                best_score = score
                best_move = i

    # AI ki chosen move ko board par apply karo
    if best_move is not None:
        board[best_move] = ai
        buttons[best_move].configure(text=ai, text_color="#ff5555")

        # Check karo if AI wins:
        if check_win(board, ai):
            messagebox.showinfo("Game Over", "Computer Wins! Such a Loser you are")
            game_over = True
        elif is_board_full(board):
            messagebox.showinfo("Game Tied", "You can't even beat a machine now? Loser!")
            game_over = True
        else:
            status_label.configure(text="Player's Turn (X)")


# To check player's click on a button and make the move if valid:

def player_move(index):
    global game_over
    # Agar dabba khali hai aur game chal raha hai tabhi click kaam karega:
    if board[index] == "" and not game_over:
        board[index] = human
        buttons[index].configure(text=human, text_color="#3b82f6")

        # Check if player wins:
        if check_win(board, human):
            messagebox.showinfo("Game Over", "You Won!")
            game_over = True
            return
        elif is_board_full(board):
            messagebox.showinfo("Game Tied", "You can't even beat a machine now? Loser!")
            game_over = True
            return

        # AI's turn:
        status_label.configure(text="Computer is Thinking...")
        app.update()
        ai_move()


# function to reset the game again:
def reset_game():
    global board, game_over
    board = ["", "", "", "", "", "", "", "", ""]
    game_over = False
    status_label.configure(text=f"Player's Turn (X) [{current_difficulty}]")
    for btn in buttons:
        btn.configure(text="", text_color="white")


# if difficulty changes, then reset the game and update the status label:
def change_difficulty(choice):
    global current_difficulty
    current_difficulty = choice
    reset_game()


# --- UI (User Interface) Layout ---

# Difficulty Dropdown Menu
control_frame = ctk.CTkFrame(app, fg_color="transparent")
control_frame.pack(pady=10)

diff_label = ctk.CTkLabel(control_frame, text="Difficulty:", font=("Arial", 12, "bold"))
diff_label.pack(side="left", padx=5)

diff_menu = ctk.CTkOptionMenu(
    control_frame, values=["Easy", "Hard"], command=change_difficulty,
    font=("Arial", 12), width=100
)
diff_menu.set("Hard")
diff_menu.pack(side="left", padx=5)

# Status Label (Batata hai kiska turn hai)
status_label = ctk.CTkLabel(app, text="Player's Turn (X) [Hard]", font=("Arial", 14, "bold"))
status_label.pack(pady=5)

# 3x3 Grid Buttons:
grid_frame = ctk.CTkFrame(app, fg_color="transparent")
grid_frame.pack(pady=5)

for i in range(9):
    # Har button ke click par uska index (0 se 8) `player_move` ko jayega
    btn = ctk.CTkButton(
        grid_frame, text="", font=("Arial", 28, "bold"),
        width=90, height=90, fg_color="#2b2b2b", hover_color="#3a3a3a",
        command=lambda idx=i: player_move(idx)
    )
    row_num = i // 3
    col_num = i % 3
    btn.grid(row=row_num, column=col_num, padx=4, pady=4)
    buttons.append(btn)

# Restart Button
reset_btn = ctk.CTkButton(
    app, text="Restart Game", font=("Arial", 12, "bold"),
    command=reset_game, width=200, height=35
)
reset_btn.pack(pady=15)

# Start the main event loop
app.mainloop()