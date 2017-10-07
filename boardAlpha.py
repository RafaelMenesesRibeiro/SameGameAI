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

	def populate_board(self):
		print('Populating game board...')
		for l in range(self.__columns):
			for c in range(self.__lines):
				color = random.randint(1, self.__colorsNumber)
				self.__boardMatrix[l][c] = color
		print('Done')

	#Calculates the adjacent coordinates to the given root (line, column).
	#Only returns the ones that are valid (inside the board).
	def get_adjacent_coordinates(line, column):
		#Starts the list as empty.
		adjacent = []
		#Calculates the board borders to check if a piece is inside the board.
		bottomBorder = this.__lines - 1
		topBorder = 0
		leftBorder = 0
		rightBorder = this.__columns - 1
		#For each adjacent coordiante, chacks if it is valid.
		for adj in [(line-1, column), (line+1, column), (line, column-1), (line, column+1)]:
			if adj[1] < bottomBorder and adj[1] >= topBorder and adj[0] < rightBorder and adj[0] >= leftBorder:
				#If it is inside the board, adds it to the list.
				adjacent.append(adj)
		#Returns the list of adjacent valid coordinates.
		return adjacent

	#Traverses the matrix as a DFS to find all the adjacent pieces with the same
	#color as the root in the board, starting in the given root's coordinates.
	def root_find_group(self, visited, rootLine, rootColumn):
		#Marks the root piece as visited.
		visited[rootLine][rootColumn] = True
		#Gets a reference to the matrix to check the colors of the adjacent
		#pieces.
		board = this.__boardMatrix
		#Starts the cluster with just the root piece.
		cluster = [(rootLine, rootColumn)]
		#Starts the queue with just the root piece.
		queue = [(rootLine, rootColumn)]
		#Gets the root color so it doens't need to access the matrix even more
		#times.
		rootColor = board[rootLine][rootColumn]
		while len(queue) > 0:
			#Removes a piece from the list.
			nextPos = queue.pop()
			#Gets the board coordinates of the piece.
			line = nextPos[0]
			column = nextPos[1]
			#Gets the adjacent coordinates of the current one.
			adjacentBalls = get_adjacent_coordinates(line, column)
			#For each adjacent coordinate checks if it meets the requirements
			#to be added to the cluster.
			for pos in adjacentBalls:
				#Gets the adjacent coordinates.
				l = pos[0]
				c = pos[1]
				#Checks if the coordinate is not empty.
				#If it is not, checks if the coordinate's piece is the same
				#color as the root piece.
				if visited[l][c] == False and board[l][c] == rootColor:
					#In case the requirements are met, adds the adjacent piece
					#to the cluster and to the queue, so its adjacent pieces
					#can be added to the cluster (if the conditions are met).
					cluster.append((l, c))
					queue.append((l, c))
					#Sets the visitation flag to True so it doens't get added
					#again.
					visited[l][c] = True
		#Returns the list of coordinates that are adjacent to each other and
		#are the same color as the root.
		return cluster

	def board_find_groups(self):
		lines = this.__lines
		columns = this.__columns
		#Creates the matrix that represents if a position has been checked for
		#or has been added to a cluster. Initiates all to False because no
		#position was visited yet.
		visited = [[False for _ in range(columns)] for _ in range(lines)]
		#Creates the empty list of clusters.
		clusters = []
		#For each valid (non empty) position on the board, gets its cluster.
		for i in range(lines):
			for j in range(columns):
				#Checks if the current position in empty and if it is, checks
				#if the position was already visited (in a previous BFS).
				if this.__boardMatrix[i][j] != 0 and visited[i][j] == False:
					#Gets the cluster of which the ball in the current position
					#belongs to.
					newCluster = root_find_group(visited, i, j)
					#Adds the newly found cluster to the cluster list.
					clusters.append(newCluster)
		#Returns all the clusters on the board.
		return clusters

	def column_remove_holes(self, boardcopy, cluster, clusterInd):
		boardLines = self.__lines
		displacementVertical = 0
		clusterIndex = clusterInd
		currentColumn = cluster[clusterIndex].get_column()
		#For each line lowers it to the lowest empty space in the same column.
		for currentLine in reversed(range(boardLines)):
			#Checks if there is even more holes. OutOfBounds exception would
			#occour otherwise.
			#Checks if the current position is empty.
			if clusterIndex < len(cluster) and currentLine == cluster[clusterIndex].get_line() and currentColumn == cluster[clusterIndex].get_column():
				#If it is, increments the vertical displacement counter(so the 
				#pieces aboves it get lowered the same amount as there are 
				#holes beneath them) and the clusterIndex variable, because the
				#hole above (not necessarily immediately above, and not necessarily
				#existant), will have the coordinates of the next position in the 
				#removed cluster list (because the list is ordered by column
				#(from right to left) and by line (from the bottom to the top).
				displacementVertical += 1
				clusterIndex += 1
				#Sets the board value of the hole to 0.
				boardcopy[currentLine][currentColumn] = 0
			#If it's not empty, it's a valid game piece.
			else:
				#Checks if the game piece has holes beneath it (represented by
				#the displacementVertical variable that is incremented each time
				#a hole in the column is found starting at the bottom, so if
				#holes were found, they are beneath the current piece.)
				if displacementVertical > 0:
					#If there is, lowers the piece the same amount of columns as
					#there are holes beneath it.
					currentPiece = boardcopy[currentLine][currentColumn]
					boardcopy[currentLine + displacementVertical][currentColumn] = currentPiece
					#Sets the value of the fallen piece to 0.
					boardcopy[currentLine][currentColumn] = 0
				else:
					continue #If there isn't, continue.
		return clusterIndex, boardcopy

	def board_remove_group(self, group):
		boardcopy = []
		for line in self.__boardMatrix:
			boardcopy.append(list(line))
		cluster = group().get_cluster()
		#Sorts the cluster by column, from rigth to left, and then by line,
		#from top to bottom.
		cluster.sort(key=itemgetter(1, 0), reverse=True)

		clusterIndex = 0
		while clusterIndex < len(cluster):
			clusterIndex, boardcopy = column_remove_holes(boardcopy, cluster, clusterIndex)
		return boardcopy

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

