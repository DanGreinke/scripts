"""
Tic Tac Toe Player
"""

import math
import copy

# Initialize Global variables
X = "X"
O = "O"
EMPTY = None

def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    if board == initial_state():
        return X
    
    total_x = 0
    total_o = 0
    for row in board:
        for col in row:
            if col == X:
                total_x += 1
            elif col == O:
                total_o += 1

    if (total_x + total_o) % 2 == 1:
        return O
    else:
        return X


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    possible_actions = set()
    for row in range(3):
        for col in range(3):
            if board[row][col] == EMPTY:
                possible_actions.add((row,col))
    return possible_actions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    i,j = action
    if action not in actions(board):
        raise Exception("Invalid action")
    
    newBoard = copy.deepcopy(board)
    newBoard[i][j] = player(board)
    return newBoard

def transpose(board):
    return [[board[i][j] for i in range(3)] for j in range(3)]

def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    for i in range(3):
        # check if all on horizontal are the same
        if len(set(board[i])) == 1 and EMPTY not in board[i]:
            return board[i][0]
        # check if all on vertical are the same
        elif len(set(transpose(board)[i])) == 1 and EMPTY not in transpose(board)[i]:
            return board[i][0]
    down_diagonal = [board[i][i] for i in range(3)]
    up_diagonal = [board[i][2-i] for i in range(3)]
    if len(set(down_diagonal)) == 1 and EMPTY not in down_diagonal:
        return down_diagonal[0]
    elif len(set(up_diagonal)) == 1 and EMPTY not in up_diagonal:
        return up_diagonal[0]


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board) != None:
        return True
    else:
        for i in board:
            for j in i:
                if j == EMPTY:
                    return False
        return True



def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    result_map = {"X": 1,"O": -1,None: 0}
    return result_map[winner(board)]


def max_value(board):
    v = -math.inf
    if terminal(board):
        return utility(board)
    for action in actions(board):
        v = max(v, min_value(result(board,action)))
    return v

def min_value(board):
    v = math.inf
    if terminal(board):
        return utility(board)
    for action in actions(board):
        v = min(v, max_value(result(board,action)))
    return v

def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    action_dict = dict()
    if player(board) == X:
        for action in actions(board):
            action_dict[max_value(result(board,action))] = action
        return action_dict[max(action_dict)]
    elif player(board) == O:
        for action in actions(board):
            action_dict[min_value(result(board,action))] = action
        return action_dict[min(action_dict)]
