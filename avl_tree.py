# -*- coding: utf-8 -*-

import math


class Node(object):

    def __init__(self, val=None, type=None, parent=None,
                 a=None, b=None, pid1=None, pid2=None):
        self.val = val
        self.w = 0
        self.left = None
        self.right = None
        self.parent = parent
        self.type = type

        self.pid1 = pid1
        self.pid2 = pid2
        self.a = a
        self.b = b
        # при замене флаг
        self.updated = False
        # версия
        self.v = None

    def __str__(self):
        return '({0}, {1}, {2})'.format(self.val, self.type, self.w)

    def calc_new_val(self, x_m):
        x_m = float(x_m)
        a = float(self.a)
        b = float(self.b)
        return a*x_m+b

    def set_new_val(self, x_m):
        self.val = self.calc_new_val(x_m)


class AVLTree(object):
    """
        AVL Search Tree
    """

    def __init__(self):
        self.root = Node()

    def get_min(self, root):
        return root.val if not root.left else self.get_min(root.left)

    def add(self, root, val, a=None, b=None, pol_id=None):
        # initial root
        r_v = root.val
        if r_v is None:
            root.val = val
            root.a = a
            root.b = b
            root.pid1 = pol_id
        else:
            if val < r_v:
                if not root.left:
                    root.left = Node(val, 'l', root, a, b, pid1=pol_id)
                    root.w -= 1
                    self.change_w_and_check(root.parent, root)
                else:
                    self.add(root.left, val, a, b, pol_id)
            elif r_v < val:
                if not root.right:
                    root.right = Node(val, 'r', root, a, b, pid1=pol_id)
                    root.w += 1
                    self.change_w_and_check(root.parent, root)
                else:
                    self.add(root.right, val, a, b, pol_id)
            else:
                # добавляем второй id полигона
                root.pid2 = pol_id

    def change_w_and_check(self, parent, node):
        w1 = node.w
        if w1 == 0:
            return
        if not parent:
            return

        parent.w = parent.w-1 if node.type == 'l' else parent.w+1

        p_w = parent.w

        if p_w == 0:
            return

        if p_w in (-1, 1):
            self.change_w_and_check(parent.parent, parent)
        elif p_w == 2:
            if w1 == 1:
                self.left_rotate(parent, node)
            else:  # w1==-1
                print 'start 2;-1'
                self.right_rotate(node, node.left, 1)
                self.left_rotate(node.parent.parent, node.parent)
        else:  # p_w==-2
            if w1 == -1:
                self.right_rotate(parent, node)
            else:  # w1==1
                self.left_rotate(node, node.right, -1)
                self.right_rotate(node.parent.parent, node.parent)

    def left_rotate(self, parent, node, w=0):
        s_parent = parent.parent
        node.parent = s_parent
        if not s_parent:
            self.root = node
            self.root.type = None
        else:
            if parent.type == 'l':
                s_parent.left = node
                node.type = 'l'
            elif parent.type == 'r':
                s_parent.right = node
                node.type = 'r'
        parent.parent = node
        parent.right = node.left
        if node.left:
            node.left.type = 'r'
        node.left = parent
        parent.type = 'l'
        parent.w = w
        node.w = w

    def right_rotate(self, parent, node, w=0):
        s_parent = parent.parent
        node.parent = s_parent
        if not s_parent:
            self.root = node
            self.root.type = None
        else:
            if parent.type == 'l':
                s_parent.left = node
                node.type = 'l'
            elif parent.type == 'r':
                s_parent.right = node
                node.type = 'r'
        parent.parent = node
        parent.left = node.right
        if node.right:
            node.right.type = 'l'
        node.right = parent
        parent.type = 'r'
        parent.w = w
        node.w = w

    @staticmethod
    def get_nodes_count(root):
        result = []
        childs = [root, ]
        while childs:
            result.extend(childs)
            new_childs = []
            for n in childs:
                new_childs.extend([n.left, n.right])
            childs = filter(None, new_childs)

        return len(result)

    @staticmethod
    def update_vals(root, x_middle):
        childs = [root, ]
        while childs:
            new_childs = []
            for n in childs:
                if n.updated:
                    n.set_new_val(x_middle)
                new_childs.extend([n.left, n.right])
            childs = filter(None, new_childs)

    @staticmethod
    def remove_update_flags(root):
        childs = [root, ]
        while childs:
            new_childs = []
            for n in childs:
                n.updated = False
                new_childs.extend([n.left, n.right])
            childs = filter(None, new_childs)

    @staticmethod
    def get_spaces(node_count, space_count):
        if not node_count:
            return []
        log_lower = int(math.log(node_count, 2))
        h = log_lower + 1
        last_row_count = 2**(log_lower+1)

        # last level
        last_level = [space_count*i for i in xrange(last_row_count)]
        spaces = [last_level, ]

        for i in range(log_lower+1):
            new_level = []
            data = spaces[i]
            data_len = len(data)
            for ind in range(data_len)[::2]:
                new_level.append((data[ind]+data[ind+1])/2)

            spaces.append(new_level)

        return spaces[::-1]

    def process(self, items):
        if not items:
            return items
        if len(items) == 1:
            return items
        first = items.pop(0)
        rang = items[0] - first
        new_items = [first, ]
        for it in items:
            new_items.append(rang)
        return new_items

    def traversing(self, li, spaces):

        if spaces:
            s = self.process(spaces.pop(0))
        else:
            s = [0, ]
        res = zip(li, s)
        gen = (((y-8 if j else y)*' '+str(getattr(x_, 'val', 'N')) +
                '('+str(getattr(x_, 'w', 'N'))+')' +
                '('+str(getattr(x_, 'type', 'N'))+')'
                # +'('+str(getattr(x_, 'a', 'N'))+')'
                # +'('+str(getattr(x_, 'b', 'N'))+')'
                +'('+str(getattr(x_, 'pid1', 'N'))+')'
                +'('+str(getattr(x_, 'pid2', 'N'))+')'
                )
               for j, (x_, y) in enumerate(res)
            )

        li_str = ' '.join(gen)

        print li_str

        new_li = []
        for el in li:
            new_li.append(getattr(el, 'left', None))
            new_li.append(getattr(el, 'right', None))
        if any(new_li):
            self.traversing(new_li, spaces)

    def traversing2(self, li):
        # print li, 'li'

        gen = ((str(getattr(x_, 'val', 'N')) +
                '('+str(getattr(x_, 'w', 'N'))+')' +
                '('+str(getattr(x_, 'type', 'N'))+')')
               for x_ in li)

        li_str = ' '.join(gen)

        print li_str

        new_li = []
        for el in li:
            new_li.append(getattr(el, 'left', None))
            new_li.append(getattr(el, 'right', None))
        if any(new_li):
            self.traversing2(new_li)

    def get_node(self, root, val):
        r_v = root.val
        if root.val is None:
            node = None
        else:
            if r_v > val:
                if root.left:
                    node = self.get_node(root.left, val)
                else:
                    return None
            elif r_v < val:
                if root.right:
                    node = self.get_node(root.right, val)
                else:
                    return None
            else:
                return root
        return node

    def show(self):
        count = self.get_nodes_count(self.root)
        spaces = AVLTree.get_spaces(count, 7)
        self.traversing([self.root, ], spaces)

    def right_rotate_for_del(self, parent, simple_rotate=True):
        node = parent.left

        s_parent = parent.parent
        node.parent = s_parent
        if not s_parent:
            self.root = node
            self.root.type = None
        else:
            if parent.type == 'l':
                s_parent.left = node
                node.type = 'l'
            elif parent.type == 'r':
                s_parent.right = node
                node.type = 'r'
        parent.parent = node
        parent.left = node.right
        if node.right:
            node.right.type = 'l'
        node.right = parent
        parent.type = 'r'
        if simple_rotate:
            if parent.left:
                parent.w = 0 if node.w == -1 else -1
                node.w += 1
            else:
                parent.w = 0
                node.w = 0

    def left_rotate_for_del(self, parent, simple_rotate=True):
        node = parent.right
        s_parent = parent.parent
        node.parent = s_parent
        if not s_parent:
            self.root = node
            self.root.type = None
        else:
            if parent.type == 'l':
                s_parent.left = node
                node.type = 'l'
            elif parent.type == 'r':
                s_parent.right = node
                node.type = 'r'
        parent.parent = node
        parent.right = node.left
        if node.left:
            node.left.type = 'r'
        node.left = parent
        parent.type = 'l'

        if simple_rotate:
            if parent.right:
                parent.w = 0 if node.w == 1 else 1
                node.w -= 1
            else:
                parent.w = 0
                node.w = 0

    def calc_w(self, node):
        l, r = node.left, node.right
        node.w = 0
        if l:
            node.w -= 1
        if r:
            node.w += 1

    def big_right_rotate(self, parent):
        self.left_rotate_for_del(parent.left, simple_rotate=False)  # parent.left, parent.left.right
        self.right_rotate_for_del(parent, simple_rotate=False)

        parent.parent.w = 0              #         5 - parent          3 - parent.parent
        self.calc_w(parent)              #      3     7  del(7) ->  4     5 - parent
        self.calc_w(parent.parent.left)  #        4                  \ parent.parent.left

    def big_left_rotate(self, parent):
        self.right_rotate_for_del(parent.right, simple_rotate=False)  # parent.left, parent.left.right
        self.left_rotate_for_del(parent, simple_rotate=False)

        parent.parent.w = 0
        self.calc_w(parent)
        self.calc_w(parent.parent.right)

    def balance_for_deletion(self, parent):
        p_w = parent.w
        if p_w in [-1, 1]:
            return

        elif p_w == 0:
            # дошли до корня
            if parent.type is None:
                return
            elif parent.type == 'l':
                parent.parent.w += 1
            else:  # right
                parent.parent.w -= 1

        elif parent.w == -2:
            l_w = parent.left.w
            if l_w in [-1, 0]:
                self.right_rotate_for_del(parent)
            else:  # l_w == 1
                self.big_right_rotate(parent)
        elif parent.w == 2:
            l_w = parent.right.w
            if l_w in [0, 1]:
                self.left_rotate_for_del(parent)
            else:  # l_w == -1
                self.big_left_rotate(parent)

        self.balance_for_deletion(parent.parent)

    def delete(self, val):
        if self.root.val is None:
            print 'Tree is empty!'
            return
        node = self.get_node(self.root, val)
        if not node:
            print 'No such element to delete!'
            return

        l, r, typ, par = node.left, node.right, node.type, node.parent
        if not l and not r:
            # если удаляем корень без детей, то сносим дерево
            if typ is None:
                self.root = Node()
                return
            else:
                if typ == 'l':
                    par.left = None
                    par.w += 1
                else:  # right
                    par.right = None
                    par.w -= 1
                self.balance_for_deletion(par)

        elif l and not r:
            if typ is None:
                l.typ = None
                self.root = l
                l.parent = None
            else:
                if typ == 'l':
                    par.left = l
                    par.w += 1
                else:  # right
                    par.right = l
                    par.w -= 1
                self.balance_for_deletion(par)

        elif not l and r:
            if typ is None:
                r.typ = None
                self.root = r
                r.parent = None
            else:
                if typ == 'l':
                    par.left = r
                    par.w += 1
                else:  # right
                    par.right = r
                    par.w -= 1
                self.balance_for_deletion(par)
        else:
            # берем минимум, удаляем минимум, заменяем ту ноду значением из минимума
            min_val = self.get_min(node.right)
            self.delete(min_val)
            node.val = min_val


if __name__ == "__main__":
    avl = AVLTree()
    # x = [5, 6, 2, 1, 3, 4, 7, 8, 9, 10, 11, ]

    # fixme needs to check all

    # deleting node without left, without right
    # right rotate
    # x = [5,3,7,1,]
    # x = [5,3,7,1,4]
    # x = [5,3,6,2,4,7,1]
    # big right rotate
    # x = [5,3,7,4]
    # x = [6,2,6,6.5,1,4,7,5]
    # x = [6,2,6,6.5,1,4,7,3]
    # x = [6,2,6,6.5,1,4,7,3,5]
    # x = [8,6,11,2,6.5,10,12,1,4,7,9,5]

    # left rotate
    # x = [4,3,5,7]
    # x = [4,3,6,5,7]
    # x = [4,3,6,2,5,7,8]
    # x = [1,-1,4,-2,0,3,6,-3,2,5,7,4.5]
    # x = [1,-1,4,-2,0,3,6,-3,2,5,7,4.5,5.1]

    # fixme needs big left rotate


    # deleting node with left, without right
    x = [3, 2, 5, 1, ]

    # deleting node with left and right
    x = [5,4,7,3,6,9,8]  # del 7

    for i in x:
        avl.add(avl.root, i)

    # avl.traversing2([avl.root])

    avl.show()

    avl.delete(5)

    print 80*'-'
    avl.show()
    print 80*'-'
