# -*- coding: utf-8 -*-

import os
from itertools import imap
from operator import itemgetter

from avl_tree import AVLTree
from helpers import (treatment_add_del, find_polygon, l, calc_Y, get_row_dict,
                     )


ALL_XS = [[-181, AVLTree()], ]

# runs throughout ALL_XS
# stopped = 0


# def get_coordinates():
#     """
#         из файла читаем строки
#     """
#     file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'simple_coords2')
#
#     with open(file_path) as f:
#         for line in f.readlines():
#             if not line.startswith('#'):
#                 pol_id, other_id, line_co = line.split(' ', 2)
#                 icoords = imap(lambda x: x.split(), line_co.split(','))
#                 coord_processing(pol_id, icoords)


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


def process_tree(row, main_file, err_del_nodes, del_nodes):

    # находим ноды для нового дерева
    row_x = row['x1']
    row_float = float(row_x)

    try:
        next_line = main_file.next()
        next_row = get_row_dict(next_line)
        next_float = float(next_row['x1'])
    except StopIteration:
            return None

    add_nodes = [row, ]

    while next_float == row_float:
        add_nodes.append(next_row)
        try:
            next_line = main_file.next()
            next_row = get_row_dict(next_line)
            next_float = float(next_row['x1'])
        except StopIteration:
            return None

    x_middle = (next_float + row_float) / 2
    prev_tree = ALL_XS[-1][1]
    prev_tree = AVLTree()

    next_tree = AVLTree()

    # удаляем ноды битые, у которых х2 меньше, чем следующий х1
    for err_d in err_del_nodes:
        next_tree.delete_versionly(prev_tree, err_d['val'])

    err_del_nodes = [node for node in add_nodes if float(node['x2']) < next_float]
    if err_del_nodes:
        print 'Err_del_nodes exists', err_del_nodes

    # обработка нодов на добавление/удаление
    to_replace, proc_add, proc_del = treatment_add_del(del_nodes, add_nodes)

    for (d, a) in to_replace:
        next_tree.replace_versionly(prev_tree, d['val'], a)



    # актуализируем все значения нодов в дереве
    # prev_tree.update_vals(x_middle)





    ALL_XS.append([row_x, None])

    # print 'prev_tree', prev_tree
    # print 'nodes', map(lambda x: x['x1'], nodes)
    # print 'nodes x2s', map(lambda x: float(x['x2']), nodes)
    # print 'next_x1_float', next_float

    # ноды будут удалены в след дереве
    # delete_for_next = [node for node in add_nodes if float(node['x2']) <= next_float]

    # print 'to_delete', map(lambda x: x['x1'], to_delete)











    return next_row

    # if not nodes:
    #     raise Exception('Nodes is empty, HOLE!')
    #
    # x_middle = (n_x+curr_x)/2
    # global deletions
    # to_delete = deletions
    #
    # # обрабатываем ноды будущего дерева
    # deletions, to_add = process_tree_nodes(nodes, x_middle, n_x)
    #
    #
    #
    # if not prev_tree:
    #     tree = AVLTree()
    #     for n in to_add:
    #         tree.add(tree.root, n['val'], n['a'], n['b'], n['pol_id'])
    #     # tree.show()
    #     ref_to_tree = tree
    # else:
    #
    #     next_tree = AVLTree()
    #
    #     print 'to_delete', to_delete
    #     print 'to_add', to_add
    #
    #     process_add_del(to_delete, to_add, next_tree, prev_tree)
    #
    #     # обновляем все значения в нодах
    #     next_tree.update_vals(next_tree.root, x_middle)
    #     # обнуляем флаги updates
    #     next_tree.remove_update_flags(next_tree.root)
    #
    #     # процесс перестраивания дерева
    #     ref_to_tree = next_tree
    #     # next_tree.show()
    #
    # ALL_XS[-1][1] = ref_to_tree
    # # следующее значение Х
    # ALL_XS.append([n_x, None])
    #
    # return n_x if not is_end else None


if __name__ == "__main__":

    file_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), 'outer_sort', 'cut')

    with open(file_path) as main_file:
        line = main_file.next()
        row = get_row_dict(line)

        new_row = process_tree(row, main_file, [])

        # print new_row

        while new_row is not None:
            new_row = process_tree(new_row, main_file, [])
            # print new_row


    # print 'next_x1', next_x1
    # next_x1 = process_tree()
    # print 'next_x1', next_x1
    # # while next_x1 is not None:
    # next_x1 = process_tree()

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

    # avl = AVLTree()
    # left rotate
    # x = [1,2,]  # 3
    # x = [5,1,7,6,8,]  # add 9 (avl2.ADD_versionly(avl, 9))
    # x = [2,1,3,4,]  # 5
    # x = [3,2,5,4,6,]  # 7
    # x = [4,2,6,1,3,5,8,7,9]  # 10
    # x = [2,1,3,4,]  # 5
    # x = [2,1,5,3,6]  # 4
    # x = [4,2,8,1,3,6,10,5,7,9,11,]  # 12

    # big left rotate
    # x = [1,3]  # 2
    # x = [2,1,3,5,]  # 4
    # x = [2,1,6,4,7]  # 5
    # x = [4,1,5,3]  # 2
    # x = [3,1,7,2,4,9,3.5,5,8,10,]  # 6
    # x = [3,1,7,2,4,9,3.5,5,8,10,]  # 3.7

    # right rotate
    # x = [3,2]  # 1
    # x = [5,3,6,2,4,]  # 1
    # x = [6,4,7,3,5,8,2,]  # 1
    # x = [-4,-2,-6,-1,-3,-5,-8,-7,-9]  # -10
    # x = [3,1,7,2,4,9,3.5,5,]  # 3.7

    # big right rotate
    # x = [3,1]  # 2
    # x = [2,1,5,3,]  # 4
    # x = [3,1,7,2,4,9,3.5,5,]  # 6

    # get_node
    # x = [2,1,3]
    # x = [1,]
    # x = []

    # delete versionly
    # left rotate
    # x = [5,1,7,6,8,]  # del 1
    # x = [2,1,4,3,5]  # del 1
    # x = [3,2,5,1,4,7,6,8]  # del 4


    # big left rotate
    # x = [2,1,4,3]  # del 1

    # right rotate
    # x = [3,2,4,1]  # 4

    # big right rotate
    # x = [3,1,4,2]  # 4
    # x = [6,4,7,2,5,8,3]  # 5
    # x = [-3,-1,-7,-2,-5,-9,-4,-6]  # -2

    # state of node to delete
    # has l, no r
    # x = [2,1,4,3]  # 4
    # x = [3,2,4,1]  # 1
    # has r, no l
    # x = [3,1,4,2]  # 1
    # x = [5,3,10,2,4,8,11,1,6,9,12,6,7]  # 4
    # x = [5,2,10,1,4,8,11,3,6,9,12,6,7]  # 1
    # has r, has l
    # x = [2,1,3]  # 2
    # x = [4,2,5,1,3,6]  # 2

    # for i in x:
    #     avl.add(avl.root, i)
    # l()
    # avl.show()
    #
    # avl2 = AVLTree()
    #
    # avl2.delete_versionly(avl, 2)

    # avl2.add_versionly(avl, 12)
    # print avl2.get_node_versionly(avl, 1)
    # l()
    # avl.show()
    # l()
    # avl2.show()
    # import os
    # print os.path.dirname(__file__)
    # print dir(__file__)
