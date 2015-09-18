
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


class TreeBST(object):
    """
        Binary Search Tree
    """

    def __init__(self):
        self.root = Node()

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
        print ' '*(n-1)+str(self.root.val)
        print ' '*(n/2-1)+str(self.root.left.val)+'-'*(n-1)+str(self.root.right.val)
        print ' '*(n/4-1)+str(self.root.left.left.val)+'-'*(n-2*(n/4)-1)+str(self.root.left.right.val)+\
              '-'*(2*n/4-1)+str(self.root.right.left.val)+'-'*(2*n/4-1)+str(self.root.right.right.val)
        return ""

    def traversing(self, l):
        if l[0] is None:
            return
        x = []
        for node in l:
            print node.val if node else 'None'
            x.append(getattr(node, 'left', None))
            x.append(getattr(node, 'right', None))
        print x
        self.traversing(x)

    def delete(self, val, root):

        l, r = root.left, root.right
        #
        if val == root.val:
            if not left and not right:
                root.val = None
                return
            if l and r:
                pass
        elif val < root.val:
            if not l:
                print 'No such element in tree'
            if l.val != val:
                delete(self, val, l)
            else:
                
        elif val > root.val:
            delete(self, val, root.left)




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
    tr.traversing([tr.root, ])












































