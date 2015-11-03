# -*- coding: utf-8 -*-


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

    def get_tree_height(self, li):
        new_li = []
        for el in li:
            new_li.append(getattr(el, 'left', None))
            new_li.append(getattr(el, 'right', None))
        if any(new_li):
            return self.get_tree_height(new_li)
        else:
            return len(li)

    def traversing2(self, li):
        gen = (str(getattr(x, 'val', 'N')) for x in li)
        li_str = ' '.join(gen)
        print li_str
        new_li = []
        for el in li:
            new_li.append(getattr(el, 'left', None))
            new_li.append(getattr(el, 'right', None))
        if any(new_li):
            self.traversing2(new_li)

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
    # tr.add(tr.root, 5)
    # tr.add(tr.root, 3)
    # tr.add(tr.root, 7)
    # tr.add(tr.root, 4)
    # tr.add(tr.root, 6)
    # tr.add(tr.root, 1)
    # tr.add(tr.root, 9)

    tr.add(tr.root, 9)
    tr.add(tr.root, 5)
    tr.add(tr.root, 7)
    tr.add(tr.root, 4)
    tr.add(tr.root, 6)
    tr.add(tr.root, 8)

    print tr.get_tree_height([tr.root, ])



