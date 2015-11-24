# -*- coding: utf-8 -*-

__author__ = 'Damir'

from itertools import imap
from operator import itemgetter

from avl_tree import AVLTree


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

ALL_XS = list()
ALL_COORDINATES = list()
SORT_COORDINATES = list()

# runs throughout ALL_XS
stopped = 0


def coord_processing(pol_id, icoords):
    """
        записывает список координат вида
        {'x1': , 'y1': , 'x2': , 'y2': , pol_id': , }
    """
    local_xs = set()

    # Polygon has 3 coords in minimum
    prev, next = icoords.next(), icoords.next()

    while next:
        p_x = float(prev[0])
        p_y = float(prev[1])
        n_x = float(next[0])
        n_y = float(next[1])
        if p_x < n_x:
            c = {
                'x1': p_x,
                'y1': p_y,
                'x2': n_x,
                'y2': n_y,
            }
        elif p_x > n_x:
            c = {
                'x1': n_x,
                'y1': n_y,
                'x2': p_x,
                'y2': p_y,
            }
        else:
            print 'Warning, pol_id={0} has vertical line'.format(pol_id)
            raise Exception()

        c['a'], c['b'] = get_A_B(**c)
        c['pol_id'] = pol_id

        try:
            prev = next
            next = icoords.next()
        except StopIteration:
            next = None

        ALL_COORDINATES.append(c)


def get_coordinates():
    """
        из файла читаем строки
    """
    with open('C:\Python27\helperFiles\simple_coords') as f:
        for line in f.readlines():
            pol_id, other_id, line_co = line.split(' ', 2)
            icoords = imap(lambda x: x.split(), line_co.split(','))
            coord_processing(pol_id, icoords)
            break


def sort_coordinates():
    """
        сортируем все координаты по х1
    """
    global SORT_COORDINATES
    SORT_COORDINATES = sorted(ALL_COORDINATES, key=itemgetter('x1'))


def sort_tree_nodes(nodes, x_middle, n_x):

    global to_dels
    to_dels = []
    # если х2 совпадает с n_x, то на удаление
    for n in nodes:
        n['val'] = calc_Y(x_middle, n['a'], n['b'])
        # del n['x1']
        # del n['y1']

        if n['x2'] == n_x:
            to_dels.append(n['val'])
            n['del'] = True
        # del n['x2']

    return sorted(nodes, key=itemgetter('val'))

# списки на удаление
to_dels = []


def build_first_tree():
    global stopped

    first = SORT_COORDINATES[stopped]
    first_x = float(first['x1'])
    nodes = [first, ]
    stopped += 1
    next = SORT_COORDINATES[stopped]

    n_x = float(next['x1'])
    while n_x == first_x:
        nodes.append(next)
        stopped += 1
        next = SORT_COORDINATES[stopped]
        n_x = float(next['x1'])

    x_middle = (n_x+first_x)/2

    # сортируем ноды
    nodes = sort_tree_nodes(nodes, x_middle, n_x)

    # строим дерево
    tree = AVLTree()
    for n in nodes:
        tree.add(tree.root, n['val'], n['a'], n['b'], n['pol_id'])
    tree.show()
    ref_to_tree = tree

    # первое дерево
    ALL_XS.append([first_x, ref_to_tree])
    # следующее значение Х
    ALL_XS.append([n_x, None])


def build_queue_tree():
    global stopped
    # stopped += 1
    next = SORT_COORDINATES[stopped]

    curr_x = ALL_XS[-1][0]
    prev_tree = ALL_XS[-2][1]
    nodes = []

    n_x = float(next['x1'])
    while n_x == curr_x:
        nodes.append(next)
        stopped += 1
        next = SORT_COORDINATES[stopped]
        n_x = float(next['x1'])

    x_middle = (n_x+curr_x)/2

    # сортируем ноды

    deleting = to_dels
    print deleting
    nodes = sort_tree_nodes(nodes, x_middle, n_x)

    tree = AVLTree()
    for n in nodes:
        tree.add(tree.root, n['val'], n['a'], n['b'], n['pol_id'])
    print to_dels
    tree.show()
    ref_to_tree = tree
    # первое дерево
    ALL_XS[-1][1] = ref_to_tree
    # следующее значение Х
    ALL_XS.append([n_x, None])


if __name__ == "__main__":
    pass
    # a, b = linear_func(0.5, 2, 1, 1)
    # y = calc_Y(a,b,3)
    # print y

    get_coordinates()
    sort_coordinates()
    # for c in SORT_COORDINATES:
    #     print c

    build_first_tree()

    build_queue_tree()
