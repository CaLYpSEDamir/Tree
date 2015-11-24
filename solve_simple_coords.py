# -*- coding: utf-8 -*-

__author__ = 'Damir'

import os
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
SORTED_COORDINATES = list()

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

    file_path = 'C:\Python27\helperFiles\simple_coords'
    if not os.path.isfile(file_path):
        file_path = '/home/damir/Projects/Tree/simple_coords'

    with open(file_path) as f:
        for line in f.readlines():
            pol_id, other_id, line_co = line.split(' ', 2)
            icoords = imap(lambda x: x.split(), line_co.split(','))
            coord_processing(pol_id, icoords)


def sort_coordinates():
    """
        сортируем все координаты по х1
        fixme needs outsort
    """
    global SORTED_COORDINATES
    SORTED_COORDINATES = sorted(ALL_COORDINATES, key=itemgetter('x1'))


def set_first_to_xs():
    """
        Записываем первый x в список X-ов
    """
    first = SORTED_COORDINATES[0]
    first_x = float(first['x1'])
    ALL_XS.append([first_x, None])


def process_tree_nodes(nodes, x_middle, n_x):
    """
        Определяем val ноды, определяем ноды на удаление,
        сортируем по val
    """
    global deletions
    deletions = []
    # если х2 совпадает с n_x, то на удаление
    for n in nodes:
        n['val'] = calc_Y(x_middle, n['a'], n['b'])
        # del n['x1']
        # del n['y1']

        if n['x2'] == n_x:
            deletions.append({'val': n['val'], 'y2': n['y2']})
            n['del'] = True
        # del n['x2']

    return sorted(nodes, key=itemgetter('val'))

# списки на удаление, элемент состоит из val и y2
# будем группировать по y2
deletions = []


def build_first_tree():
    global stopped

    first = SORTED_COORDINATES[stopped]
    first_x = float(first['x1'])
    nodes = [first, ]
    stopped += 1
    next = SORTED_COORDINATES[stopped]

    n_x = float(next['x1'])
    while n_x == first_x:
        nodes.append(next)
        stopped += 1
        next = SORTED_COORDINATES[stopped]
        n_x = float(next['x1'])

    x_middle = (n_x+first_x)/2

    # сортируем ноды
    nodes = process_tree_nodes(nodes, x_middle, n_x)

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


def build_tree():
    global stopped

    curr = SORTED_COORDINATES[stopped]
    curr_x = ALL_XS[-1][0]

    # если деревьев еще не было, то None
    try:
        prev_tree = ALL_XS[-2][1]
    except Exception:
        prev_tree = None

    nodes = []
    n_x = float(curr['x1'])
    is_end = False

    while n_x == curr_x:
        nodes.append(curr)
        stopped += 1
        try:
            curr = SORTED_COORDINATES[stopped]
            n_x = float(curr['x1'])
        except IndexError:
            is_end = True
            # у последнего берем х2 для нахождения x_middle
            n_x = curr['x2']

    if not nodes:
        raise Exception('Nodes is empty, something went wrong!')

    x_middle = (n_x+curr_x)/2

    to_delete = deletions
    print 'to_delete', to_delete

    # обрабатываем ноды будущего дерева
    nodes = process_tree_nodes(nodes, x_middle, n_x)

    print 'to_add'
    for n in nodes:
        print n
    print 90*'-'

    if not prev_tree:
        tree = AVLTree()
        for n in nodes:
            tree.add(tree.root, n['val'], n['a'], n['b'], n['pol_id'])
        tree.show()
        ref_to_tree = tree
    else:
        # процесс перестраивания дерева
        ref_to_tree = prev_tree
        # prev_tree.show()

    ALL_XS[-1][1] = ref_to_tree
    # следующее значение Х
    ALL_XS.append([n_x, None])

    return n_x if not is_end else None


if __name__ == "__main__":

    # a, b = linear_func(0.5, 2, 1, 1)
    # y = calc_Y(a,b,3)
    # print y

    # достаем коорды
    get_coordinates()
    # for i, c in enumerate(ALL_COORDINATES):
    #     print i, c
    # print 90*'-'

    # сортируем коорды
    sort_coordinates()
    # for i, c in enumerate(SORTED_COORDINATES):
    #     print i, c
    # print 90*'-'

    set_first_to_xs()

    all_coords_len = len(SORTED_COORDINATES)

    # пока не достигли конца строим деревья
    next_x1 = build_tree()
    # while next_x1 is not None:
    #     next_x1 = build_tree()
