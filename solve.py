# -*- coding: utf-8 -*-

__author__ = 'Damir'

from itertools import imap

from avl_tree import AVLTree


ALL_XS = set()
TREE_COUNTER = 0


def get_A_B(x1, y1, x2, y2):

    if x1 == x2:
        return 'undf', 'undf'

    x1 = float(x1)
    x2 = float(x2)
    y1 = float(y1)
    y2 = float(y2)

    if not x1:
        b = y1
        a = (y2-b)/x2
    elif not x2:
        b = y2
        a = (y1-b)/x1
    else:
        x_diff = x1/x2
        b = (y1-x_diff*y2)/(1-x_diff)
        a = (y1-b)/x1
    return a, b


def calc_Y(x, a, b):
    x = float(x)
    a = float(a)
    b = float(b)
    return a*x+b


ALL_COORDINATES = []


def coord_processing(pol_id, icoords):
    # Polygon has 3 coords in minimum
    prev, next = icoords.next(), icoords.next()
    print prev, next
    first = prev
    while next:

        if prev[0] < next[0]:
            c = {
                'x1': prev[0],
                'y1': prev[1],
                'x2': next[0],
                'y2': next[1],
                'pol_id': pol_id,
            }
            ALL_XS.add(prev[0])
        elif prev[0] > next[0]:
            c = {
                'x1': next[0],
                'y1': next[1],
                'x2': prev[0],
                'y2': prev[1],
                'pol_id': pol_id,
            }
            ALL_XS.add(next[0])
        else:
            print 'Warning, pol_id={0} has vertical line'.format(pol_id)

        ALL_COORDINATES.append(c)


def get_coordinates():
    with open('C:\Users\Damir\Projects\polygon.txt') as f:
        line = f.readline()
        # fixme каретка разделитель
        pol_id, other_id, line_co = line.split('\t', 2)

        icoords = map(lambda x: x.split(), line_co.split(','))
        print icoords
        coord_processing(pol_id, icoords)


class Node2(object):

    def __init__(self, x1, y1, x2, y2, pol_id, a=None, b=None):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.pol_id = pol_id

        if a is None and b is None:
            self.a, self.b = get_A_B(x1, y1, x2, y2)


if __name__ == "__main__":
    pass
    # a, b = linear_func(0.5, 2, 1, 1)
    # y = calc_Y(a,b,3)
    # print y

    get_coordinates()
