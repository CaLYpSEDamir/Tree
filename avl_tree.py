# -*- coding: utf-8 -*-

import math


class Node(object):

    def __init__(self, val=None, type=None, parent=None):
        self.val = val
        self.w = 0
        self.left = None
        self.right = None
        self.parent = parent
        self.type = type

    def __str__(self):
        return '({0}, {1}, {2})'.format(self.val, self.type, self.w)


class AVLTree(object):
    """
        AVL Search Tree
    """

    def __init__(self):
        self.root = Node()

    def get_min(self, root):
        return root.val if not root.left else self.get_min(root.left)

    def add(self, root, val):
        # initial root
        r_v = root.val
        if r_v is None:
            root.val = val
        else:
            if val < r_v:
                if not root.left:
                    root.left = Node(val, 'l', root)
                    root.w -= 1
                    self.change_w_and_check(root.parent, root)
                else:
                    self.add(root.left, val)
            elif r_v < val:
                if not root.right:
                    root.right = Node(val, 'r', root)
                    root.w += 1
                    self.change_w_and_check(root.parent, root)
                else:
                    self.add(root.right, val)

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
        # print li, 'li'
        if spaces:
            s = self.process(spaces.pop(0))
        else:
            s = [0, ]
        res = zip(li, s)
        gen = (((y-8 if j else y)*' '+str(getattr(x_, 'val', 'N')) +
                '('+str(getattr(x_, 'w', 'N'))+')' +
                '('+str(getattr(x_, 'type', 'N'))+')')
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
        print 'count', count
        spaces = AVLTree.get_spaces(count, 10)
        print spaces
        self.traversing([self.root, ], spaces)

    def delete(self, tree, val):
        if tree.root.val is None:
            print 'Tree is empty!'
            return
        node = self.get_node(tree.root, val)
        if not node:
            print 'No such element to delete!'
            return
        # print node

        l, r, typ, par = node.left, node.right, node.type, node.parent
        if not l and not r:
            # если удаляем корень без детей, то сносим дерево
            if typ is None:
                tree.root = Node()
                return
            elif typ == 'l':
                par.w += 1
            else:  # right
                par.w -= 1





if __name__ == "__main__":
    avl = AVLTree()
    # x = [5, 6, 2, 1, 3, 4, 7, 8, 9, 10, 11, ]
    x = [5, 6, 4, 3, ]
    # x = [4,2,6,1,3,5,7]
    for i in x:
        avl.add(avl.root, i)

    # avl.traversing2([avl.root])

    avl.show()

    # avl.delete(avl, 5)

    # avl.show()






