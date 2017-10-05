class Position:
    __line = 0
    __column = 0
    __position = (0, 0)

    def __init__(self, l, c):
        self.__line = l
        self.__column = c
        self.__position = (l, c)

    def get_line(self):
        return self.__line

    def get_column(self):
        return self.__column

    def get_position(self):
        return self.__position

    @staticmethod
    def make_pos(l, c):
        return (l, c)

    @staticmethod
    def pos_l(pos):
        return pos[0]

    @staticmethod
    def pos_c(pos):
        return pos[1]