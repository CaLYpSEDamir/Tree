# -*- coding: utf-8 -*-


class Node(object):

    def __init__(self, val=None, type=None, parent=None):
        self.val = val
        self.w = 0
        self.left = None
        self.right = None
        self.parent = parent
        self.type = type


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
    i=0
    def traversing(self, li):
        if AVLTree.i<5:
            gen = ((str(getattr(x, 'val', 'N'))
                    +'('+str(getattr(x, 'w', 'N'))+')'
                    +'('+str(getattr(x, 'type', 'N'))+')') for x in li)
            li_str = ' '.join(gen)
            print li_str
            new_li = []
            for el in li:
                new_li.append(getattr(el, 'left', None))
                new_li.append(getattr(el, 'right', None))
            if any(new_li):
                AVLTree.i+=1
                self.traversing(new_li)

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
            else: #w1==1
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
        node.right = parent
        parent.type = 'r'
        parent.w = w
        node.w = w

if __name__ == "__main__":
    avl = AVLTree()
    x = [5, 6, 2, 1, 3, 4]
    for i in x:
        avl.add(avl.root, i)
    avl.traversing([avl.root, ])
