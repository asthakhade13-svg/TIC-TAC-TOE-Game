import numpy as np

board = np.zeros((3, 3), dtype=int)

def print_board(b):
    symbols = {0: " ", 1: "X", -1: "O"}
    for r in range(3):
        row = " | ".join([symbols[val] for val in b[r]])
        print(" " + row)
        if r < 2:
            print("---+---+---")


def check_winner(b):
    # Check rows and columns
    if 3 in np.sum(b, axis=1) or 3 in np.sum(b, axis=0):
        return 'X'
    if -3 in np.sum(b, axis=1) or -3 in np.sum(b, axis=0):
        return 'O'

    # Check diagonals
    if np.trace(b) == 3 or np.trace(np.fliplr(b)) == 3:
        return 'X'
    if np.trace(b) == -3 or np.trace(np.fliplr(b)) == -3:
        return 'O'

    # Check draw
    if 0 not in b:
        return 'Draw'
    return None


def main():
    current = 1
    print("Welcome to Tic Tac Toe!")
    print_board(board)

    while True:
        player = 'X' if current == 1 else 'O'

        try:
            row = int(input(f"{player}, enter row (0, 1, 2): "))
            col = int(input(f"{player}, enter column (0, 1, 2): "))
        except ValueError:
            print("Please enter numbers only!\n")
            continue

        if row < 0 or row > 2 or col < 0 or col > 2:
            print("Please enter row and column between 0 and 2.\n")
            continue

        if board[row][col] != 0:
            print("This cell is already occupied, please choose another one.\n")
            continue

        board[row][col] = current
        print_board(board)

        result = check_winner(board)
        if result is not None:
            if result == 'Draw':
                print("It's a draw!")
            else:
                print(f"Player {result} wins!")
            break

        current = -current


if __name__ == "__main__":
    main()
