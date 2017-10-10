from operator import itemgetter
import random

# ---------------------------------------------------------------------------------------------------------------------#
#                                                GLOBAL VARIABLES
# ---------------------------------------------------------------------------------------------------------------------#

clusterAux = []
clusterList = []

board = []
liness = 0
columns = 0
colorsnumber = 0

# ---------------------------------------------------------------------------------------------------------------------#
#                                                TAD BOARD
# ---------------------------------------------------------------------------------------------------------------------#


# ---------------------------------------------------------------------------------------------------------------------#
#                                                TAD GROUP
# ---------------------------------------------------------------------------------------------------------------------#

def reset_cluster():
    clusterAux.clear()


def new_cluster(c):
    if is_cluster(c):
        clusterList.append(c)
        reset_cluster()
    else:
        raise ValueError("new_cluster: invalid arguments")


def cluster_add_pos(p):
    if pos_has_color(p):
        clusterAux.append(p)
    else:
        raise ValueError("cluster_add_pos: invalid arguments")


def is_cluster(c):
    if len(c) < 2:
        return False
    else:
        clustercolor = pos_color(c[1])
        for p in c:
            positionscolor = pos_color(c[p])
            if eq_colors(positionscolor, clustercolor):
                continue
            else:
                return False
    return True

#----------------------------------------------------------------------------------------------------------------------#
#                                                TAD POSITION
# ---------------------------------------------------------------------------------------------------------------------#


def make_pos(l, c):
    if not (isinstance(l, int) and l > 0 and isinstance(c, int) and c > 0):
        raise ValueError("new_position: invalid arguments")
    return (l, c)


def pos_l(p):
    if is_pos(p):
        return p[0]
    return


def pos_c(p):
    if is_pos(p):
        return p[1]
    return


def pos_color(p):
    if is_pos(p):
        return board[pos_l(p)][pos_c(p)]
    else:
        raise ValueError("get_color: invalid position")


def pos_has_color(p):
    if is_pos(p):
        poscolor = pos_color(p)
        return color(poscolor)
    else:
        raise ValueError("pos_has_color: invalid position")


def is_pos(p):
    if isinstance(p, tuple) and len(p) == 2:
        return isinstance(p[0], int) and p[0] > 0 and isinstance(p[1], int) and p[1] > 0
    return False


def eq_pos(p1, p2):
    if is_pos(p1) and is_pos(p2):
        if pos_l(p1) == pos_l(p2) and pos_c(p1) == pos_c(p2):
            return True
    return False

# ---------------------------------------------------------------------------------------------------------------------#
#                                                TAD COLOR
# ---------------------------------------------------------------------------------------------------------------------#


def set_color(l, c, k):
    p = make_pos(l, c)
    if is_pos(p) and (no_color(k) or color(k)):
        board[pos_l()][pos_c()] = k
    else:
        raise ValueError("set_color: at least one argument is invalid")


def no_color(c):
    return c == 0


def color(c):
    return c > 0


def eq_colors(c1, c2):
    if color(c1) and color(c2):
        return c1 == c2
    else:
        raise ValueError("equal_color: at least one argument is not color")

# ---------------------------------------------------------------------------------------------------------------------#
#                                                CLASS SGSTATE
# ---------------------------------------------------------------------------------------------------------------------#


class sg_state:
    __slots__ = ['__board']

    def __init__(self, b):
        self.__board = b

    def update_board(self, nb):
        self.__board = nb

    def __lt__(self, other_sg_state):
        # TODO compares another sg_state with the current one and returns true if this one is less than other
        pass

# ---------------------------------------------------------------------------------------------------------------------#
#                                                CLASS SAMEGAME
# ---------------------------------------------------------------------------------------------------------------------#
