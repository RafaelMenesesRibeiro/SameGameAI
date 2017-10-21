from operator import itemgetter
from search import *
import time

infinite = float("inf")

#------------------------------------------------------------------------------#
#
#           ADT Color
#
#-----------------------------------------------------------------------------#
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
#           ADT Position
#
#-----------------------------------------------------------------------------#
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
#           ADT Board
#
#-----------------------------------------------------------------------------#
#Calculates the adjacent coordinates to the given root (line, column).
#Only returns the ones that are valid (inside the board).
def get_adjacent_coordinates(l, c, lines, columns):
	adjacentlist = []
	#Calculates the board borders to check if a piece is inside the board.
	bottomborder = lines - 1
	topborder = 0
	leftborder = 0
	rightborder = columns - 1
	#For each adjacent coordinate check its validity.
	for adj in [(l - 1, c), (l + 1, c), (l, c - 1), (l, c + 1)]:
		if bottomborder >= pos_l(adj) >= topborder and rightborder >= pos_c(adj) >= leftborder:
			#If it is inside the board, adds it to the list.
			adjacentlist.append(adj)
	#Returns the list of adjacent valid coordinates.
	return adjacentlist

#Traverses the matrix as a DFS to find all the adjacent pieces with the same
#color as the root in the board, starting in the given root's coordinates.
def root_find_group(board, visited, rootline, rootcolumn, lines, columns):
	#Marks the root piece as visited.
	visited[rootline][rootcolumn] = True
	#Starts the cluster with just the root piece.
	cluster = [(rootline, rootcolumn)]
	#Starts the queue with just the root piece.
	queue = [(rootline, rootcolumn)]
	#Gets the root color so it doens't need to access the matrix even more
	#times.
	rootcolor = get_color(board, rootline, rootcolumn)
	while len(queue) > 0:
		#Removes a piece from the list.
		nextposition = queue.pop()
		#Gets the adjacent coordinates of the current one.
		adjacentballs = get_adjacent_coordinates(pos_l(nextposition), pos_c(nextposition), lines, columns)
		#For each adjacent coordinate checks if it meets the requirements to be 
		#added to the cluster.
		for pos in adjacentballs:
			#Gets the adjacent coordinates.
			l = pos_l(pos)
			c = pos_c(pos)
			#Checks if the coordinate is not empty and if the coordinate's piece
			#is the same color as the root piece.
			if not visited[l][c] and rootcolor == get_color(board, l, c):
				#In case the requirements are met, adds the adjacent piece to
				#the cluster and to the queue.
				cluster.append((l, c))
				queue.append((l, c))
				#Sets the visitation flag to True so it doesnt get added again.
				visited[l][c] = True
	#Returns the list of coordinates that are adjacent to each other and are the
	#same color as the root.
	return cluster

#Traverses the matrix as a DFS to find all groups of adjacent pieces with the
#same color.
def board_find_groups(board, minimumsize=1):
	lines = len(board)
	columns = len(board[0])
	#Creates the array of clusters as empty.
	clusters = []
	#Creates the visited matrix with False. No piece has been visited yet.
	visited = [[False for _ in range(columns)] for _ in range(lines)]
	#For each piece, finds its cluster, if it was not visited yet.
	for l in range(lines):
		for c in range(columns):
			#If the current piece is valid (not empty) has not been visited,
			#finds its cluster.
			if color(get_color(board, l, c)) and not visited[l][c]:
				newcluster = root_find_group(board, visited, l, c, lines, columns)
				#If the minimum size of the cluster is respected, adds to the list.
				if len(newcluster) >= minimumsize:
					clusters.append(newcluster)
	#Returns all the clusters in the board.
	return clusters

#Traverses the matrix as a DFS to mark all the adjacent pieces with the same
#color as the root in the board, starting in the given root's coordinates.
def root_find_number_cluster(board, visited, rootline, rootcolumn, lines, columns):
	#Marks the root piece as visited.
	visited[rootline][rootcolumn] = True
	#Starts the queue with just the root piece.
	queue = [(rootline, rootcolumn)]
	#Gets the root color so it doens't need to access the matrix more times.
	rootcolor = get_color(board, rootline, rootcolumn)
	while len(queue) > 0:
		#Removes a piece from the list.
		nextposition = queue.pop()
		#Gets the adjacent coordinates of the current one.
		adjacentballs = get_adjacent_coordinates(pos_l(nextposition), pos_c(nextposition), lines, columns)
		#For each adjacent coordinate checks if it meets the requirements to be 
		#added to the cluster.
		for pos in adjacentballs:
			#Gets the adjacent coordinates.
			l = pos_l(pos)
			c = pos_c(pos)
			#Checks if the coordinate is not empty and if the coordinate's piece
			#is the same color as the root piece.
			if not visited[l][c] and rootcolor == get_color(board, l, c):
				queue.append((l, c))
				visited[l][c] = True
	#Marks all the pieces of the cluster and returns it found a cluster.
	return 1

#Traverses the matrix as a DFS to find all groups of adjacent pieces with the
#same color.
def board_find_number_groups(board, lines, columns, maximumsize=infinite):
	#Creates the visited matrix with False. No piece has been visited yet.
	visited = [[False for _ in range(columns)] for _ in range(lines)]
	#Initiates the counter at 0.
	counter = 0
	#For each piece, finds its cluster, if it was not visited yet.
	for l in range(lines):
		for c in range(columns):
			if counter > maximumsize:
				return counter
			#If the current piece is valid (not empty) has not been visited,
			#finds the length of its cluster.
			if color(get_color(board, l, c)) and not visited[l][c]:
				counter += root_find_number_cluster(board, visited, l, c, lines, columns)
	#Returns how many clusters are in the board.
	return counter

#Removed all the empty pieces from the column, lowering all the pieces above
#empty spaces.
def concatenate_lines(boardcopy, cluster, index, lines):
	#Initiates the vertical displcament at 0.
	displacement = 0
	clusterindex = index
	#Gets the column in which to remove the empty pieces.
	c = pos_c(cluster[clusterindex])
	#Traverses the lines from the lowest to the highest.
	for l in reversed(range(lines)):
		#If the current piece is empty increments the number of lines the higher
		#pieces need to descend. Gets the next hole coordinates.
		if clusterindex < len(cluster) and l == pos_l(cluster[clusterindex]) and c == pos_c(cluster[clusterindex]):
			displacement += 1
			clusterindex += 1
			#If the current piece is to be removed, marks it as empty.
			set_color(boardcopy, l, c, get_no_color())
		#If the current piece is valid and it needs to be loweres, lowers it
		#to the lowest empty space in the column and empties its current place.
		elif displacement > 0:
			set_color(boardcopy, l + displacement, c, get_color(boardcopy, l, c))
			set_color(boardcopy, l, c, get_no_color())
	#Returns the index of the next piece to remove (because its in the next
	#column) and the altered board.
	return clusterindex, boardcopy

#Removed all the empty columns from the board.
def concatenate_columns(boardcopy, lines, columns):
	#Initiates the horizontal displcament at 0.
	displacement = 0
	#Traverses the columns from the left to the right.
	for c in range(columns):
		#If the column is empty, increments the number of columns the columns to
		#the right need to shift left.
		if boardcopy[lines - 1][c] == 0:
			displacement += 1
		#If the column is not empty and it needs to move left, shifts it.
		elif displacement > 0:
			for l in range(lines):
				boardcopy[l][c - displacement] = boardcopy[l][c]
				boardcopy[l][c] = 0
	#Returns the altered board.
	return boardcopy

#Removes a cluster from the board.
def board_remove_group(board, cluster):
	lines = len(board)
	columns = len(board[0])
	#Copies the board so it doesn't alter the original.
	boardcopy = []
	for line in board:
		boardcopy.append(list(line))
	#Sorts the cluster by descending column and then descending line.
	cluster.sort(key=itemgetter(1, 0), reverse=True)
	clusterindex = 0
	while clusterindex < len(cluster):
		#For each line involved in the cluster to remove, 
		clusterindex, boardcopy = concatenate_lines(boardcopy, cluster, clusterindex, lines)
	#After removing the pieces and concatenating the lines, shifts the empty
	#columns left.
	boardcopy = concatenate_columns(boardcopy, lines, columns)
	return boardcopy

class sg_state:
	__slots__ = ['board', 'lines', 'columns']

	def __init__(self, board):
		self.lines = len(board)
		self.columns = len(board[0])
		self.board = board

	def get_board(self):
		return self.board

	def __lt__(self, other_sg_state):
		thisclustercount = board_find_number_groups(self.get_board(), self.lines, self.columns)
		otherclustercount = board_find_number_groups(other_sg_state.get_board(), self.lines, self.columns, thisclustercount)
		return thisclustercount < otherclustercount

class same_game(Problem):
	__slots__ = ['lines', 'columns']

	def __init__(self, board):
		self.lines = len(board)
		self.columns = len(board[1])
		initialstate = sg_state(board)
		super(same_game, self).__init__(initialstate)

	#Returns the avaliable action in the current state: array of clusters in the
	#board.
	def actions(self, state):
		board = state.get_board()
		return board_find_groups(board, 2)

	#Returns a state which board is the result of removing the cluster (action)
	#from the given state's board.
	def result(self, state, action):
		board = state.get_board()
		resultingboard = board_remove_group(board, action)
		return sg_state(resultingboard)

	#Returns True if the state is a goal.
	def goal_test(self, state):
		board = state.get_board()
		if board[self.lines - 1][0] != 0:
			return False
		return True

	#Returns the cost of the path to the node.
	def path_cost(self, c, state1, action, state2):
		numberremoved = len(action)
		return c + numberremoved

	#Returns the preducted cost to reach the goal state from the given state.
	def h(self, node):
		board = node.state.get_board()
		coloredballs = 0
		for j in range(self.columns):
			if board[self.lines - 1][j] == 0:
				continue
			for i in reversed(range(self.lines)):
				if board[i][j] != 0:
					coloredballs += 1
				else:
					continue
		return coloredballs




def testMethod(method, problem, heuristic=None):
	tstart = time.time()
	if heuristic == None:
		method(problem)
	else:
		method(problem, heuristic)
	tend = time.time()
	executiontime = tend - tstart
	print('{} took {} seconds'.format(method, executiontime))




board = [[3,1,3,2],[1,1,1,3],[1,3,2,1],[1,1,3,3],[3,3,1,2],[2,2,2,2],[3,1,2,3],[2,3,2,3],[5,1,1,3],[4,5,1,2]]
print(board)


game = same_game(board)
method1 = depth_first_tree_search
method2 = astar_search
method3 = best_first_graph_search #Greedy search
testMethod(method1, game)
testMethod(method2, game, game.h)
testMethod(method3, game, game.h)





