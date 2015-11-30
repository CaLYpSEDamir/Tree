# -*- coding: utf-8 -*-

from itertools import groupby, izip_longest
from operator import itemgetter



























def replace_node(next_tree, del_val, new_info):
    node = next_tree.get_node(next_tree.root, del_val)
    node.val = new_info['val']
    node.val = new_info['']
    node.val = new_info['']
    node.val = new_info['']
    node.val = new_info['']
    node.val = new_info['']
    node.val = new_info['']


def process_add_del(to_del, to_add, next_tree, prev_tree):

    # del/add pairs
    pairs = []

    del_dict = {}
    add_dict = {}

    for k, gr in groupby(sorted(to_del, key=itemgetter('val')), lambda x: x['y2']):
        del_dict[k] = list(gr)

    for k, gr in groupby(sorted(to_add, key=itemgetter('val')), lambda x: x['y1']):
        add_dict[k] = list(gr)

    for k in del_dict:
        pairs.append((del_dict[k], add_dict.get(k, [])))

        add_dict.pop(k, None)

    # print pairs

    for pair in pairs:
        d, a = pair

        for pair in izip_longest(d, a):
            first, second = pair
            print first, second
            if first and second:
                replace_node(next_tree, first['val'], second)

    print 80 * '-'
