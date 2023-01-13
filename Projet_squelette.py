import math
import tkinter as tk
from tkinter import ttk
import numpy as np
import random as rnd
from threading import Thread
from queue import Queue
import math




disk_color = ['white', 'red', 'orange']
disks = list()

player_type = ['human']
for i in range(42):
    player_type.append('AI: alpha-beta level '+str(i+1))

def alpha_beta_decision(board, turn, ai_level, queue, max_player):
    moves = board.get_possible_moves()
    best_move = moves[2]
    best_value = -999999999
    alpha = -999999999
    beta = 999999999
    for m in moves:
        copy_board = board.copy()
        copy_board.add_disk(m, max_player, False)
        alphaBeta = alpha_beta_algo(copy_board, ai_level, turn, alpha, beta, game.current_player())
        if alphaBeta > best_value:
            best_value = alphaBeta
            best_move = m
        alpha = max(alpha, best_value)
    queue.put(best_move)

def maximizeAlpha(board, turn, alpha, beta, max_player):
    moves = board.get_possible_moves()
    alphaBeta = -999999999
    for m in moves:
        copyBoard = board.copy()
        copyBoard.add_disk(m, max_player, False)
        alphaBeta = max(alphaBeta, minimizeBeta(copyBoard, turn + 1, alpha, beta, 2 - ((max_player + 1) % 2)))
        if alphaBeta >= beta:
            return 
        alpha = max(alpha, alphaBeta)
    return alphaBeta

def minimizeBeta(board, turn, alpha, beta, max_player):
    moves = board.get_possible_moves()
    alphaBeta = 999999999
    for m in moves:
        copyBoard = board.copy()
        copyBoard.add_disk(m, max_player, False)
        alphaBeta = max(alphaBeta, maximizeAlpha(copyBoard, turn + 1, alpha, beta, 2 - ((max_player + 1) % 2)))
        if alphaBeta >= alpha:
            return alphaBeta
        beta = max(beta, alphaBeta)
    return alphaBeta

def alpha_beta_algo(board, depth, turn, alpha, beta, max_player):
    if depth == 0 or board.check_victory():
        return board.eval(max_player)

    if max_player == 1:
        best_score = -999999999
        moves = board.get_possible_moves()
        for move in moves :
            algo_board = board.copy()
            algo_board.add_disk(move, max_player,False)
            best_score = max(alpha_beta_algo(algo_board, depth - 1, turn, alpha, beta, game.current_player()), best_score)
            alpha = max(alpha, best_score)
            if beta <= alpha:
                break
        return best_score
    else:
        best_score = 999999999
        moves = board.get_possible_moves()
        for move in moves:
            algo_board = board.copy()
            algo_board.add_disk(move, max_player, False)
            best_score = min(alpha_beta_algo(algo_board, depth - 1, turn, alpha, beta, game.current_player()), best_score)
            beta = min(beta, best_score)
            if beta <= alpha:
                break
        return best_score

#To verify how many pieces we can make in one sequence to get 4 pieces
def evaluate_window(window, turn):
    score = 0
    # definig when the ia is playing
    piece = (turn % 2) + 2 #ia
    opp = (turn % 2) + 1
    #getting the score based on the player and number of empty spots
    if window.count(piece) == 3 and window.count(0) == 1:
        score += 50
    if window.count(piece) == 2 and window.count(0) == 2:
        score += 15
    if window.count(piece) == 1 and window.count(0) == 3:
        score += 5

    if window.count(opp) == 3 and window.count(0) == 1:
        score -= 50
    if window.count(opp) == 2 and window.count(0) == 2:
        score -= 20
    if window.count(opp) == 1 and window.count(0) == 3:
        score -= 10
    return score

class Board:
    grid = np.array([[0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0]])
#To give a score to a grid based on directions
    def eval(self, player):
        BOARD_WIDTH  = 6 #cols
        BOARD_HEIGHT = 5 #rows
        LENGTH = 4
        score = 0

        ## Score vertical
        for c in range (BOARD_WIDTH):
            col_array = [int(i) for i in list(self.grid[:,c])]
            for r in range (BOARD_HEIGHT-3):
                window = col_array[r:r+LENGTH]
                score += evaluate_window(window,player)

        ## Score Horizental
        for c in range (BOARD_HEIGHT):
            col_array = [int(i) for i in list(self.grid[:,c])]
            for r in range (BOARD_WIDTH-3):
                window = col_array[r:r+LENGTH]
                score += evaluate_window(window,player)

        ## Score Positive Diagonal
        for r in range(BOARD_HEIGHT-3):
            for c in range(BOARD_WIDTH-3):
                window = [self.grid[r+i][c+i] for i in range(LENGTH)]
                score += evaluate_window(window, player)

        ## Score Negative Diagonal
        for r in range(BOARD_HEIGHT-3):
            for c in range(BOARD_WIDTH-3):
                window = [self.grid[r-i][c-i] for i in range(LENGTH)]
                score += evaluate_window(window, player)

        ## Score center column
        center_array = [int(i) for i in list(self.grid[:, BOARD_WIDTH//2])]
        center_count = center_array.count(player)
        score += center_count * 99
        return score

    def copy(self):
        new_board = Board()
        new_board.grid = np.array(self.grid, copy=True)
        return new_board

    def reinit(self):
        self.grid.fill(0)
        for i in range(7):
            for j in range(6):
                canvas1.itemconfig(disks[i][j], fill=disk_color[0])

    def get_possible_moves(self):
        possible_moves = list()
        if self.grid[3][5] == 0:
            possible_moves.append(3)
        for shift_from_center in range(1, 4):
            if self.grid[3 + shift_from_center][5] == 0:
                possible_moves.append(3 + shift_from_center)
            if self.grid[3 - shift_from_center][5] == 0:
                possible_moves.append(3 - shift_from_center)
        return possible_moves

    def add_disk(self, column, player, update_display=True):
        for j in range(6):
            if self.grid[column][j] == 0:
                break
        self.grid[column][j] = player
        if update_display:
            canvas1.itemconfig(disks[column][j], fill=disk_color[player])

    def column_filled(self, column):
        return self.grid[column][5] != 0

    def check_victory(self):
        # Horizontal alignment check
        for line in range(6):
            for horizontal_shift in range(4):
                if self.grid[horizontal_shift][line] == self.grid[horizontal_shift + 1][line] == self.grid[horizontal_shift + 2][line] == self.grid[horizontal_shift + 3][line] != 0:
                    return True
        # Vertical alignment check
        for column in range(7):
            for vertical_shift in range(3):
                if self.grid[column][vertical_shift] == self.grid[column][vertical_shift + 1] == \
                        self.grid[column][vertical_shift + 2] == self.grid[column][vertical_shift + 3] != 0:
                    return True
        # Diagonal alignment check
        for horizontal_shift in range(4):
            for vertical_shift in range(3):
                if self.grid[horizontal_shift][vertical_shift] == self.grid[horizontal_shift + 1][vertical_shift + 1] ==\
                        self.grid[horizontal_shift + 2][vertical_shift + 2] == self.grid[horizontal_shift + 3][vertical_shift + 3] != 0:
                    return True
                elif self.grid[horizontal_shift][5 - vertical_shift] == self.grid[horizontal_shift + 1][4 - vertical_shift] ==\
                        self.grid[horizontal_shift + 2][3 - vertical_shift] == self.grid[horizontal_shift + 3][2 - vertical_shift] != 0:
                    return True
        return False


class Connect4:

    def __init__(self):
        self.board = Board()
        self.human_turn = False
        self.turn = 1
        self.players = (0, 0)
        self.ai_move = Queue()

    def current_player(self):
        return 2 - (self.turn % 2)

    def launch(self):
        self.board.reinit()
        self.turn = 0
        information['fg'] = 'black'
        information['text'] = "Turn " + str(self.turn) + " - Player " + str(
            self.current_player()) + " is playing"
        self.human_turn = False
        self.players = (combobox_player1.current(), combobox_player2.current())
        self.handle_turn()

    def move(self, column):
        if not self.board.column_filled(column):
            self.board.add_disk(column, self.current_player())
            self.handle_turn()

    def click(self, event):
        if self.human_turn:
            column = event.x // row_width
            self.move(column)

    def ai_turn(self, ai_level):
        Thread(target=alpha_beta_decision, args=(self.board, self.turn, ai_level, self.ai_move, self.current_player(),)).start()
        self.ai_wait_for_move()

    def ai_wait_for_move(self):
        if not self.ai_move.empty():
            self.move(self.ai_move.get())
        else:
            window.after(100, self.ai_wait_for_move)

    def handle_turn(self):
        self.human_turn = False
        if self.board.check_victory():
            information['fg'] = 'red'
            information['text'] = "Player " + str(self.current_player()) + " wins !"
            return
        elif self.turn >= 42:
            information['fg'] = 'red'
            information['text'] = "This a draw !"
            return
        self.turn = self.turn + 1
        information['text'] = "Turn " + str(self.turn) + " - Player " + str(
            self.current_player()) + " is playing"
        if self.players[self.current_player() - 1] != 0:
            self.human_turn = False
            self.ai_turn(self.players[self.current_player() - 1])
        else:
            self.human_turn = True


game = Connect4()

# Graphical settings
width = 700
row_width = width // 7
row_height = row_width
height = row_width * 6
row_margin = row_height // 10

window = tk.Tk()
window.title("Connect 4")
canvas1 = tk.Canvas(window, bg="blue", width=width, height=height)

# Drawing the grid
for i in range(7):
    disks.append(list())
    for j in range(5, -1, -1):
        disks[i].append(canvas1.create_oval(row_margin + i * row_width, row_margin + j * row_height, (i + 1) * row_width - row_margin,
                            (j + 1) * row_height - row_margin, fill='white'))


canvas1.grid(row=0, column=0, columnspan=2)

information = tk.Label(window, text="")
information.grid(row=1, column=0, columnspan=2)

label_player1 = tk.Label(window, text="Player 1: ")
label_player1.grid(row=2, column=0)
combobox_player1 = ttk.Combobox(window, state='readonly')
combobox_player1.grid(row=2, column=1)

label_player2 = tk.Label(window, text="Player 2: ")
label_player2.grid(row=3, column=0)
combobox_player2 = ttk.Combobox(window, state='readonly')
combobox_player2.grid(row=3, column=1)

combobox_player1['values'] = player_type
combobox_player1.current(0)
combobox_player2['values'] = player_type
combobox_player2.current(6)

button2 = tk.Button(window, text='New game', command=game.launch)
button2.grid(row=4, column=0)

button = tk.Button(window, text='Quit', command=window.destroy)
button.grid(row=4, column=1)

# Mouse handling
canvas1.bind('<Button-1>', game.click)

window.mainloop()
