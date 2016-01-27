# -*- coding: utf-8 -*-


import os
from itertools import imap
from operator import itemgetter

from copy import deepcopy
from avl_tree import AVLTree
from simple_helpers import (process_add_del, find_polygon, l)


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
    file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'simple_coords2')

    with open(file_path) as f:
        for line in f.readlines():
            if not line.startswith('#'):
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
    # global deletions
    to_delete = []
    # если х2 совпадает с n_x, то на удаление
    for n in nodes:
        n['val'] = calc_Y(x_middle, n['a'], n['b'])

        if n['x2'] == n_x:
            to_delete.append({
                'val': n['val'], 'y2': n['y2'], 'pol_id': n['pol_id'], })

    return sorted(to_delete, key=itemgetter('val')), sorted(nodes, key=itemgetter('val'))

# списки на удаление, элемент состоит из val и y2
# будем группировать по y2
deletions = []


def process_tree():
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
        raise Exception('Nodes is empty, HOLE!')

    x_middle = (n_x+curr_x)/2
    global deletions
    to_delete = deletions

    # обрабатываем ноды будущего дерева
    deletions, to_add = process_tree_nodes(nodes, x_middle, n_x)



    if not prev_tree:
        tree = AVLTree()
        for n in to_add:
            tree.add(tree.root, n['val'], n['a'], n['b'], n['pol_id'])
        # tree.show()
        ref_to_tree = tree
    else:

        next_tree = AVLTree()

        print 'to_delete', to_delete
        print 'to_add', to_add

        process_add_del(to_delete, to_add, next_tree, prev_tree)

        # обновляем все значения в нодах
        next_tree.update_vals(next_tree.root, x_middle)
        # обнуляем флаги updates
        next_tree.remove_update_flags(next_tree.root)

        # процесс перестраивания дерева
        ref_to_tree = next_tree
        # next_tree.show()

    ALL_XS[-1][1] = ref_to_tree
    # следующее значение Х
    ALL_XS.append([n_x, None])

    return n_x if not is_end else None


if __name__ == "__main__":
    # # достаем коорды
    # get_coordinates()
    # # сортируем коорды
    # sort_coordinates()
    # set_first_to_xs()
    # all_coords_len = len(SORTED_COORDINATES)

    # пока не достигли конца строим деревья
    # next_x1 = process_tree()
    # print 'next_x1', next_x1
    # next_x1 = process_tree()
    # print 'next_x1', next_x1
    # while next_x1 is not None:
    #     next_x1 = process_tree()

    # print ALL_XS
    # second_tree = ALL_XS[1][1]
    # second_tree.show()
    # pol_id = find_polygon(second_tree.root, 1.5, 1.4)
    # print pol_id
    # second_tree.show()

    # l()
    #
    # avl = AVLTree([4, 3, 5, 2])
    # avl.show()
    # l()
    #
    # avl.add(avl.root, 1)
    # avl.show()
    # l()

    avl = AVLTree()
    # left rotate
    # x = [1,2,]
    # x = [5,1,7,6,8,]  # add 9 (avl2.ADD_versionly(avl, 9))
    # x = [2,1,3,4,]  # 5
    # x = [3,2,5,4,6,]  # 7
    # x = [4,2,6,1,3,5,8,7,9]  # 10
    # x = [2,1,3,4,]  # 5
    x = [2,1,5,3,6]  # 4
    # big left rotate
    # x = [1,3]  # 2
    # x = [2,1,3,5,]  # 4
    # x = [2,1,6,4,7]  # 5
    # x = [4,1,5,3]  # 2
    # x = [3,1,7,2,4,9,3.5,5,8,10,]  # 6
    x = [3,1,7,2,4,9,3.5,5,8,10,]  # 3.7


    # big right rotate
    # x = [2,1,6,4,]  # 5

    for i in x:
        avl.add(avl.root, i)
    l()
    avl.show()

    avl2 = AVLTree()
    avl2.add_versionly(avl, 3.7)
    l()
    avl2.show()

    # l()
    # avl3 = AVLTree()
    # avl3.replace_create_node_branch(5, '3new_val3', avl2)
    # l()
    # avl3.show()








