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

	def board_find_groups(self):
		# TODO
		pass

	def board_remove_group(self, group):
		boardcopy = []
		for line in self.__boardMatrix:
			boardcopy.append(list(line))
		cluster = group().get_cluster()
		#Sorts the cluster by column, from rigth to left, and then by line,
		#from top to bottom.
		cluster.sort(key=itemgetter(2, 1), reverse=True)

		clusterIndex = 0
		while clusterIndex < len(cluster):
			clusterIndex, boardcopy = column_remove_holes(boardcopy, cluster, clusterIndex)
		return boardcopy
#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------
	#THE CLUSTER VECTOR NEEDS TO BE ORDERED FROM RIGHT TO LEFT AND BOTTOM UP
	#CONSIDERING THE TOP LEFT CORNER IS (0, 0).
#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------
	def column_remove_holes(self, boardcopy, cluster, clusterInd):
		boardLines = self.__lines
		displacementVertical = 0
		clusterIndex = clusterInd
		currentColumn = cluster[clusterIndex].get_column()

		#For each line lowers it to the lowest empty space in the same column.
		for currentLine in range(boardLines):
			#Checks if there is even more holes. OutOfBounds exception would
			#occour otherwise.
			#Checks if the current position is empty.
			if clusterIndex < clusterLen and currentLine == cluster[clusterIndex].get_line() and currentColumn == cluster[clusterIndex].get_column():
				#If it is, increments the vertical displacement counter(so the 
				#pieces aboves it get lowered the same amount as there are 
				#holes beneath them) and the clusterIndex variable, because the
				#hole above (not necessarily immediately above, and not necessarily
				#existant), will have the coordinates of the next position in the 
				#removed cluster list (because the list is ordered by column
				#(from right to left) and by line (from the bottom to the top).
				displacementVertical += 1
				clusterIndex += 1
				continue

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
					pass
				else:
					#If there isn't, continue.
					continue		
		return clusterIndex, boardcopy

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

