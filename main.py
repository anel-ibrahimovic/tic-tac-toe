import math

def print_reference_board():
    print("Board positions:")
    positions = [[str(i + j * 3 + 1) for i in range(3)] for j in range(3)]
    for i, row in enumerate(positions):
        print('|'.join(row))
        if i < 2:
            print('-----')
    print()

def print_board(board):
    for i, row in enumerate(board):
        print('|'.join(cell if cell else ' ' for cell in row))
        if i < 2:
            print('-----')

def player_move(board):
    while True:
        try:
            move = int(input("Enter your move (1-9): "))
            if move not in range(1, 10):
                print("Invalid move. Please try again.")
                continue

            row = (move - 1) // 3
            col = (move - 1) % 3

            if board[row][col] == '':
                board[row][col] = 'X'
                break
            else:
                print("Cell already taken. Try again.")
        except ValueError:
            print("Invalid input. Please enter a number.")

def win(board, player):
    for i in range(3):
        if all(board[i][j] == player for j in range(3)):
            return True
        if all(board[j][i] == player for j in range(3)):
            return True
    if all(board[i][i] == player for i in range(3)):
        return True
    if all(board[i][2 - i] == player for i in range(3)):
        return True
    return False

def full_board(board):
    return all(cell != '' for row in board for cell in row)

def minimax(board, depth, is_maximizing):
    if win(board, 'O'):
        return 10 - depth
    if win(board, 'X'):
        return depth - 10
    if full_board(board):
        return 0

    if is_maximizing:
        best_score = -math.inf
        for i in range(3):
            for j in range(3):
                if board[i][j] == '':
                    board[i][j] = 'O'
                    score = minimax(board, depth + 1, False)
                    board[i][j] = ''
                    best_score = max(score, best_score)
        return best_score
    else:
        best_score = math.inf
        for i in range(3):
            for j in range(3):
                if board[i][j] == '':
                    board[i][j] = 'X'
                    score = minimax(board, depth + 1, True)
                    board[i][j] = ''
                    best_score = min(score, best_score)
        return best_score

def computer_move(board):
    best_score = -math.inf
    move = (-1, -1)

    for i in range(3):
        for j in range(3):
            if board[i][j] == '':
                board[i][j] = 'O'
                score = minimax(board, 0, False)
                board[i][j] = ''
                if score > best_score:
                    best_score = score
                    move = (i, j)

    board[move[0]][move[1]] = 'O'

def main():
    print_reference_board()

    while True:
        board = [['', '', ''], ['', '', ''], ['', '', '']]

        while True:
            # Player move
            player_move(board)
            if win(board, 'X'):
                print_board(board)
                print("X won!")
                break
            if full_board(board):
                print_board(board)
                print("It's a draw!")
                break

            # Computer move
            computer_move(board)
            print_board(board)  # print after both moves, except when player just won or draw
            if win(board, 'O'):
                print("O won!")
                break
            if full_board(board):
                print("It's a draw!")
                break

        again = input("Play again? (y/n): ").strip().lower()
        if again != 'y':
            print("Thanks for playing!")
            break

if __name__ == '__main__':
    main()
