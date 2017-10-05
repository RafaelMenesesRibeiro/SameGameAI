class Board:
    __colorsNumber = 0
    __lines = 0
    __filledLines = 0
    __columns = 0
    __filledColumns = 0
    __boardMatrix = []

    def __init__(self, lines, columns, colorsnumber):
        self.__lines = lines
        self.__columns = columns
        self.__colorsNumber = colorsnumber

    def get_board(self):
        return self.__boardMatrix

    def get_columns(self):
        return self.__columns

    def get_lines(self):
        return self.__lines

    def get_colors_number(self):
        return self.__colorsNumber

    def get_filled_lines(self):
        return self.__filledLines

    def get_filled_columns(self):
        return self.__filledColumns

    def set_filled_lines(self, n):
        self.__filledLines = n

    def set_filled_columns(self, n):
        self.__filledColumns = n

    def board_find_groups(self):
        # TODO
        pass

    def board_remove_group(self, group):
        # TODO
        pass

    def populate_board(self):
        # TODO
        pass

    def to_string(self):
        print('Printing SameGame board with ', self.__lines, 'and ', self.__columns, '...')
        print('  ', end='')
        for i in range(self.__columns):
            print(i, end=' ')
        for l in self.__boardMatrix:
            print()
            print(l, end=' ')
            for c in self.__boardMatrix[l]:
                print(self.__boardMatrix[l][c], end=' ')
        print('\nDone')



