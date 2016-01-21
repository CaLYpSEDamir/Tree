# -*- coding: utf-8 -*-

import math
from simple_helpers import l


class Node(object):

    def __init__(self, val=None, type=None, parent=None,
                 a=None, b=None, pid1=None, pid2=None, tree_id=None):
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
        self.pid1_filled = False
        # при построении версий, new in new version
        self.new_in_v = False
        # временно
        self.tree_id = tree_id

    def __str__(self):
        return '(tree={3}, val={0}, type={1}, w={2})'.format(
            self.val, self.type, self.w, self.tree_id)

    def calc_new_val(self, x_m):
        x_m = float(x_m)
        a = float(self.a)
        b = float(self.b)
        return a*x_m+b

    def set_new_val(self, x_m):
        self.val = self.calc_new_val(x_m)

    def copy_node_attrs(self, orig_node, val_to_copy, parent_to_copy):
        """
            делает копию ноды при добавлении/замене значения в новое дерево
        """
        self.val = val_to_copy
        self.left = orig_node.left
        self.right = orig_node.right
        self.type = orig_node.type
        self.w = orig_node.w
        self.new_in_v = True
        self.a = orig_node.a
        self.b = orig_node.b

        if parent_to_copy:
            if orig_node.type == 'l':
                parent_to_copy.left = self
            else:
                parent_to_copy.right = self

        self.parent = parent_to_copy


class AVLTree(object):
    """
        AVL Search Tree
    """

    def __init__(self, nodes=None):
        self.root = Node()
        # строим дерево в ините, передавая список значений
        if nodes is not None:
            for i_ in nodes:
                self.add(self.root, i_)

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
            root.tree_id = id(self)
        else:
            if val < r_v:
                if not root.left:
                    root.left = Node(val, 'l', root, a, b, pid1=pol_id, tree_id=id(self))
                    root.w -= 1
                    self.change_w_and_check(root.parent, root)
                else:
                    self.add(root.left, val, a, b, pol_id)
            elif r_v < val:
                if not root.right:
                    root.right = Node(val, 'r', root, a, b, pid1=pol_id, tree_id=id(self))
                    root.w += 1
                    self.change_w_and_check(root.parent, root)
                else:
                    self.add(root.right, val, a, b, pol_id)
            else:
                # добавляем второй id полигона
                root.pid2 = pol_id

    # добавление нодов в версионное дерево
    def ADD_create_node_branch(self, orig_tree, val):
        """
        Во всех add/del/replace функциях, если self.root.val is None,
        а значит пустое дерево, то копируем с ориг дерева!
        иначе работаем только с копи-деревом
        """
        # FIXME возможно хватит тока копировать вначале только корень

        # предок для новой ноды
        parent_for_copy = None
        orig = orig_tree.root
        copy = self.root

        # значит копи-дерево пусто и будем работать с ориг-деревом
        if copy.val is None:
            # вроде такого быть не должно, чтобы оба дерева были пусты
            if orig.val is None:
                raise Exception("Something went wrong! Tree is empty!")
            # копируем корень ориг дерева
            copy.copy_node_attrs(orig, orig.val, None)
            copy.tree_id = id(self)
        # идем вниз, копируя, но со ссылками на parent проблемы

        if copy.val == val:
            print 'Value {0} is already in Tree root!'.format(str(val))
            return

        # fixme не обработано, если значение уже есть, то pol_id2 сувать
        child, side = (copy.left, 'l') if copy.val > val else (copy.right, 'r')

        while child:
            # уже иммеется значение в дереве
            if child.val == val:
                print 'Value {0} is already in Tree!'.format(str(val))
                break
            # создание копии ноды
            if not child.new_in_v:
                new_node = Node()
                new_node.copy_node_attrs(child, child.val, copy)
                new_node.new_in_v = True
                new_node.tree_id = id(self)
                copy = new_node
            else:
                copy = child
            child, side = (copy.left, 'l') if copy.val > val else (copy.right, 'r')
        else:
            new_node = Node(val=val, type=side, parent=copy, tree_id=id(self))
            new_node.new_in_v = True
            new_node.tree_id = id(self)
            if side == 'l':
                copy.left = new_node
                copy.w -= 1
            else:
                copy.right = new_node
                copy.w += 1
            self.ADD_change_w_and_check(copy.parent, copy)

    def ADD_change_w_and_check(self, parent, node):
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
            self.ADD_change_w_and_check(parent.parent, parent)
        elif p_w == 2:
            if w1 == 1:
                self.left_rotate_for_add(parent, node)
            else:  # w1==-1
                print 'start 2;-1'
                self.right_rotate_for_add(node, node.left, simple_rotate=False)
                self.left_rotate_for_add(node.parent.parent, node.parent)
        else:  # p_w==-2
            if w1 == -1:
                self.right_rotate_for_add(parent, node)
            else:  # w1==1
                self.left_rotate_for_add(node, node.right, -1)
                self.right_rotate_for_add(node.parent.parent, node.parent)

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
                print 'left rotate add'
                self.show()
                l()
                self.left_rotate_for_add(parent, node)
                parent.w = 0
                node.w = 0

            else:  # w1==-1
                print 'start 2;-1'
                print 'big left rotate'
                print node.parent.val, 'parent'
                print node.val, 'node'
                print node.left.val, 'left'

                self.show()
                l()

                bottom = node.left
                bottom_w = bottom.w

                if bottom_w == 0:
                    bottom.w = node.w = parent.w = 0
                elif bottom_w == 1:
                    bottom.w = node.w = 0
                    parent.w = -1
                else:  # bottom_w == -1
                    bottom.w = parent.w = 0
                    node.w = 1

                self.right_rotate_for_add(node, node.left)
                self.left_rotate_for_add(node.parent.parent, node.parent)
        else:  # p_w==-2
            if w1 == -1:
                print 'right rotate add'
                self.show()
                l()
                self.right_rotate_for_add(parent, node)
                parent.w = 0
                node.w = 0
            else:  # w1==1
                print 'start -2;1'
                print 'big right rotate'
                print node.parent.val, 'parent'
                print node.val, 'node'
                print node.right.val, 'right'

                self.show()
                l()

                bottom = node.right
                bottom_w = bottom.w

                if bottom_w == 0:
                    bottom.w = node.w = parent.w = 0
                elif bottom_w == 1:
                    bottom.w = parent.w = 0
                    node.w = -1
                else:  # bottom_w == -1
                    bottom.w = node.w = 0
                    parent.w = 1

                self.left_rotate_for_add(node, node.right)
                self.right_rotate_for_add(node.parent.parent, node.parent)

    def left_rotate_for_add(self, parent, node):
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

    def right_rotate_for_add(self, parent, node, simple_rotate=True):
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
        """
        неправильная реализация обновления значений всех нодов каждый раз
        """
        childs = [root, ]
        while childs:
            new_childs = []
            for n in childs:
                if n.pid1_filled:
                    n.set_new_val(x_middle)
                new_childs.extend([n.left, n.right])
            childs = filter(None, new_childs)

    @staticmethod
    def remove_update_flags(root):
        childs = [root, ]
        while childs:
            new_childs = []
            for n in childs:
                n.pid1_filled = False
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
        gen = (((y-8 if j else y)*' '+str(getattr(x_, 'val', None) or 'N') +
                '('+str(getattr(x_, 'w', 'N'))+')' +
                '('+str(getattr(x_, 'type', None) or 'N')+')'
                # +'('+str(getattr(x_, 'a', 'N'))+')'
                # +'('+str(getattr(x_, 'b', 'N'))+')'
                # +'('+str(getattr(x_, 'pid1', 'N'))+')'
                # +'('+str(getattr(x_, 'pid2', 'N'))+')'
                # +'('+str(getattr(x_, 'tree_id', None) or 'N') +')'
                # +('(N)' if x_ is None else ('(T)' if x_.new_in_v else '(F)'))
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

    def create_node_branch(self, del_val, new_info, orig_tree):

        copy_par = None

        orig = orig_tree.root
        copy = self.root
        # exchanging
        while orig:
            if orig.val == del_val:
                # дерево пусто
                if not copy.new_in_v:
                    copy.val = new_info['val']
                    copy.a = new_info['a']
                    copy.b = new_info['b']
                    if not copy.pid1_filled:
                        copy.pid1 = new_info['pol_id']
                        copy.pid1_filled = True
                    else:
                        copy.pid2 = new_info['pol_id']
                    copy.new_in_v = True

                copy.left = orig.left
                copy.right = orig.right
                copy.type = orig.type
                copy.w = orig.w
                if copy_par:
                    if copy.type == 'l':
                        copy_par.left = copy
                    else:
                        copy_par.right = copy

                copy.parent = copy_par
                break
            else:
                # у нового дерева ноды пустые перед заменой
                if not copy.val:
                    copy.val = orig.val
                    copy.a = orig.a
                    copy.b = orig.b
                    copy.pid1 = orig.pid1
                    copy.pid2 = orig.pid2
                    copy.new_in_v = True
                    copy.pid2 = new_info['pol_id']

                    copy.parent = copy_par
                    copy.left = orig.left
                    copy.right = orig.right
                    copy.type = orig.type
                    copy.w = orig.w

                if copy_par:
                    if copy.type == 'l':
                        copy_par.left = copy
                    else:
                        copy_par.right = copy

                copy_par = copy
                orig, copy = (orig.left, copy.left) if orig.val > del_val else (orig.right, copy.right)

    def REPLACE_create_node_branch(
            self, orig_tree, del_val, add_val):

        copy_par = None

        orig = orig_tree.root
        copy = self.root
        # print orig
        # print copy
        # exchanging
        # идем от корня, и пока есть дети
        # обрабатываем и идем дальше
        while orig:
            # print 'orig', orig
            if orig.val == del_val:
                copy.val = add_val
                copy.left = orig.left
                copy.right = orig.right
                copy.type = orig.type
                copy.w = orig.w
                copy.tree_id = id(self)
                copy.new_in_v = True
                if copy_par:
                    if orig.type == 'l':
                        copy_par.left = copy
                    else:
                        copy_par.right = copy

                copy.parent = copy_par
                break
            else:
                # у нового дерева ноды пустые перед заменой
                if not copy.val:
                    copy.val = orig.val
                    copy.parent = copy_par
                    copy.left = orig.left
                    copy.right = orig.right
                    copy.type = orig.type
                    copy.w = orig.w
                    copy.tree_id = id(self)
                    copy.new_in_v = True

                if copy_par:
                    if copy.type == 'l':
                        copy_par.left = copy
                    else:
                        copy_par.right = copy

                copy_par = copy
                orig, copy = (
                    (orig.left, Node()) if orig.val > del_val
                        else (orig.right, Node()))

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

        elif p_w == -2:
            l_w = parent.left.w
            if l_w in [-1, 0]:
                self.right_rotate_for_del(parent)
            else:  # l_w == 1
                self.big_right_rotate(parent)
        elif p_w == 2:
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
    # x = [3,2,1]
    # x = [5,3,6,2,4,1]
    # x = [6,4,7,3,5,8,2,1]
    # -------------------------------

    # big right rotate(сначала left, потом right)
    # x = [3,1,2]
    # x = [2,1,5,3,4]
    # x = [3,1,7,2,4,9,3.5,5,6]
    # x = [3,1,7,2,4,9,3.5,5,3.7]
    # -------------------------------

    # left rotate
    # x=[1,2,3]
    # x = [2,1,3,4,5]
    # x = [4,3,6,2,5,7,8,9]
    # x = [3,2,5,1,4,6,7,8]
    # -------------------------------

    # big left rotate(сначала right, потом left)
    # x = [1,3,2]
    # x = [2,1,3,5,4]
    # x = [2,1,5,3,6,4]
    # x = [2,1,5,4,6,3]
    # x = [2,1,5,4,6,4.5]
    # x = [3,1,7,2,4,9,3.5,5,8,10,6]
    # x = [3,1,7,2,4,9,3.5,5,8,10,3.7]

    # deleting node with left, without right
    # x = [3, 2, 5, 1, ]

    # deleting node with left and right
    # x = [5,4,7,3,6,9,8]  # del 7

    for i in x:
        avl.add(avl.root, i)

    # avl.traversing2([avl.root])

    avl.show()

    # avl.delete(5)
    #
    # print 80*'-'
    # avl.show()
    # print 80*'-'
