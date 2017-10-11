from operator import itemgetter
from search import *

__lines = 0
__columns = 0
colorsDict = {}

#------------------------------------------------------------------------------#
#
#            ADT Color
#
# -----------------------------------------------------------------------------#
def is_color(c):
    if isinstance(c, int):
        return True
    return False


def get_color(board, line, column):
    return board[line][column]


def set_color(board, line, column, newcolor):
    p = make_pos(line, column)
    if is_color(newcolor):
        board[pos_l(p)][pos_c(p)] = newcolor


def get_no_color():
    return 0


def no_color(c):
    return c == 0


def color(c):
    return c > 0


def eq_colors(c1, c2):
    if is_color(c1) and is_color(c2):
        return c1 == c2
    return False


#------------------------------------------------------------------------------#
#
#            ADT Position
#
# -----------------------------------------------------------------------------#
def make_pos(l, c):
    if not (isinstance(l, int) and l >= 0 and isinstance(c, int) and c >= 0):
        raise ValueError("new_position: invalid arguments")
    return (l, c)


def is_pos(p):
    if isinstance(p, tuple) and len(p) == 2 and isinstance(p[0], int) and p[0] >= 0 and isinstance(p[1], int) and p[1] >= 0:
        return True
    return False


def pos_l(p):
    if is_pos(p):
        return p[0]
    return -1


def pos_c(p):
    if is_pos(p):
        return p[1]
    return -1


def pos_color(board, p):
    if is_pos(p):
        return board[pos_l(p)][pos_c(p)]


def eq_pos(p1, p2):
    if is_pos(p1) and is_pos(p2) and pos_l(p1) == pos_l(p2) and pos_c(p1) == pos_c(p2):
        return True
    return False


#------------------------------------------------------------------------------#
#
#            ADT Board
#
# -----------------------------------------------------------------------------#
def is_column_empty(board, columnnumber):
    if no_color(board[__lines - 1][columnnumber]):
        return True
    return False


def is_empty(board):
    global __lines
    for line in range(__lines):
        for column in range(__columns):
            if board[line][column] != 0:
                return False
    return True


# Calculates the adjacent coordinates to the given root (line, column).
# Only returns the ones that are valid (inside the board).
def get_adjacent_coordinates(line, column):
    # Starts the list as empty.
    adjacent = []
    # Calculates the board borders to check if a piece is inside the board.
    bottomborder = __lines - 1
    topborder = 0
    leftborder = 0
    rightborder = __columns - 1
    # For each adjacent coordiante, chacks if it is valid.
    for adj in [(line - 1, column), (line + 1, column), (line, column - 1), (line, column + 1)]:
        if bottomborder >= pos_l(adj) >= topborder and rightborder >= pos_c(adj) >= leftborder:
            # If it is inside the board, adds it to the list.
            adjacent.append(adj)
        # Returns the list of adjacent valid coordinates.
    return adjacent


# Traverses the matrix as a DFS to find all the adjacent pieces with the same
# color as the root in the board, starting in the given root's coordinates.
def root_find_group(board, visited, rootline, rootcolumn):
    # Marks the root piece as visited.
    visited[rootline][rootcolumn] = True
    # Starts the cluster with just the root piece.
    cluster = [(rootline, rootcolumn)]
    # Starts the queue with just the root piece.
    queue = [(rootline, rootcolumn)]
    # Gets the root color so it doens't need to access the matrix even more
    # times.
    rootcolor = get_color(board, rootline, rootcolumn)
    while len(queue) > 0:
        # Removes a piece from the list.
        nextposition = queue.pop()
        # Gets the board coordinates of the piece.
        line = pos_l(nextposition)
        column = pos_c(nextposition)
        # Gets the adjacent coordinates of the current one.
        adjacentballs = get_adjacent_coordinates(line, column)
        # For each adjacent coordinate checks if it meets the requirements
        # to be added to the cluster.
        for pos in adjacentballs:
            
            # Gets the adjacent coordinates.
            line = pos_l(pos)
            column = pos_c(pos)
            # Checks if the coordinate is not empty.
            # If it is not, checks if the coordinate's piece is the same
            # color as the root piece.
            
            if not visited[line][column] and eq_colors(rootcolor, get_color(board, line, column)):
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


def board_find_groups(board):
    lines = __lines
    columns = __columns
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
            if color(get_color(board, i, j)) and not visited[i][j]:
                # Gets the cluster of which the ball in the current position
                # belongs to.
                newcluster = root_find_group(board, visited, i, j)
                # Adds the newly found cluster to the cluster list.
                clusters.append(newcluster)
            # Returns all the clusters on the board.
    return clusters


def concatenate_lines(boardcopy, cluster, index):
    maxlines = __lines
    verticaldisplacement = 0
    clusterindex = index
    column = pos_c(cluster[clusterindex])
    # For each line lowers it to the lowest empty space in the same column.
    for line in reversed(range(maxlines)):
        # Checks if there are more holes. OutOfBounds exception would occour otherwise.
        # Checks if the current position is empty.
        if clusterindex < len(cluster) and line == pos_l(cluster[clusterindex]) and column == pos_c(cluster[clusterindex]):
            ''' Increments the vertical displacement counter, so the pieces above it get lowered by as many holes as
            there are beneath them. The clusterindex variable also updates because the next hole will have the
            coordinates of the next position in the removed cluster list. At the same time it sets the current
            position to 0. '''
            verticaldisplacement += 1
            clusterindex += 1
            set_color(boardcopy, line, column, get_no_color())
        elif verticaldisplacement > 0:
            '''If the current game piece has holes beneath it, represented by the verticaldisplacement variable,
            then it lowers that piece the same amount of lines. Setting the value of the current piece to zero.'''
            set_color(boardcopy, line + verticaldisplacement, column, get_color(boardcopy, line, column))
            set_color(boardcopy, line, column, get_no_color())
    return clusterindex, boardcopy


def concatenate_columns(boardcopy):
    maxlines = __lines
    maxcolumns = __columns
    horizontaldisplacement = 0
    for column in range(maxcolumns):
        if boardcopy[maxlines - 1][column] == 0:
            horizontaldisplacement += 1
        elif horizontaldisplacement > 0:
            for line in range(maxlines):
                boardcopy[line][column - horizontaldisplacement] = boardcopy[line][column]
                boardcopy[line][column] = 0
    return boardcopy


def board_remove_group(board, group):
    boardcopy = []
    for line in board:
        boardcopy.append(list(line))
    cluster = group
    # Sorts the cluster by column, from rigth to left, and then by line, from top to bottom.
    cluster.sort(key=itemgetter(1, 0), reverse=True)
    clusterindex = 0
    while clusterindex < len(cluster):
        clusterindex, boardcopy = concatenate_lines(boardcopy, cluster, clusterindex)
    boardcopy = concatenate_columns(boardcopy)
    return boardcopy


def to_string(board):
    for l in range(__columns):
        print('[ ', end='')
        for c in range(__lines):
            print('{} '.format(board[l][c]), end='')
        print(']')


def setLines(lines, columns):
    global __lines
    global __columns
    __lines = lines
    __columns = columns


class sg_state:
    __slots__ = ['__board']

    def __init__(self, board):
        self.__board = board

    def update_board(self, newboard):
        self.__board = newboard

    def get_board(self):
        return self.__board

    def __lt__(self, other_sg_state):
        # TODO compares another sg_state with the current one and returns true if this one is less than other
        pass


class same_game(Problem):
    def __init__(self, board):
        lines = len(board)
        columns = len(board[1])
        setLines(lines, columns)

        initialstate = sg_state(board)
        emptyboard = []
        for i in range(lines):
            line = []
            for j in range(columns):
                # RFE: All these accesses to dictionary might cause program to run slower than intended
                colorinteger = get_color(board, i, j)
                colorstr = str(colorinteger)
                colorcount = colorsDict.setdefault(colorstr, 0)
                colorsDict[colorstr] += colorcount + 1
                line.append(0)
            emptyboard.append(line)
        goalstate = sg_state(emptyboard)
        super(same_game, self).__init__(initialstate, goalstate)

    '''Return the actions that can be executed in the given
    state. The result would typically be a list, but if there are
    many actions, consider yielding them one at a time in an
    iterator, rather than building them all at once.'''
    def actions(self, state):
        board = state.get_board()
        clusters = board_find_groups(board)
        validclusters = []
        for cluster in clusters:
            if len(cluster) >= 2:
                validclusters.append(cluster)               
        return validclusters

    '''Return the state that results from executing the given
    action in the given state. The action must be one of
    self.actions(state).'''
    def result(self, state, action):
        board = state.get_board()
        clustertoremove = action
        resultingboard = board_remove_group(board, clustertoremove)
        newstate = sg_state(resultingboard)
        return newstate

    '''Return True if the state is a goal. The default method compares the
    state to self.goal or checks for state in self.goal if it is a
    list, as specified in the constructor. Override this method if
    checking against a single self.goal is not enough.'''
    def goal_test(self, state):
        board = state.get_board()
        if is_empty(board):
            return True
        return False

    def path_cost(self, c, state1, action, state2):
        return c + 1

    def h(self, node):
        # state = node.state
        # board = state.get_board()
        return 


if __name__ == '__main__':
    board = [[1, 1, 1, 1], [2, 2, 2, 2], [3, 3, 3, 3], [4, 4, 4, 4]]
    #board = [[1, 2, 3, 4], [1, 2, 3, 4], [1, 2, 3, 4], [1, 2, 3, 4]]
    #board = [[1,2,2,3,3],[2,2,2,1,3],[1,2,2,2,2],[1,1,1,1,1]]
    problem = same_game(board)
    depth_first_tree_search(problem)