class Color:
    __color = 0

    def __init__(self, c):
        self.__color = c

    def get_color(self):
        return self.__color

    def set_color(self, c):
        self.__color = c

    def is_empty(self):
        return self.__color == 0
