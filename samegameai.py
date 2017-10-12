from operator import itemgetter
from search import *

lines = 0
columns = 0

#------------------------------------------------------------------------------#
#
#            ADT Color
#
# -----------------------------------------------------------------------------#
def is_color(c):
	if isinstance(c, int):
		return True
	return False


def get_color(board, l, c):
	return board[l][c]


def set_color(board, l, c, color):
	p = make_pos(l, c)
	if is_color(color):
		board[pos_l(p)][pos_c(p)] = color


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

def pos_l(p):
	return p[0]

def pos_c(p):
	return p[1]

def pos_color(board, p):
	return board[pos_l(p)][pos_c(p)]

#------------------------------------------------------------------------------#
#
#            ADT Board
#
# -----------------------------------------------------------------------------#
def is_empty(board, lines, columns):
	for l in range(lines):
		for c in range(columns):
			if board[l][c] != 0:
				return False
	return True


# Calculates the adjacent coordinates to the given root (line, column).
# Only returns the ones that are valid (inside the board).
def get_adjacent_coordinates(l, c, lines, columns):
	adjacentlist = []
	# Calculates the board borders to check if a piece is inside the board.
	bottomborder = lines - 1
	topborder = 0
	leftborder = 0
	rightborder = columns - 1
	# For each adjacent coordinate check its validity.
	for adj in [(l - 1, c), (l + 1, c), (l, c - 1), (l, c + 1)]:
		if bottomborder >= pos_l(adj) >= topborder and rightborder >= pos_c(adj) >= leftborder:
			# If it is inside the board, adds it to the list.
			adjacentlist.append(adj)
		# Returns the list of adjacent valid coordinates.
	return adjacentlist


# Traverses the matrix as a DFS to find all the adjacent pieces with the same
# color as the root in the board, starting in the given root's coordinates.
def root_find_group(board, visited, rootline, rootcolumn, lines, columns):
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
		l = pos_l(nextposition)
		c = pos_c(nextposition)
		# Gets the adjacent coordinates of the current one.
		adjacentballs = get_adjacent_coordinates(l, c, lines, columns)
		# For each adjacent coordinate checks if it meets the requirements to be added to the cluster.
		for pos in adjacentballs:
			# Gets the adjacent coordinates.
			l = pos_l(pos)
			c = pos_c(pos)
			# Checks if the coordinate is not empty and if the coordinate's piece is the same color as the root piece.
			if not visited[l][c] and rootcolor == get_color(board, l, c):
				# In case the requirements are met, adds the adjacent piece to the cluster and to the queue
				cluster.append((l, c))
				queue.append((l, c))
				# Sets the visitation flag to True so it doesnt get added again.
				visited[l][c] = True
			# Returns the list of coordinates that are adjacent to each other and are the same color as the root.
	return cluster


def board_find_groups(board):
	lines = len(board)
	columns = len(board[0])
	clusters = []
	# Creates the matrix that represents if a position has been checked for or has been added to a cluster.
	# Initiates all to False because no position was visited yet.
	visited = [[False for _ in range(columns)] for _ in range(lines)]
	# For each valid (non empty) position on the board, get its cluster.
	for l in range(lines):
		for c in range(columns):
			# Checks if the current position in empty and if it is, checks if the it was already visited in a previous BFS.
			if color(get_color(board, l, c)) and not visited[l][c]:
				# Get the cluster to which the ball in this position belongs to.
				newcluster = root_find_group(board, visited, l, c, lines, columns)
				newcluster.sort(key=itemgetter(0, 1))
				clusters.append(newcluster)
	return clusters

def board_find_valid_groups(board):
	lines = len(board)
	columns = len(board[0])
	clusters = []
	# Creates the matrix that represents if a position has been checked for or has been added to a cluster.
	# Initiates all to False because no position was visited yet.
	visited = [[False for _ in range(columns)] for _ in range(lines)]
	# For each valid (non empty) position on the board, get its cluster.
	for l in range(lines):
		for c in range(columns):
			# Checks if the current position in empty and if it is, checks if the it was already visited in a previous BFS.
			if color(get_color(board, l, c)) and not visited[l][c]:
				# Get the cluster to which the ball in this position belongs to.
				newcluster = root_find_group(board, visited, l, c, lines, columns)
				newcluster.sort(key=itemgetter(0, 1))
				if len(newcluster) >= 2:
					clusters.append(newcluster)
	return clusters


def concatenate_lines(boardcopy, cluster, index, lines):
	displacement = 0
	clusterindex = index
	c = pos_c(cluster[clusterindex])
	for l in reversed(range(lines)):
		if clusterindex < len(cluster) and l == pos_l(cluster[clusterindex]) and c == pos_c(cluster[clusterindex]):
			''' Increments the vertical displacement counter, so the pieces above it get lowered by as many holes as
			there are beneath them. The clusterindex variable also updates because the next hole will have the
			coordinates of the next position in the removed cluster list. At the same time it sets the current
			position to 0. '''
			displacement += 1
			clusterindex += 1
			set_color(boardcopy, l, c, get_no_color())
		elif displacement > 0:
			'''If the current game piece has holes beneath it, represented by the displacement variable,
			then it lowers that piece the same amount of lines. Setting the value of the current piece to zero.'''
			set_color(boardcopy, l + displacement, c, get_color(boardcopy, l, c))
			set_color(boardcopy, l, c, get_no_color())
	return clusterindex, boardcopy


def concatenate_columns(boardcopy, lines, columns):
	displacement = 0
	for c in range(columns):
		if boardcopy[lines - 1][c] == 0:
			displacement += 1
		elif displacement > 0:
			for l in range(lines):
				boardcopy[l][c - displacement] = boardcopy[l][c]
				boardcopy[l][c] = 0
	return boardcopy


def board_remove_group(board, group):
	lines = len(board)
	columns = len(board[0])
	boardcopy = []
	for line in board:
		boardcopy.append(list(line))
	cluster = group
	cluster.sort(key=itemgetter(1, 0), reverse=True)
	# Sorts the cluster by column, from right to left and then by line, from top to bottom.
	clusterindex = 0
	while clusterindex < len(cluster):
		clusterindex, boardcopy = concatenate_lines(boardcopy, cluster, clusterindex, lines)
	boardcopy = concatenate_columns(boardcopy, lines, columns)
	return boardcopy

class sg_state:
	__slots__ = ['board']
	
	def __init__(self, board):
		self.board = board

	def update_board(self, newboard):
		self.board = newboard

	def get_board(self):
		return self.board

	def __lt__(self, other_sg_state):
		thisclusters = len(board_find_groups(self.get_board()))
		otherclusters = len(board_find_groups(other_sg_state.get_board()))
		return thisclusters < otherclusters


class same_game(Problem):
	__slots__ = ['lines', 'columns']

	def __init__(self, board):
		self.lines = len(board)
		self.columns = len(board[1])
		initialstate = sg_state(board)
		super(same_game, self).__init__(initialstate)
	
	def actions(self, state):
		board = state.get_board()
		return board_find_valid_groups(board)

	'''Return the state that results from executing the given
	action in the given state. The action must be one of
	self.actions(state).'''
	def result(self, state, action):
		board = state.get_board()
		resultingboard = board_remove_group(board, action)
		return sg_state(resultingboard)

	'''Return True if the state is a goal. The default method compares the
	state to self.goal or checks for state in self.goal if it is a
	list, as specified in the constructor. Override this method if
	checking against a single self.goal is not enough.'''
	def goal_test(self, state):
		board = state.get_board()
		if board[self.lines - 1][0] != 0:
			return False
		return True

	def path_cost(self, c, state1, action, state2):
		return c + 1

	def h(self, node):
		board = node.state.get_board()
		coloredballs = 0
		for i in range(self.lines):
			for j in range(self.columns):
				if board[i][j] != 0:
					coloredballs += 1
		return coloredballs
