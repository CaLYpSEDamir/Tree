# -*- coding: utf-8 -*-
import re
from itertools import groupby, izip_longest
from operator import itemgetter
from collections import Counter


def find_middle_x(x1, x2):
    cut_x1_i = x1.index('.')+11
    cut_x2_i = x2.index('.')+11
    cut_x1, prec_x1 = float(x1[:cut_x1_i]), x1[cut_x1_i:]
    cut_x2, prec_x2 = float(x2[:cut_x2_i]), x1[cut_x2_i:]
    print x1[:cut_x1_i], repr(float(x1[:cut_x1_i]))
    print cut_x1, cut_x2, x2[:cut_x2_i]
    fl_midl = (cut_x1 + cut_x2) / 2
    print fl_midl
    r = re.findall(r'^\d+.\d{0,10}', str(fl_midl))
    q = re.split(r'^\d+.\d{0,10}', str(fl_midl))[1]



    print r,q

    s_midl = str(fl_midl)
    cut_midl_i = s_midl.index('.')+10
    cut_midl = s_midl[:cut_midl_i]
    cut_prec = s_midl[cut_midl_i:]

    if all([prec_x1, prec_x2]):
        l1 = len(prec_x1)
        l2 = len(prec_x2)
        prec_f = int(prec_x1)*(10**(-1)*l1) + int(prec_x2)*(10**(-1)*l2)
    elif prec_x1:
        prec_f = int(prec_x1)*(10**(-1)*len(prec_x1))
    elif prec_x2:
        prec_f = int(prec_x2)*(10**(-1)*len(prec_x2))
    else:
        prec_f = ''

    if cut_prec:
        prec_f += int(cut_prec)*(10**(-1)*len(cut_prec))
    print cut_midl
    print prec_f
    return cut_midl + ":" + str(prec_f)


# print find_middle_x('123.0000000003123', '123.0000000004123')


def get_row_dict(line):
    keys = ['x1', 'y1', 'x2', 'y2', 'pol_id', 'a', 'b']
    vals = line.split()
    row = {k: v for (k, v) in zip(keys, vals)}
    return row


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
    return [a, b]


def calc_Y(x, a, b):
    x = float(x)
    a = float(a)
    b = float(b)
    return a*x+b


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


# def create_node_branch(next_tree, del_val, new_info, prev_tree):
#     next_tree.create_node_branch(del_val, new_info, prev_tree)


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
                # create_node_branch(next_tree, i_d['val'], i_a, prev_tree)
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


def treatment_add_del(del_nodes, add_nodes, x_middle, root_val):
    # fixme too many for loops

    for add in add_nodes:
        add['val'] = calc_Y(x_middle, add['a'], add['b'])

    to_replace = []

    for dele in del_nodes:
        for add in add_nodes:
            if float(dele['x2']) == float(add['x1']):
                to_replace.append((dele, add))
                break
        dele['val'] = calc_Y(x_middle, dele['a'], dele['b'])






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
