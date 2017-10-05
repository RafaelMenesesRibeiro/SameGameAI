from operator import itemgetter
import random

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
        boardcopy = []
        for line in self.__boardMatrix:
            boardcopy.append(list(line))
        cluster = group().get_cluster()
        ''' Sorts cluster by Column and then by Line in descending order. First position in the list is the position
        ' that is further to the right and to the top of the board among the given cluster.
        '''
        cluster.sort(key=itemgetter(2, 1), reverse=True)
        '''i is width counter, j is the index of the position within the cluster list
        ' maxshifts variable counts how far upper pieces will fall, aux helps detecting column jumps'
        '''
        i, j, maxshifts, shifts = 0, 0, 0, 0
        aux = cluster[j]().get_column()
        '''clusterlen will allow us to access the position with the lowest column value, allowing us to obtain 
        ' the clusterwidth. But we always need to add one. For instance, if we are removing balls from only column, 
        ' the clusterwidth would be zero.
        '''
        clusterlen = len(cluster)
        clusterwidth = aux - cluster[clusterlen].get_column() + 1
        while i < clusterwidth:
            ''' As long as we are in the current column, we count how many ball deletations will occur, increasing our
            ' maxshifts for that purpose and our j to check the next position in the cluster list.
            '''
            currentcolumn = cluster[j]().get_column()
            if currentcolumn == aux:
                currentline = cluster[j]().get_line()
                maxshifts = maxshifts + 1
                j = j + 1
            else:
                ''' If we changed one column to the left (cluster as positions ordered in descending order of column value
                ' then we go back one column and start deleting balls, letting the ones above fall.
                '''
                currentcolumn = currentcolumn + 1
                while True:
                    ''' If we would go out of bounds during ball replacement, then we just delete the position we are at.'
                    ' If currentline-maxshifts is a valid board line, then we make a replacement as expected.
                    '''
                    if currentline-maxshifts < 0:
                        boardcopy[currentline][currentcolumn] = 0
                        shifts = shifts + 1
                    else:
                        boardcopy[currentline][currentcolumn] = boardcopy[currentline-maxshifts][currentcolumn]
                        boardcopy[currentline-maxshifts][currentcolumn] = 0
                        currentline = currentline - 1
                        shifts = shifts + 1
                    if shifts == maxshifts:
                        ''' Update i and aux to indicate we are done updating the first column of the cluster. Reset the
                        ' remaining assisting variables. 
                        '''
                        i = i + 1
                        aux = aux - 1
                        maxshifts = 0
                        shifts = 0
                        break
        return boardcopy

    def populate_board(self):
        print('Populating game board...')
        for l in range(self.__columns):
            for c in range(self.__lines):
                color = random.randint(1, self.__colorsNumber)
                self.__boardMatrix[l][c] = color
        print('Done')

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
