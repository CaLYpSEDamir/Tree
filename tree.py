# -*- coding: utf-8 -*-
# class Node(object):
#
#     def __init__(self, val=None, left=None, right=None):
#
#         self.val = val
#         self.left = left
#         self.right = right
#
#
# class BstTree(object):
#
#     def __init__(self):
#         self.root = Node()
#
#     def add(self, node, val):
#         if not node.val:
#             node.val = val
#             node.left = Node()
#             node.right = Node()
#         else:
#             if node.val > val:
#                 self.add(node.left, val)
#             elif node.val < val:
#                 self.add(node.right, val)
#
#     def __str__(self):
#         print 'Tree val', self.root.val
#         print self.root.val, 'left', self.root.left.val
#         print self.root.val, 'right', self.root.right.val
#         print 'Tree right', self.root.right, self.root.right.left.val
#         print 'Tree right', self.root.right, self.root.right.right.val
#         return ''
#
# if __name__=="__main__":
#
#     bst = BstTree()
#
#     bst.add(bst.root, 5)
#     bst.add(bst.root, 3)
#     bst.add(bst.root, 6)
#
#     print bst


class Node(object):

    def __init__(self, val=None):
        self.val = val
        self.left = None
        self.right = None

    def has_childs(self):
        return self.left or self.right

    def has_both_childs(self):
        return self.left and self.right

    def get_left_or_right(self):
        return self.left or self.right


class TreeBST(object):
    """
        Binary Search Tree
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
            if r_v > val:
                if not root.left:
                    root.left = Node(val)
                else:
                    self.add(root.left, val)
            elif r_v < val:
                if not root.right:
                    root.right = Node(val)
                else:
                    self.add(root.right, val)

    def contains(self, root, val):
        r_v = root.val
        if root.val is None:
            b = False
        else:
            if r_v > val:
                b = self.contains(root.left, val)
            elif r_v < val:
                b = self.contains(root.right, val)
            else:
                return True
        return b

    def __str__(self):
        n = 20
        print ' '*(n-1)+str(getattr(self.root, 'val', 'N'))
        print ' '*(n/2-1)+str(getattr(self.root.left, 'val', 'N'))+'-'*(n-1)+str(getattr(self.root.right, 'val', 'N'))
        print ' '*(n/4-1)+str(getattr(self.root.left.left, 'val', 'N'))+\
              '-'*(n-2*(n/4)-1)+str(getattr(self.root.left.right, 'val', 'N'))+\
              '-'*(2*n/4-1)+str(getattr(self.root.right.left, 'val', 'N'))+\
              '-'*(2*n/4-1)+str(getattr(self.root.right.right, 'val', 'N'))
        return ""

    def traversing(self, l):
        if l[0] is None:
            return
        x = []
        for node in l:
            x.append(getattr(getattr(node, 'left', None), 'val', None))
            x.append(getattr(getattr(node, 'right', None), 'val', None))
        print x
        self.traversing(x)

    def delete(self, val, root):
        if root.val is None:
            print 'Tree is empty'
            return
        l, r = root.left, root.right

        # чисто для корня
        if val == root.val:
            if not l and not r:
                root.val = None
                return
            if l and r:
                pass
        else:
            child, is_left = (l, True) if val < root.val else (r, False)
            if not child:
                print 'No such element in tree'
            elif child.val != val:
                self.delete(val, child)
            else:
                if not child.has_childs():
                    if is_left:
                        root.left = None
                    else:
                        root.right = None
                elif child.has_both_childs():
                    mini = self.get_min(child.right)
                    self.delete(mini, child)
                    child.val = mini
                else:
                    if is_left:
                        root.left = child.left or child.right
                    else:
                        root.right = child.left or child.right

if __name__ == "__main__":
    tr = TreeBST()
    tr.add(tr.root, 5)
    tr.add(tr.root, 3)
    tr.add(tr.root, 7)
    tr.add(tr.root, 4)
    tr.add(tr.root, 6)
    tr.add(tr.root, 1)
    tr.add(tr.root, 9)

    # print tr.contains(tr.root, 3)
    # print tr.contains(tr.root, 5)

    print tr
    # tr.traversing([tr.root, ])

    tr.delete(3, tr.root)
    print tr

    # print tr.get_min(tr.root)
    # tr.delete(3, tr.root)


