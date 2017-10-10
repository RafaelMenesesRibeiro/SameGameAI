class same_game(Problem):
    #Models a Same Game problem as a satisfaction problem.
    #A solution cannot have pieces left on the board.
    def __init__(self, board):
        initialstate = sg_state(board)
        Problem.__init__(self, initialstate)

    '''Return the actions that can be executed in the given
    state. The result would typically be a list, but if there are
    many actions, consider yielding them one at a time in an
    iterator, rather than building them all at once.'''
    def actions(self, state):
        #Gets the board of the state.
        board = state.board
        #Find all the clusters in the board.
        clusters = board.board_find_groups()
        #Trims the clusters to only consider groups of 2 or more pieces.
        validclusters = []
        for cluster in cluster:
            if cluster.is_valid_action():
                validclusters.append(cluster)               
        return validclusters

    '''Return the state that results from executing the given
    action in the given state. The action must be one of
    self.actions(state).'''
    def result(self, state, action):
        #Gets the board of the state.
        board = state.board
        #Gets the cluster to be removed.
        cluster = action
        #Calculates the board that would result in completing the action in the
        #given state.
        resultingboard = board.board_remove_group(cluster)
        return resultingboard

    '''Return True if the state is a goal. The default method compares the
    state to self.goal or checks for state in self.goal if it is a
    list, as specified in the constructor. Override this method if
    checking against a single self.goal is not enough.'''
    def goal_test(self, state):
        #Gets the board of the state.
        board = state.board
        if board.is_empty():
            return True
        return False

    def path_cost(self, c, state1, action, state2):
        '''Return the cost of a solution path that arrives at state2 from
        state1 via action, assuming cost c to get up to state1. If the problem
        is such that the path doesn't matter, this function will only look at
        state2.  If the path does matter, it will consider c and maybe state1
        and action. The default method costs 1 for every step in the path.'''
        return c + 1

    def h(self, node):
        #Needed for informed search.
        pass