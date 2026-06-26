def print_board(board):
    for i in range(0, 9, 3):
        row = " | ".join(board[i + j] for j in range(3))
        print(row)
        if i < 6:
            print("-" * 9)

def check_winner(board, player):
    wins = [
        (0, 1, 2), (3, 4, 5), (6, 7, 8),  # rows
        (0, 3, 6), (1, 4, 7), (2, 5, 8),  # columns
        (0, 4, 8), (2, 4, 6),             # diagonals
    ]
    return any(all(board[i] == player for i in line) for line in wins)

def get_move(board, player):
    while True:
        try:
            move = int(input(f"Player {player}, enter position (1-9): ")) - 1
            if move < 0 or move > 8:
                print("Pick a number from 1 to 9.")
                continue
            if board[move] != " ":
                print("That spot is taken.")
                continue
            return move
        except ValueError:
            print("Enter a valid number.")

def play():
    board = [" "] * 9
    current = "X"

    while True:
        print_board(board)
        move = get_move(board, current)
        board[move] = current

        if check_winner(board, current):
            print_board(board)
            print(f"Player {current} wins!")
            break

        if " " not in board:
            print_board(board)
            print("It's a draw!")
            break

        current = "O" if current == "X" else "X"

if __name__ == "__main__":
    play()