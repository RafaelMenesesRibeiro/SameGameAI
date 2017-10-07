from boardAlpha import *
import random


class sg_state:
    __slots__ = ['__board']

    def __init__(self, board):
        self.__board = board

    def update_board(self, newboard):
        self.__board = newboard

    def __lt__(self, other_sg_state):
        # TODO compares another sg_state with the current one and returns true if this one is less than other
        pass
