# -*- coding: utf-8 -*-

from itertools import groupby, izip_longest
from operator import itemgetter
from collections import Counter


def l():
    print 80*'-'+'\n\n\n'


def replace_node_val(next_tree, del_val, new_info):
    node = next_tree.get_node(next_tree.root, del_val)
    if not node.pid1_filled:
        node.a = new_info['a']
        node.b = new_info['b']
        node.pid1 = new_info['pol_id']
        node.pid1_filled = True
    else:
        node.pid2 = new_info['pol_id']


def create_node_branch(next_tree, del_val, new_info, prev_tree):
    next_tree.create_node_branch(del_val, new_info, prev_tree)


def process_add_del(to_del, to_add, next_tree, prev_tree):

    # del/add pairs
    pairs = []

    del_dict = {}
    add_dict = {}

    for k, gr in groupby(sorted(to_del, key=itemgetter('val')), lambda x: x['y2']):
        del_dict[k] = list(gr)

    for k, gr in groupby(sorted(to_add, key=itemgetter('val')), lambda x: x['y1']):
        add_dict[k] = list(gr)

    print 'del_dict', del_dict
    print 'add_dict', add_dict

    for k in del_dict:
        pairs.append((del_dict[k], add_dict.get(k, [])))

        # add_dict.pop(k, None)

    # finals
    f_del = []  # deletions without pair to replace
    f_add = []  # addition without pair to replace

    print 'pairs', pairs

    for pair in pairs:
        d, a = pair

        for i_pair in izip_longest(d, a):
            # пара (на удаление, на добавление вместо удаленного)
            i_d, i_a = i_pair
            if i_d and i_a:
                # replace_node_val(next_tree, first['val'], second)
                create_node_branch(next_tree, i_d['val'], i_a, prev_tree)
                print prev_tree
                prev_tree.show()
                print next_tree
                next_tree.show()
            else:
                f_del.append(i_d) if i_d else f_add.append(i_a)

    print 80*'-'
    print 'deletions without pair to replace'
    print f_del
    print 'addition without pair to replace'
    print f_add

    # удаляем сразу по 2 значения
    for v, gr in groupby(f_del, lambda x: x['val']):
        # pol_ids = [g['pol_id'] for g in gr]
        next_tree.delete(v)


def find_polygon(root, came_x, came_y):
    less, more = None, None
    if root is None:
        print 'No {0} element in Tree'.format(came_y)
    elif root.val is None:
        print 'Tree is empty!'
    else:
        child = root
        while child:
            r_v = child.calc_new_val(came_x)
            if r_v == came_y:
                return child, child
            elif r_v < came_y:
                less = child
                child = child.right
            elif r_v > came_y:
                more = child
                child = child.left
    print less, more
    if not less and not more:
        pass
    elif less and more:
        # fixme достаю 2 одинаковых
        ids = [less.pid1, less.pid2, more.pid1, more.pid2]
        print ids
        return max(Counter(ids))
    else:
        print 'Out of territory'
        return None
