class Group:
    __cluster = []

    def __init__(self):
        pass

    def add_pos(self, pos):
        self.__cluster.append(pos)

    def get_cluster(self):
        return self.__cluster

    def is_valid_action(self):
    	return len(self.__cluster) >= 2