#################################################
# 15-112-n19 hw-tetris
# Your Name: Zachary Zheng
# Your Andrew ID: zacharyz
# Your Section: C
# Collaborators: N/A
#################################################

"""Bonus Features: Levels of Play, Pause Button ('p')"""

######################################################################
# ignore_rest: The autograder will ignore all code below here
######################################################################

from tkinter import *
import math

#sets all the color for each cell to blue
def starterBoard(data):
    board = []
    for row in range(data.rows):
        innerList = []
        for col in range(data.cols):
            innerList.append("blue")
        board.append(innerList)
    return board

def init(data):
    data.rows, data.cols = 15, 10
    data.margin = 50
    data.boardWidth = data.width - 2 * data.margin
    data.boardHeight = data.height - 2 * data.margin
    data.cellWidth = data.boardWidth // data.cols
    data.cellHeight = data.boardHeight // data.rows
    data.board = starterBoard(data)
    data.emptyColor = "blue"
    data.isPause = False
    data.isGameOver = False
    data.timerDelay = 300
    data.score = 0
    data.levelCounter = 0
    iPiece = [[  True,  True,  True,  True ]]
    jPiece = [[  True, False, False ],[  True,  True,  True ]]
    lPiece = [[ False, False,  True ],[  True,  True,  True ]]
    oPiece = [[  True,  True ],[  True,  True ]]
    sPiece = [[ False,  True,  True ],[  True,  True, False ]]
    tPiece = [[ False,  True, False ],[  True,  True,  True ]]
    zPiece = [[  True,  True, False ],[ False,  True,  True ]]
    data.tetrisPieces = [iPiece, jPiece, lPiece, oPiece, sPiece, tPiece, zPiece]
    data.tetrisPieceColors = ["red","yellow","magenta","pink","cyan","green",
    "orange"]
    newFallingPiece(data)

def mousePressed(event, data):
    # use event.x and event.y
    pass

#checks if the current loc of piece is within the board range and on empty color
def fallingPieceIsLegal(data):
    for row in range(len(data.fallingPiece)):
        for col in range(len(data.fallingPiece[0])):
            if data.fallingPiece[row][col]:
                adjustedRow = row + data.fallingPieceRow
                adjustedCol = col + data.fallingPieceCol
                '''checks if the cells of the piece are outside of the board
                or if it's occupying a square that's not an empty color''' 
                if adjustedRow < 0 or adjustedRow > data.rows - 1 or \
                adjustedCol < 0 or adjustedCol > data.cols - 1 or \
                data.board[adjustedRow][adjustedCol] != data.emptyColor:
                    return False
    return True #returns true if every cell is within range and on empty cell


#helper function that forms the 2D list for the new rotated piece
def makeNewPiece(oldNumRows, oldNumCols, newNumRows, newNumCols, oldPiece):
    newPiece = []
    for row in range(newNumRows):
        eachRow = []
        for col in range(newNumCols):
            eachRow.append(None)
        newPiece.append(eachRow)
    #creates the new values for each of the cells of rotated piece    
    for row in range(oldNumRows):
        for col in range(oldNumCols):
            newPiece[newNumRows - 1 - col][row] = oldPiece[row][col] 
    return newPiece


def rotateFallingPiece(data):
    #stores data for old pieces into temp variables
    oldNumRows = len(data.fallingPiece)
    oldNumCols = len(data.fallingPiece[0])
    oldRow = data.fallingPieceRow
    oldCol = data.fallingPieceCol
    oldPiece = data.fallingPiece
    #computes the new data for the new rotated piece
    newNumRows = oldNumCols
    newNumCols = oldNumRows
    newRow = oldRow + oldNumRows // 2 - newNumRows // 2
    newCol = oldCol + oldNumCols // 2 - newNumCols // 2
    #stores the new data into the official falling piece
    data.fallingPieceRow = newRow
    data.fallingPieceCol = newCol
    data.fallingPiece = makeNewPiece(oldNumRows, oldNumCols, newNumRows,
    newNumCols, oldPiece)
    #resets the piece location if the move is not valid 
    if not fallingPieceIsLegal(data):
        data.fallingPieceRow = oldRow
        data.fallingPieceCol = oldCol
        data.fallingPiece = oldPiece

#changes row and col of piece based off of key presses
def moveFallingPiece(data, drow, dcol):
    data.fallingPieceRow += drow
    data.fallingPieceCol += dcol
    #resets the piece location if the move is not valid
    if not fallingPieceIsLegal(data):
        data.fallingPieceRow -= drow
        data.fallingPieceCol -= dcol
        return False
    return True

#detects arrow key presses and calls moveFallingPiece based off it    
def keyPressed(event, data):
    # use event.char and event.keysym
    if not data.isGameOver:
        if not data.isPause:
            if event.keysym == "Left":
                moveFallingPiece(data, 0, -1)
            elif event.keysym == "Right":
                moveFallingPiece(data, 0, +1)
            elif event.keysym == "Down":
                moveFallingPiece(data, +1, 0)
            elif event.keysym == "Up":
                rotateFallingPiece(data)
    #sets the game in pause mode
    if event.char == "p":
        data.isPause = not data.isPause
    #checks if user presses 'r' to restart the game
    if event.char == "r":
        init(data)

#piece speed is increased through a 50 millisecond reduction in time delay
def speedIncrease(data):
    if data.levelCounter % 3 == 0 and data.timerDelay - 50 > 0:
        data.timerDelay -= 50

#creates a new board that doesn't contain the filled up rows
def removeFullRows(data):
    newBoard = []
    #adds the rows that are not full into the new board
    for row in range(data.rows):
        emptyCount = 0
        currentRow = []
        for col in range(data.cols):
            currentRow.append(data.board[row][col])
            if data.board[row][col] == data.emptyColor:
                emptyCount += 1
        if emptyCount != 0:
            newBoard.append(currentRow)
    #calculate num of full rows removed and adds score based of that
    fullRowCount = data.rows - len(newBoard)
    data.score += fullRowCount ** 2
    #adds empty-color rows to top of board til board is full
    while len(newBoard) < data.rows:
        newBoard.insert(0, [data.emptyColor] * data.cols)
    data.board = newBoard
    #increased speed/level every third time rows are cleared
    if fullRowCount > 0:
        data.levelCounter += 1
        speedIncrease(data)

#adds piece as part of the board
def placeFallingPiece(data):
    for row in range(len(data.fallingPiece)):
        for col in range(len(data.fallingPiece[0])):
            #only places color on board if contains True
            if data.fallingPiece[row][col]:
                #adds the offset of the row and col to properly position piece
                adjustedRow = row + data.fallingPieceRow 
                adjustedCol = col + data.fallingPieceCol
                data.board[adjustedRow][adjustedCol] = data.fallingPieceColor
    removeFullRows(data)

#moves the falling piece down automatically and also checks if game is over
def timerFired(data):
    if not data.isGameOver:
        if not data.isPause:
            if not moveFallingPiece(data, +1, 0):
                placeFallingPiece(data)
                newFallingPiece(data)
                if not fallingPieceIsLegal(data):
                    data.isGameOver = True

#draws each individual cell with corresponding color
def drawCell(canvas, data, row, col, color):
    left = data.margin + col * data.cellWidth
    top = data.margin + row * data.cellHeight
    right = left + data.cellWidth
    bot = top + data.cellHeight
    canvas.create_rectangle(left, top, right, bot, fill = color, width = 5)

#draws the board with all the individual cells
def drawBoard(canvas, data):
    for row in range(data.rows):
        for col in range(data.cols):
            drawCell(canvas, data, row, col, data.board[row][col])

#generates a random tetris piece with its color
def newFallingPiece(data):
    import random
    #randint to pick a random item in tetrisPiece
    randomIndex = random.randint(0, len(data.tetrisPieces) - 1)
    data.fallingPiece = data.tetrisPieces[randomIndex]
    data.fallingPieceColor = data.tetrisPieceColors[randomIndex]
    #determines the row and col of top left corner of the falling piece
    data.fallingPieceRow = 0
    data.fallingPieceCol = (data.cols // 2) - (len(data.fallingPiece[0]) // 2)
 
#creates the falling piece on top of the board    
def drawFallingPiece(canvas, data):
    for row in range(len(data.fallingPiece)):
        for col in range(len(data.fallingPiece[0])):
            #only creates the cell of piece if it contains True
            if data.fallingPiece[row][col]:
                #adds the offset of the row and col to properly position piece
                adjustedRow = row + data.fallingPieceRow 
                adjustedCol = col + data.fallingPieceCol
                #calls for the drawCell function with the generated piece color
                drawCell(canvas, data, adjustedRow, adjustedCol,
                data.fallingPieceColor)

#draws the score that's displayed at the top of the board
def drawScore(canvas, data):
    x = data.width // 2
    y = data.margin // 2
    canvas.create_text(x, y, fill = "blue", font = "Arial 20 bold",
    text = "Score: %s" % str(data.score))

#displays the level that player currently is on
def levelCounter(canvas, data):
    x = data.width // 2
    y = data.height - data.margin // 2
    canvas.create_text(x, y, fill = "blue", font = "Arial 20 bold",
    text = "Level: %s" % str((data.levelCounter // 3) + 1))

def drawPause(canvas, data):
    x0 = data.margin
    y0 = data.margin + data.cellHeight * 6
    x1 = data.width - data.margin
    y1 = y0 + data.cellHeight * 2
    canvas.create_rectangle(x0, y0, x1, y1, fill = "black")
    canvas.create_text((x0 + x1) / 2, (y0 + y1) / 2, fill = "yellow",
    font = "Arial 30 bold", text = "Paused")
    
#draws the orange background, then the board, then the tetris piece
def redrawAll(canvas, data):
    # draw in canvas
    canvas.create_rectangle(0, 0, data.width, data.height, fill = "orange")
    drawBoard(canvas, data)
    drawScore(canvas, data)
    levelCounter(canvas, data)
    drawFallingPiece(canvas, data)
    #checks if game is over and prints game over screen
    if data.isPause:
        drawPause(canvas, data)
    if data.isGameOver:
        x0 = data.margin
        y0 = data.margin + data.cellHeight
        x1 = data.width - data.margin
        y1 = data.margin + 3 * data.cellHeight
        canvas.create_rectangle(x0, y0, x1, y1, fill = "black")
        canvas.create_text(data.margin + data.boardWidth / 2,
        data.margin + 2 * data.cellHeight, fill = "yellow",
        font = "Arial 30 bold", text = "Game Over!")

####################################
# use the run function as-is
####################################

def run(width=400, height=600):
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        canvas.create_rectangle(0, 0, data.width, data.height,
                                fill='white', width=0)
        redrawAll(canvas, data)
        canvas.update()

    def mousePressedWrapper(event, canvas, data):
        mousePressed(event, data)
        redrawAllWrapper(canvas, data)

    def keyPressedWrapper(event, canvas, data):
        keyPressed(event, data)
        redrawAllWrapper(canvas, data)

    def timerFiredWrapper(canvas, data):
        timerFired(data)
        redrawAllWrapper(canvas, data)
        # pause, then call timerFired again
        canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)
    # Set up data and call init
    class Struct(object): pass
    data = Struct()
    data.width = width
    data.height = height
    data.timerDelay = 100 # milliseconds
    root = Tk()
    init(data)
    # create the root and the canvas
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.configure(bd=0, highlightthickness=0)
    canvas.pack()
    # set up events
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    timerFiredWrapper(canvas, data)
    # and launch the app
    root.mainloop()  # blocks until window is closed
    print("bye!")

def playTetris(rows=15, cols=10):
    # use the rows and cols to compute the appropriate window size here!
    run()

playTetris()