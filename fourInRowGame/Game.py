import copy
from termcolor import colored
import alphaBetaPruning
import random
import numpy as np

VICTORY = 10 ** 20  # The value of a winning board (for max)
LOSS = -VICTORY  # The value of a losing board (for max)
PROMISE_VICTORY = 10 ** 10
PROMISE_LOSS = -PROMISE_VICTORY

TIE = 0  # The value of a tie
SIZE = 4  # the length of winning seq.
COMPUTER = SIZE + 1  # Marks the computer's cells on the board
HUMAN = 1  # Marks the human's cells on the board

rows = 6
columns = 7
full_seq_val = (rows * (SIZE - 1)) + 1  # val for the heuristic function


# that class wll generate the game
class Game:
    board = []
    size = rows * columns
    playTurn = HUMAN

    # Used by alpha-beta pruning to allow pruning

    '''
    The state of the game is represented by a list of 4 items:
        0. The game board - a matrix (list of lists) of ints. Empty cells = 0,
        the comp's cells = COMPUTER and the human's = HUMAN
        1. The heuristic value of the state.
        2. Whose turn is it: HUMAN or COMPUTER
        3. Number of empty cells
    '''


# create state Returns an empty board, The human plays first.
def createInitState(state):
    # create the board
    state.board = []
    for i in range(rows):
        state.board = state.board + [columns * [0]]

    state.board = np.array(state.board)

    state.playTurn = HUMAN
    state.size = rows * columns
    state.val = 0.00001

    # return [board, 0.00001, playTurn, r*c]     # 0 is TIE


def cpy(s1):
    # construct a parent DataFrame instance
    s2 = Game()
    s2.playTurn = s1.playTurn
    s2.size = s1.size
    s2.board = copy.deepcopy(s1.board)
    # print("board ", s2.board)
    return s2


def state_value(state):
    # the next lines compute the heuristic val
    diagonal_row = [-SIZE + 1, -SIZE + 1, 0,SIZE-1]
    diagonal_column = [0, SIZE - 1, SIZE - 1, SIZE - 1]
    val = 0.00001
    # count the opportunities to full sequence (missing one step to win)
    victory_opportunities, loss_opportunities = 0, 0

    # pass all over the board
    for row in range(rows):
        for col in range(columns):
            # check the four possible sequences
            for i in range(len(diagonal_row)):
                # check specific possible sequence
                seq_value = checkSeq(state, row, col, row + diagonal_row[i], col + diagonal_column[i])

                if seq_value in [LOSS, VICTORY]:
                    return seq_value
                # if seq_value is one step from victory
                if seq_value == full_seq_val - 1:
                    victory_opportunities += 1
                # if seq_value is one step from loss
                if seq_value == -(full_seq_val - 1):
                    loss_opportunities += 1
                # sum the cell value
                val += seq_value
    # if there is two or more opportunities to win in next step so it promise victory
    if victory_opportunities >= 2:
        return PROMISE_VICTORY
    if loss_opportunities >= 2:
        return PROMISE_LOSS
    if state.size == 0 and val not in [LOSS, VICTORY]:
        return TIE
    return val


def checkSeq(s, r1, c1, r2, c2):  # r2,c2 = end of the seq
    # r1, c1 are in the board. if r2,c2 not on board returns 0.
    # Checks the seq. from r1,c1 to r2,c2. If all X returns VICTORY. If all O returns LOSS.
    # If empty returns 0.00001. If no Os returns 1. If no Xs returns -1.
    if r2 < 0 or c2 < 0 or r2 >= rows or c2 >= columns:
        return 0  # r2, c2 are illegal

    dr = (r2 - r1) // (SIZE - 1)  # the horizontal step from cell to cell == 1
    dc = (c2 - c1) // (SIZE - 1)  # the vertical step from cell to cell

    sum = 0

    for i in range(SIZE):  # summing the values in the seq.
        sum += s.board[r1 + i * dr][c1 + i * dc]

    if sum == COMPUTER * SIZE:
        return VICTORY


    elif sum == HUMAN * SIZE:
        return LOSS

    if 0 < sum < COMPUTER:
        # if there is posibbelty fo computer sequence calculate that seq val and return it
        return - calculateVal(s, r1, c1, r2, c2)

    elif sum > 0 and sum % COMPUTER == 0:
        # if there is posibbelty fo human sequence calculate that seq val and return it
        return calculateVal(s, r1, c1, r2, c2)

    return 0.00001  # not 0 because TIE is 0


# return the heuristic value of specific sequence
def calculateVal(s, r1, c1, r2, c2):
    dr = (r2 - r1) // (SIZE - 1)  # the horizontal step from cell to cell
    dc = (c2 - c1) // (SIZE - 1)  # the vertical step from cell to cell

    # init the seq_val for the value of full seq
    seq_val = full_seq_val

    # reduce the distance from full sequence from the value
    for i in range(SIZE):  # summing the values in the seq.
        seq_val -= distance(s, r1 + i * dr, c1 + i * dc)

    return seq_val


# get: state and cell indexes
# return: the distance from puting token in that cell
def distance(state, row, column):
    sum = 0
    # sum while the cells in the column are empty
    while row < rows and state.board[row][column] == 0:
        sum += 1
        row += 1
    return sum


def printState(s):
    # Prints the board. The empty cells are printed as numbers = the cells name(for input)
    # If the game ended prints who won.
    for r in range(rows):
        print("\n|", end="")
        for c in range(columns):
            if s.board[r][c] == COMPUTER:
                print(colored("X", 'red'), "|", sep="", end="")
            elif s.board[r][c] == HUMAN:
                print(colored("0", 'cyan'), "|", sep="", end="")
            else:
                print(" |", end="")
    print()

    for i in range(columns):  # For numbers on the bottom
        print(" ", i, sep="", end="")

    print()

    val = state_value(s)

    if val == VICTORY:
        print("I won!")
    elif val == LOSS:
        print("You beat me!", 'red')
    elif val == TIE:
        print("It's a TIE")


def isFinished(s):
    # Seturns True iff the game ended
    return state_value(s) in [LOSS, VICTORY, TIE] or s.size == 0


def isHumTurn(s):
    # Return True iff it is the human's turn to play
    return s.playTurn == HUMAN


def decideWhoIsFirst(s):
    # The user decides who plays first
    if int(input("Who plays first? 1-me / anything else-you : ")) == 1:
        s.playTurn = COMPUTER
    else:
        s.playTurn = HUMAN
    return s.playTurn


def makeMove(s, c):
    # Puts mark (for human or computer) in col. c
    # and switches turns.
    # Assumes the move is legal.

    if s.board[0][c] != 0:
        return -1

    r = 0
    while r < rows and s.board[r][c] == 0:
        r += 1

    s.board[r - 1][c] = s.playTurn  # marks the board
    s.size -= 1  # one less empty cell
    if (s.playTurn == COMPUTER):
        s.playTurn = HUMAN
    else:
        s.playTurn = COMPUTER


def inputMove(s):
    # Reads, enforces legality and executes the user's move.
    flag = True
    while flag:
        c = int(input("Enter your next move: "))
        if c < 0 or c >= columns or s.board[0][c] != 0:
            print("Illegal move.")
        else:
            flag = False
            makeMove(s, c)


def inputRandom(s):
    # See if the random should block one move ahead
    '''for i in range(0,columns):
        tmp=cpy(s)
        makeMove(tmp, i)
        if(value(tmp)==VICTORY):
            makeMove(s,i)'''
    for i in range(0, columns):  # this simple agent always plays min
        tmp = cpy(s)
        if (state_value(tmp) == LOSS):  # so a "loss" is a win for this side
            makeMove(s, i)
    # If no obvious move, than move random
    flag = True
    while flag:
        c = random.randrange(0, columns)
        if c < 0 or c >= columns or s.board[0][c] != 0:
            print("Illegal move.")
            # printState(s)
            break
        else:
            flag = False

            makeMove(s, c)


# returns a list of the next states of s
def getNext(s):
    ns = []
    # pass all over the columns
    for c in list(range(columns)):  # why not range ?
        # if there is place for new token at this column
        if s.board[0][c] == 0:
            # copy the current state
            tmp = cpy(s)
            # put token at this column (in the copy board)
            makeMove(tmp, c)
            # add the state to the next state list
            ns += [tmp]
    return ns


def inputComputer(s):
    return alphaBetaPruning.go(s)
