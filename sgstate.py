from boardAlpha import *


class sg_state:
    __board = []

    def __init__(self, lines, columns, colorsnum):
        board = Board(lines, columns, colorsnum)
        board.populate_board()
        self.__board = board

    def set_board(self, newboard):
        self.__board = newboard