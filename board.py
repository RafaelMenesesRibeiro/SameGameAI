from operator import itemgetter
import random
import search

class Board:
    __colorsNumber = 0
    __lines = 0
    __columns = 0
    __boardMatrix = []

    def __init__(self, lines, columns, colorsnumber):
        self.__lines = lines
        self.__columns = columns
        self.__colorsNumber = colorsnumber
        self.populate_board()

    def get_board(self):
        return self.__boardMatrix

    def populate_board(self):
        for l in range(self.__columns):
            line = []
            for c in range(self.__lines):
                color = random.randint(1, self.__colorsNumber)
                line.append(color)
            self.__boardMatrix.append(line)


    def is_empty(self):
        for l in range(self.__columns):
            for c in range(self.__lines):
                if self.__boardMatrix[l][c] != 0:
                    return False
        return True

    # Calculates the adjacent coordinates to the given root (line, column).
    # Only returns the ones that are valid (inside the board).

    def get_adjacent_coordinates(self, line, column):
        # Starts the list as empty.
        adjacent = []
        # Calculates the board borders to check if a piece is inside the board.
        bottomborder = self.__lines - 1
        topborder = 0
        leftborder = 0
        rightborder = self.__columns - 1
        # For each adjacent coordiante, chacks if it is valid.
        for adj in [(line - 1, column), (line + 1, column), (line, column - 1), (line, column + 1)]:
            if bottomborder >= adj[1] >= topborder and rightborder >= adj[0] >= leftborder:
                # If it is inside the board, adds it to the list.
                adjacent.append(adj)
            # Returns the list of adjacent valid coordinates.
        return adjacent

    # Traverses the matrix as a DFS to find all the adjacent pieces with the same
    # color as the root in the board, starting in the given root's coordinates.

    def root_find_group(self, visited, rootline, rootcolumn):
        # Marks the root piece as visited.
        visited[rootline][rootcolumn] = True
        # Gets a reference to the matrix to check the colors of the adjacent
        # pieces.
        board = self.__boardMatrix
        # Starts the cluster with just the root piece.
        cluster = [(rootline, rootcolumn)]
        # Starts the queue with just the root piece.
        queue = [(rootline, rootcolumn)]
        # Gets the root color so it doens't need to access the matrix even more
        # times.
        rootcolor = board[rootline][rootcolumn]
        while len(queue) > 0:
            # Removes a piece from the list.
            nextposition = queue.pop()
            # Gets the board coordinates of the piece.
            line = nextposition[0]
            column = nextposition[1]



            #print('rootLine {}, rootcolumn {}, current pos {} {}'.format(rootline, rootcolumn, line, column))

            # Gets the adjacent coordinates of the current one.
            adjacentballs = self.get_adjacent_coordinates(line, column)
            # For each adjacent coordinate checks if it meets the requirements
            # to be added to the cluster.
            for pos in adjacentballs:
                # Gets the adjacent coordinates.
                line = pos[0]
                column = pos[1]
                # Checks if the coordinate is not empty.
                # If it is not, checks if the coordinate's piece is the same
                # color as the root piece.
                if not visited[line][column] and board[line][column] == rootcolor:
                    # In case the requirements are met, adds the adjacent piece
                    # to the cluster and to the queue, so its adjacent pieces
                    # can be added to the cluster (if the conditions are met).
                    cluster.append((line, column))
                    queue.append((line, column))
                    # Sets the visitation flag to True so it doens't get added
                    # again.
                    visited[line][column] = True
                # Returns the list of coordinates that are adjacent to each other and
                # are the same color as the root.
        return cluster

    def board_find_groups(self):
        lines = self.__lines
        columns = self.__columns
        # Creates the matrix that represents if a position has been checked for
        # or has been added to a cluster. Initiates all to False because no
        # position was visited yet.
        visited = [[False for _ in range(columns)] for _ in range(lines)]
        # Creates the empty list of clusters.
        clusters = []
        # For each valid (non empty) position on the board, gets its cluster.
        for i in range(lines):
            for j in range(columns):
                # Checks if the current position in empty and if it is, checks
                # if the position was already visited (in a previous BFS).
                if self.__boardMatrix[i][j] != 0 and not visited[i][j]:
                    #print('CALLING ROOT FIND WITH {} {}'.format(i, j))
                    # Gets the cluster of which the ball in the current position
                    # belongs to.
                    newcluster = self.root_find_group(visited, i, j)
                    # Adds the newly found cluster to the cluster list.
                    clusters.append(newcluster)
                # Returns all the clusters on the board.
        return clusters

    def concatenate_lines(self, boardcopy, cluster, index):
        boardlines = self.__lines
        verticaldisplacement = 0
        clusterindex = index
        currentcolumn = cluster[clusterindex][1]
        # For each line lowers it to the lowest empty space in the same column.
        for currentline in reversed(range(boardlines)):
            # Checks if there are more holes. OutOfBounds exception would occour otherwise.
            # Checks if the current position is empty.
            if clusterindex < len(cluster) and currentline == cluster[clusterindex][0] and currentcolumn == \
                    cluster[clusterindex][1]:
                ''' Increments the vertical displacement counter, so the pieces above it get lowered by as many holes as
                there are beneath them. The clusterindex variable also updates because the next hole will have the
                coordinates of the next position in the removed cluster list. At the same time it sets the current
                position to 0. '''
                verticaldisplacement += 1
                clusterindex += 1
                boardcopy[currentline][currentcolumn] = 0
            else:
                '''If the current game piece has holes beneath it, represented by the verticaldisplacement variable,
                then it lowers that piece the same amount of lines. Setting the value of the current piece to zero.'''
                if verticaldisplacement > 0:
                    currentpiece = boardcopy[currentline][currentcolumn]
                    boardcopy[currentline + verticaldisplacement][currentcolumn] = currentpiece
                    boardcopy[currentline][currentcolumn] = 0
                else:
                    continue
        return clusterindex, boardcopy

    def concatenate_columns(self, boardcopy):
        maxcolumns = self.__columns
        maxlines = self.__lines
        horizontaldisplacement = 0
        for column in range(maxcolumns):
            if boardcopy[maxlines - 1][column] == 0:
                horizontaldisplacement += 1
            else:
                if horizontaldisplacement == 0:
                    continue
                for line in range(maxlines):
                    boardcopy[line][column - horizontaldisplacement] = boardcopy[line][column]
                    boardcopy[line][column] = 0
        return boardcopy

    def board_remove_group(self, group):
        boardcopy = []
        for line in self.__boardMatrix:
            boardcopy.append(list(line))
        cluster = group
        # Sorts the cluster by column, from rigth to left, and then by line, from top to bottom.
        cluster.sort(key=itemgetter(1, 0), reverse=True)
        clusterindex = 0
        while clusterindex < len(cluster):
            clusterindex, boardcopy = self.concatenate_lines(boardcopy, cluster, clusterindex)
        boardcopy = self.concatenate_columns(boardcopy)
        return boardcopy

    def to_string(self):
        for l in range(self.__columns):
            print('[ ', end='')
            for c in range(self.__lines):
                print('{} '.format(self.__boardMatrix[l][c]), end='')
            print(']')


if __name__ == '__main__':
    board = Board(4, 4, 4)
    board.to_string()
    clusters = board.board_find_groups()
    print(clusters)
    group  = clusters[0]
    board2 = board.board_remove_group(group)
    print(board2)
    board.to_string()
    

