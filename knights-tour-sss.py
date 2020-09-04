# Import tkinter module for Graphical User Interface
import tkinter as tk
from tkinter import messagebox
from tkinter import scrolledtext

def checkMove(x, y, board, boardSize):
    """
    Check if move to coordinate x and y is a valid move

    :param x: the destination in x
    :param y: the destination in y
    :param board: the chess board
    :return: boolean value, true if move is valid
    """
    if x >= 0 and x < boardSize and y >= 0 and y < boardSize and board[x][y] == 0:
        return True
    else:
        return False

def showSolution(board, boardSize):
    """
    Function to print the solution found by the program

    :param board: the chess board containing all moves
    :param boardSize: the size of the board
    :return: none
    """
    text = ''
    for i in range(boardSize):
        for j in range(boardSize):
            text = text + str(board[i][j]) + ' '
        text = text + '\n'

    txtBig.insert(tk.INSERT, text)  # Insert all text in variable text to the scrolled text box

def solve(boardSize, board, x, y, moveCoord, count):
    """
    Recursive function to find the solution, and this function uses backtracking feature.
    True will be returned if the knight successfully moves. If no single move is available when
    calling this function, this function will undo the knight's last move by changing last move's
    coordinate to 0 and return False.

    :param boardSize: the size of the chess board
    :param board: the chess board containing all moves
    :param x: current x position of the knight
    :param y: current y position of the knight
    :param moveCoord: list of x and y moves that are legal to do
    :param count: counter that increases everytime the knight moves
    :return: boolean value, true if the knight successfully moved
    """
    # If the knight has visited all space, return True
    if count - 1 == boardSize ** 2:
        return True

    # Try all next possible moves from the current position
    for i in range(8):
        if checkMove(x + moveCoord[i][0], y + moveCoord[i][1], board, boardSize):
            board[x + moveCoord[i][0]][y + moveCoord[i][1]] = count
            if solve(boardSize, board, x + moveCoord[i][0], y + moveCoord[i][1], moveCoord, count + 1):
                return True
            else:
                board[x + moveCoord[i][0]][y + moveCoord[i][1]] = 0 # If the previous solution fails, undo by resetting current coordinate to -1 again

    return False

def buttonSolve():
    """
    Solve the Knight's Tour problem with the board size specified from the user input spinbox,
    this function is called by pressing 'Solve!' button, and will solve the puzzle
    by calling solve(boardSize, board, x, y, moveCoord, count) recursive function.

    :return: none
    """
    # Input validation
    try:
        boardSize = int(txtInputSize.get())
        startX = int(txtStartX.get())
        startY = int(txtStartY.get())
        # Raise ValueError if input is invalid (e.g. input < 0)
        if boardSize < 0:
            raise ValueError
        if startX < 0 or startY < 0 or startX > boardSize - 1 or startY > boardSize - 1:
            raise ValueError
    except ValueError:
        messagebox.showerror('ERROR!', 'Invalid input')    # Show error message
        return                                             # Get out of this function

    # Ask the user for confirmation to continue
    confirm = messagebox.askokcancel('Continue?', 'Depends on the board size, this might take a while to find the solution. Continue?')
    if confirm:
        # Clear scrolled text box
        txtBig.delete(1.0, tk.END)

        # Initialise the chess board
        board = []
        temp = []
        for i in range(boardSize):
            for j in range(boardSize):
                temp.append(0)
            board.append(temp)
            temp = []

        # list of x and y moves that are legal to do
        moveCoord = [
            [2, 1],
            [1, 2],
            [-1, 2],
            [-2, 1],
            [-2, -1],
            [-1, -2],
            [1, -2],
            [2, -1]]

        # Set the value of the starting position to 1
        board[startX][startY] = 1

        # Counter that increases everytime the knight moves. Starts from 2 since it is the next move after the starting position
        moveCount = 2

        if (solve(boardSize, board, startX, startY, moveCoord, moveCount)):
            showSolution(board, boardSize)
            lblResult.configure(text='Solution found')
        else:
            lblResult.configure(text='Solution does not exist')
            txtBig.insert(tk.INSERT, '-')
    else:
        return  # If the user decides to cancel, get out of this function

window = tk.Tk()
window.title('Knight\'s Tour Problem Solver')
window.geometry('270x250')
window.resizable(False, False)

# Labels
lblInputSize = tk.Label(window, text='Board size:', font=('Arial', 10))
lblStartPos = tk.Label(window, text='Start Coordinate:', font=('Arial', 10))
lblResult = tk.Label(window, text='', font=('Arial', 10))

# Label placements
lblInputSize.grid(column=0, row=0)
lblStartPos.grid(column=0, row=1)
lblResult.place(x=100, y=45)

# Spinbox
var = tk.IntVar()
var.set(5)
txtInputSize = tk.Spinbox(window, from_=0, to=100, width=7, textvariable=var)
txtStartX = tk.Spinbox(window, from_=0, to=100, width=7)
txtStartY = tk.Spinbox(window, from_=0, to=100, width=7)

# Spinbox placement
txtInputSize.grid(column=1, row=0)
txtStartX.grid(column=1, row=1)
txtStartY.grid(column=2, row=1)

# Scrolled text
txtBig = scrolledtext.ScrolledText(window, width=30, height=10)

# Scrolled text placement
txtBig.place(x=5, y=75)

# Button
btnSolve = tk.Button(window, text='Solve!', command=buttonSolve, width=10)

# Button placement
btnSolve.grid(column=0, row=2)

window.mainloop()