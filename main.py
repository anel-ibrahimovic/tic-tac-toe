import tkinter as tk
from tkinter import messagebox
import math

class TicTacToe:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic Tac Toe with Minimax AI")

        self.board = [['' for _ in range(3)] for _ in range(3)]
        self.buttons = [[None for _ in range(3)] for _ in range(3)]

        self.create_widgets()
        self.player_turn = True

    def create_widgets(self):
        frame = tk.Frame(self.root)
        frame.pack()

        for i in range(3):
            for j in range(3):
                btn = tk.Button(frame, text=' ', font=('Arial', 40), width=3, height=1,
                                command=lambda r=i, c=j: self.player_move(r, c))
                btn.grid(row=i, column=j)
                self.buttons[i][j] = btn

        self.restart_btn = tk.Button(self.root, text="Restart Game", command=self.restart_game)
        self.restart_btn.pack(pady=10)

    def player_move(self, row, col):
        if self.player_turn and self.board[row][col] == '':
            self.board[row][col] = 'X'
            self.update_button(row, col, 'X')

            if self.win(self.board, 'X'):
                self.game_over("You won!")
                return
            elif self.full_board(self.board):
                self.game_over("It's a draw!")
                return

            self.player_turn = False
            self.root.after(300, self.computer_move)  # AI move with slight delay

    def computer_move(self):
        best_score = -math.inf
        move = (-1, -1)

        for i in range(3):
            for j in range(3):
                if self.board[i][j] == '':
                    self.board[i][j] = 'O'
                    score = self.minimax(self.board, 0, False)
                    self.board[i][j] = ''
                    if score > best_score:
                        best_score = score
                        move = (i, j)

        if move != (-1, -1):
            self.board[move[0]][move[1]] = 'O'
            self.update_button(move[0], move[1], 'O')

        if self.win(self.board, 'O'):
            self.game_over("Computer won!")
        elif self.full_board(self.board):
            self.game_over("It's a draw!")
        else:
            self.player_turn = True

    def update_button(self, row, col, player):
        self.buttons[row][col]['text'] = player
        self.buttons[row][col]['state'] = 'disabled'

    def win(self, board, player):
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

    def full_board(self, board):
        return all(cell != '' for row in board for cell in row)

    def minimax(self, board, depth, is_maximizing):
        if self.win(board, 'O'):
            return 10 - depth
        if self.win(board, 'X'):
            return depth - 10
        if self.full_board(board):
            return 0

        if is_maximizing:
            best_score = -math.inf
            for i in range(3):
                for j in range(3):
                    if board[i][j] == '':
                        board[i][j] = 'O'
                        score = self.minimax(board, depth + 1, False)
                        board[i][j] = ''
                        best_score = max(score, best_score)
            return best_score
        else:
            best_score = math.inf
            for i in range(3):
                for j in range(3):
                    if board[i][j] == '':
                        board[i][j] = 'X'
                        score = self.minimax(board, depth + 1, True)
                        board[i][j] = ''
                        best_score = min(score, best_score)
            return best_score

    def game_over(self, message):
        messagebox.showinfo("Game Over", message)
        self.disable_all_buttons()

    def disable_all_buttons(self):
        for i in range(3):
            for j in range(3):
                self.buttons[i][j]['state'] = 'disabled'

    def restart_game(self):
        self.board = [['' for _ in range(3)] for _ in range(3)]
        self.player_turn = True
        for i in range(3):
            for j in range(3):
                self.buttons[i][j]['text'] = ' '
                self.buttons[i][j]['state'] = 'normal'

if __name__ == '__main__':
    root = tk.Tk()
    game = TicTacToe(root)
    root.mainloop()
