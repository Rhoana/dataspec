'''boundingbox.py - a 2D bounding box for the extent of a tile or similar'''


class BoundingBox(object):
    def __init__(self, x0, x1, y0, y1):
        '''Initialize the bounding box

        :param x0: the leftmost coordinate
        :param x1: the rightmost coordinate
        :param y0: the topmost coordinate
        :param y1: the bottommost coordinate
        '''
        self.__x0 = x0
        self.__x1 = x1
        self.__y0 = y0
        self.__y1 = y1

    @property
    def x0(self):
        return self.__x0

    @property
    def x1(self):
        return self.__x1

    @property
    def y0(self):
        return self.__y0

    @property
    def y1(self):
        return self.__y1

    @property
    def width(self):
        return self.x1 - self.x0

    @property
    def height(self):
        return self.y1 - self.y0
