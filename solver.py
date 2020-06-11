from PIL import Image, ImageDraw
import pyautogui as pag 
import time
import cv2
import copy
import numpy as np

sudoku = np.zeros((9, 9), dtype=int).tolist()


def printsudoku(sudoku):
    print("\n")
    for i in range(len(sudoku)):
        line = ""
        if i == 3 or i == 6:
            print("---------------------")
        for j in range(len(sudoku[i])):
            if j == 3 or j == 6:
                line += "| "
            line += str(sudoku[i][j]) + " "
        print(line)
    print("\n")

def findNextCellToFill(sudoku):
    for x in range(9):
        for y in range(9):
            if sudoku[x][y] == 0:
                return x, y
    return -1, -1

def isValid(sudoku, i, j, e):
    rowOk = all([e != sudoku[i][x] for x in range(9)])
    if rowOk:
        columnOk = all([e != sudoku[x][j] for x in range(9)])
        if columnOk:
            secTopX, secTopY = 3*(i//3), 3*(j//3)
            for x in range(secTopX, secTopX+3):
                for y in range(secTopY, secTopY+3):
                    if sudoku[x][y] == e:
                        return False
            return True
    return False


def solveSudoku(sudoku, i=0, j=0):
    i, j = findNextCellToFill(sudoku)
    if i == -1:
        return True

    for e in range(1, 10):
        if isValid(sudoku, i, j, e):
            sudoku[i][j] = e
            if solveSudoku(sudoku, i, j):
                return True
            sudoku[i][j] = 0
    return False




topleftx = 2805
toplefty = 475
bottomrightx = 3135
bottomrighty = 812

boxwidth = (bottomrightx - topleftx)/8
boxheight = (bottomrighty - toplefty)/8

def fillsudoku(nr, pos):
    global sudoku
    indexlocx = int((pos[0] - topleftx + boxwidth/2)//boxwidth)
    indexlocy = int((pos[1] - toplefty + boxheight/2)//boxwidth)
    sudoku[indexlocy][indexlocx] = nr

time.sleep(2)
for i in range(1, 10):
    for pos in pag.locateAllOnScreen(str(i) + ".png", confidence=0.85):
        fillsudoku(i, pos)

def fillcell(nr, x, y):
    xcoord = topleftx + boxwidth * x
    ycoord = toplefty + boxheight * y
    pag.click(xcoord+4, ycoord+4)
    pag.press(str(nr))

printsudoku(sudoku)
sudokucopy = copy.deepcopy(sudoku)
solveSudoku(sudoku)
printsudoku(sudoku)

for x in range(9):
    for y in range(9):
        if sudokucopy[x][y] == 0:
            fillcell(sudoku[x][y], y, x)
