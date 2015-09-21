# -*- coding: utf-8 -*-


class Node(object):

    def __init__(self, val=None):
        self.val = val
        self.w = 0
        self.left = None
        self.right = None

    def calc_weight(self):
        print self.w

    def left_rotate(self):
        pass


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
                root.w += 1
                if not root.left:
                    root.left = Node(val)
                else:
                    self.add(root.left, val)
                root.calc_weight()
            elif r_v < val:
                root.w -= 1
                if not root.right:
                    root.right = Node(val)
                else:
                    self.add(root.right, val)
                root.calc_weight()

    def traversing(self, li):
        gen = (str(getattr(x, 'val', 'N')) for x in li)
        li_str = ' '.join(gen)
        print li_str
        new_li = []
        for el in li:
            new_li.append(getattr(el, 'left', None))
            new_li.append(getattr(el, 'right', None))
        if any(new_li):
            self.traversing(new_li)

if __name__ == "__main__":
    avl = AVLTree()
    avl.add(avl.root, 5)
    avl.add(avl.root, 3)
    avl.add(avl.root, 1)

    print avl.traversing([avl.root, ])
