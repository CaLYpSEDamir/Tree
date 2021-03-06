# -*- coding: utf-8 -*-

import math
from helpers import calc_Y


class Node(object):

    def __init__(self, val=None, type=None, parent=None,
                 a=None, b=None, pid=None, tree_id=None, x2=None, y2=None):
        self.val = val
        self.w = 0
        self.left = None
        self.right = None
        self.parent = parent
        self.type = type

        self.pids = []
        if pid:
            self.pids.append(pid)
        self.a = a
        self.b = b
        # при построении версий, new in new version
        self.new_in_v = False
        # временно
        self.tree_id = tree_id

        self.x2 = x2
        self.y2 = y2

    def __str__(self):
        return ('(tree={3}, val={0}, type={1}, w={2},' +
               'a={4}, b={5}, new_in_v={6}, x={7}, y={8})').format(
            self.val, self.type, self.w, self.tree_id, self.a, self.b,
            self.new_in_v, self.x2, self.y2)

    def copy_node_attrs(self, orig_node, parent_to_copy,
                        val=None, pid=None,
                        a=None, b=None, not_rotate=True):
        """
            делает копию ноды при добавлении/замене значения в новое дерево
        """
        self.val = orig_node.val if val is None else val
        self.left = orig_node.left
        self.right = orig_node.right
        self.type = orig_node.type
        self.w = orig_node.w
        self.new_in_v = True
        self.a = orig_node.a if a is None else a
        self.b = orig_node.b if b is None else b

        self.pids = [x for x in orig_node.pids]

        self.parent = parent_to_copy

        self.x2 = orig_node.x2
        self.y2 = orig_node.y2

        # при простом добаление, типы должны копироваться тоже,
        # но при ротации этого не надо!
        # parent_to_copy может быть None
        if not_rotate and parent_to_copy:
            if orig_node.type == 'l':
                parent_to_copy.left = self
            else:
                parent_to_copy.right = self

    @staticmethod
    def get_node_copy(node, parent):

        if not parent.new_in_v:
            raise Exception('Version of node is old!')

        new_node = Node()
        new_node.copy_node_attrs(node, parent)
        new_node.tree_id = 'New'

        return new_node


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

    def add(self, root, val, a=None, b=None, pol_id=None, x2=None, y2=None):

        # initial root
        r_v = root.val
        if r_v is None:
            root.val = val
            root.a = a
            root.b = b
            root.pids.append(pol_id)
            root.tree_id = str(id(self))+' O'
            root.x2 = x2
            root.y2 = y2
        else:
            if val < r_v:
                if not root.left:
                    root.left = Node(val, 'l', root, a, b, pid=pol_id,
                                     tree_id=str(id(self))+' O', x2=x2, y2=y2)
                    root.w -= 1
                    self.change_w_and_check(root)
                else:
                    self.add(root.left, val, a, b, pol_id, x2=x2, y2=y2)
            elif r_v < val:
                if not root.right:
                    root.right = Node(val, 'r', root, a, b, pid=pol_id,
                                      tree_id=str(id(self))+' O', x2=x2, y2=y2)
                    root.w += 1
                    self.change_w_and_check(root)
                else:
                    self.add(root.right, val, a, b, pol_id, x2=x2, y2=y2)
            else:
                # добавляем второй id полигона
                root.pids.append(pol_id)

    # добавление нодов в версионное дерево
    def add_versionly(self, orig_tree, new_node_info):
        """
        Во всех add/del/replace функциях, если self.root.val is None,
        а значит пустое дерево, то копируем с ориг дерева!
        иначе работаем только с копи-деревом
        """
        val = new_node_info['val']
        a = new_node_info['a']
        b = new_node_info['b']
        pid = new_node_info['pol_id']
        x2 = new_node_info['x2']
        y2 = new_node_info['y2']

        orig = orig_tree.root
        copy = self.root

        # значит копи-дерево пусто и будем работать с ориг-деревом
        if copy.val is None:
            # копируем корень ориг дерева
            copy.copy_node_attrs(orig, None)
            copy.tree_id = str(id(self))+' N'

        # fixme со ссылками на parent проблемы
        if copy.val == val:
            copy.pids.append(pid)
            return

        # идем вниз, копируя,
        # fixme не обработано, если значение уже есть, то pol_id2 сувать
        child, side = (copy.left, 'l') if copy.val > val else (copy.right, 'r')

        while child:
            # уже иммеется значение в дереве
            if child.val == val:
                child.pids.append(pid)
                child.x2 = x2
                child.y2 = y2
                return
            # создание копии ноды
            if not child.new_in_v:
                new_node = Node()
                new_node.copy_node_attrs(child, copy)
                new_node.tree_id = str(id(self))+' N'
                copy = new_node
            else:
                copy = child
            child, side = (copy.left, 'l') if copy.val > val else (copy.right, 'r')
        else:
            new_node = Node(val=val, type=side, parent=copy,
                            a=a, b=b, pid=pid,
                            tree_id=str(id(self))+' N',
                            x2=x2, y2=y2)
            new_node.new_in_v = True
            new_node.tree_id = str(id(self))+' N'
            if side == 'l':
                copy.left = new_node
                copy.w -= 1
            else:
                copy.right = new_node
                copy.w += 1
            self.change_w_and_check_versionly(copy)

    def check_next_tree(self, prev_tree, x_middle):
        pass

    # добавление нодов в версионное дерево
    def replace_versionly(self, orig_tree, val, new_info):
        # fixme со ссылками на parent проблемы
        orig = orig_tree.root
        copy = self.root

        # значит копи-дерево пусто и будем работать с ориг-деревом
        if copy.val is None:
            # такого быть не должно,чтобы на реплэйсе оба дерева были пусты
            if orig.val is None:
                raise Exception("Something went wrong! Tree is empty!")
            # копируем корень ориг дерева
            copy.copy_node_attrs(orig, None)
            copy.tree_id = str(id(self))+' N'
        # корень copy уже есть копия
        if copy.val == val:
            copy.a = new_info['a']
            copy.b = new_info['b']
            copy.x2 = new_info['x2']
            copy.y2 = new_info['y2']
            copy.pids.append(new_info['pol_id'])
            return

        # идем вниз, копируя,
        # fixme не обработано, если значение уже есть, то pol_id2 сувать
        child = copy.left if copy.val > val else copy.right

        while child:
            if not child.new_in_v:
                new_node = Node()
                new_node.copy_node_attrs(child, copy)
                new_node.tree_id = str(id(self))+' N'
                copy = new_node
            else:
                copy = child

            # нашли значение в дереве
            if child.val == val:
                # создание копии ноды
                copy.a = new_info['a']
                copy.b = new_info['b']
                copy.x2 = new_info['x2']
                copy.y2 = new_info['y2']
                copy.pids.append(new_info['pol_id'])
                break
            child = copy.left if copy.val > val else copy.right

    def change_w_and_check_versionly(self, node):

        parent = node.parent

        node_w = node.w
        if node_w == 0:
            return
        if not parent:
            return

        parent.w = parent.w-1 if node.type == 'l' else parent.w+1

        p_w = parent.w

        if p_w == 0:
            return

        if p_w in (-1, 1):
            self.change_w_and_check_versionly(parent)
        elif p_w == 2:
            # 2 1
            if node_w == 1:
                print 'left rotate versionly-add'
                self.left_rotate_versionly(node)
                parent.w = node.w = 0
            # 2 -1
            else:  # node_w==-1
                print 'start 2;-1'
                print 'big left rotate versionly-add'
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

                node_for_big_rotate = node.left

                self.right_rotate_versionly(node_for_big_rotate)
                self.left_rotate_versionly(node_for_big_rotate)

        # p_w = -2
        else:
            # -2 1
            if node_w == -1:
                print 'right rotate versionly-add'

                self.right_rotate_versionly(node)
                parent.w = 0
                node.w = 0
            else:  # node_w==1
                print 'start -2;1'
                print 'big right rotate versionly-add'

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

                node_for_big_rotate = node.right

                self.left_rotate_versionly(node_for_big_rotate)
                self.right_rotate_versionly(node_for_big_rotate)

    def change_w_and_check(self, node):

        parent = node.parent

        node_w = node.w
        if node_w == 0:
            return
        if not parent:
            return

        parent.w = parent.w-1 if node.type == 'l' else parent.w+1

        p_w = parent.w

        if p_w == 0:
            return

        if p_w in (-1, 1):
            self.change_w_and_check(parent)
        elif p_w == 2:
            if node_w == 1:
                print 'left rotate for add'

                self.left_rotate_for_add(node)
                parent.w = node.w = 0

            else:  # node_w==-1
                print 'start 2;-1'
                print 'big left rotate for add'

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

                node_for_big_rotate = node.left

                self.right_rotate_for_add(node_for_big_rotate)
                self.left_rotate_for_add(node_for_big_rotate)
        else:  # p_w == -2
            if node_w == -1:
                print 'right rotate for add'

                self.right_rotate_for_add(node)
                parent.w = 0
                node.w = 0
            else:  # node_w==1
                print 'start -2;1'
                print 'big right rotate for add'

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

                node_for_big_rotate = node.right

                self.left_rotate_for_add(node_for_big_rotate)
                self.right_rotate_for_add(node_for_big_rotate)

    def left_rotate_versionly(self, node):
        """
        У parent, node, parent.parent new_in_v всегда True
        """
        parent = node.parent
        s_parent = parent.parent
        node.parent = s_parent

        if not s_parent:
            node.type = None
            self.root = node
        else:
            if parent.type == 'l':
                s_parent.left = node
                node.type = 'l'
            elif parent.type == 'r':
                s_parent.right = node
                node.type = 'r'
        parent.parent = node

        # копируем левого сына of node, если он не пуст
        node_left = node.left
        if not node_left:
            parent.right = None
        else:
            new_node = Node()
            new_node.copy_node_attrs(
                node_left, parent, not_rotate=False)
            new_node.tree_id = str(id(self))+' N'
            new_node.type = 'r'
            parent.right = new_node

        node.left = parent
        parent.type = 'l'

    def left_rotate_for_add(self, node):
        parent = node.parent
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
            node.left.parent = parent
        node.left = parent
        parent.type = 'l'

    def right_rotate_versionly(self, node):
        """
        У parent, node, parent.parent new_in_v всегда True
        """
        parent = node.parent
        s_parent = parent.parent
        node.parent = s_parent

        if not s_parent:
            node.type = None
            self.root = node
        else:
            if parent.type == 'l':
                s_parent.left = node
                node.type = 'l'
            elif parent.type == 'r':
                s_parent.right = node
                node.type = 'r'
        parent.parent = node

        # копируем правго сына of node, если он не пуст
        node_right = node.right
        if not node_right:
            parent.left = None
        else:
            new_node = Node()
            new_node.copy_node_attrs(
                node_right, parent, not_rotate=False)
            new_node.tree_id = str(id(self))+' N'
            new_node.type = 'l'
            parent.left = new_node

        node.right = parent
        parent.type = 'r'

    def right_rotate_for_add(self, node):

        parent = node.parent
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
            node.right.parent = parent
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
    def get_all_nodes_vals(root):
        result = []
        childs = [root, ]
        while childs:
            new_childs = []
            for n in childs:
                result.append(n.val)
                new_childs.extend([n.left, n.right])
            childs = filter(None, new_childs)

        return result

    def update_vals(self, x_middle):
        """
        каждый раз в дереве обновляем значения, исходя из x_middle
        """
        if self.root.val is not None:
            childs = [self.root, ]
            while childs:
                new_childs = []
                for n in childs:
                    n.val = calc_Y(x_middle, n.a, n.b)
                    new_childs.extend([n.left, n.right])
                childs = filter(None, new_childs)

    @staticmethod
    def remove_update_flags(root):

        childs = [root, ]
        while childs:
            for ch in childs:
                ch.new_in_v = False
            new_childs = []
            for n in childs:
                l, r = n.left, n.right
                if l and l.new_in_v:
                    new_childs.append(l)
                if r and r.new_in_v:
                    new_childs.append(r)
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
        gen = (((y-8 if j else y)*' '
                +str(getattr(x_, 'val', None) or 'N')
                # +'('+str(getattr(x_, 'w', 'N'))+')'
                # +'('+str(getattr(x_, 'type', None) or 'N')+')'
                # +'('+str(getattr(x_, 'a', 'N'))+')'
                # +'('+str(getattr(x_, 'b', 'N'))+')'
                # +'('+str(getattr(x_, 'tree_id', None) or 'N') +')'
                # +('(N)' if x_ is None else ('(T)' if x_.new_in_v else '(F)'))
                # +('(N)' if x_ is None else
                #   '(P:'+str(getattr(getattr(x_, 'parent', None), 'val', None) or 'N')+')')
                +('(x2=')+(getattr(x_, 'x2', None) or 'N')[:8]+(')')
                +('(y2=')+(getattr(x_, 'y2', None) or 'N')[:8]+(')')
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

    def show(self):
        count = self.get_nodes_count(self.root)
        spaces = AVLTree.get_spaces(count, 7)
        self.traversing([self.root, ], spaces)

    def right_rotate_del_versionly(self, parent):
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
            node.right.parent = parent
        node.right = parent
        parent.type = 'r'

    def right_rotate_for_del(self, node):

        parent = node.parent
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
            node.right.parent = parent
        node.right = parent
        parent.type = 'r'

    def left_rotate_for_del(self, node):

        parent = node.parent
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
            node.left.parent = parent
        node.left = parent
        parent.type = 'l'

    def balance_for_deletion_versionly(self, parent):
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
            left_pivot = parent.left

            # копируем левого сына
            if not left_pivot.new_in_v:
                left_pivot = Node.get_node_copy(left_pivot, parent)

            l_w = left_pivot.w
            if l_w in [-1, 0]:
                print '-2 -1 right rotate for del versionly'

                self.right_rotate_versionly(left_pivot)

                if l_w == 0:
                    parent.w = -1
                    left_pivot.w = 1
                else:  # l_w == -1
                    parent.w = left_pivot.w = 0

            else:  # l_w == 1
                print '-2 1 big right rotate for del versionly'

                bottom = left_pivot.right
                if not bottom.new_in_v:
                    bottom = Node.get_node_copy(bottom, left_pivot)

                bottom_w = bottom.w

                if bottom_w == 0:
                    bottom.w = left_pivot.w = parent.w = 0
                elif bottom_w == 1:
                    bottom.w = parent.w = 0
                    left_pivot.w = -1
                else:  # bottom_w == -1
                    bottom.w = left_pivot.w = 0
                    parent.w = 1

                self.left_rotate_versionly(bottom)
                self.right_rotate_versionly(bottom)

        elif p_w == 2:
            right_pivot = parent.right

            # копируем правого сына
            if not right_pivot.new_in_v:
                right_pivot = Node.get_node_copy(right_pivot, parent)

            r_w = right_pivot.w
            if r_w in [0, 1]:
                print '2 1 left rotate for del versionly'

                self.left_rotate_versionly(right_pivot)

                if r_w == 0:
                    parent.w = 1
                    right_pivot.w = -1
                else:
                    parent.w = right_pivot.w = 0
            else:  # 2 -1;    l_w == -1
                print '2 -1 big left rotate for del versionly'

                # node = parent.right
                bottom = right_pivot.left
                if not bottom.new_in_v:
                    bottom = Node.get_node_copy(bottom, right_pivot)

                bottom_w = bottom.w

                if bottom_w == 0:
                    bottom.w = right_pivot.w = parent.w = 0
                elif bottom_w == 1:
                    bottom.w = right_pivot.w = 0
                    parent.w = -1
                else:  # bottom_w == -1
                    bottom.w = parent.w = 0
                    right_pivot.w = 1

                self.right_rotate_versionly(bottom)
                self.left_rotate_versionly(bottom)

        self.balance_for_deletion_versionly(parent.parent)

    def balance_for_deletion(self, parent):
        print 'simple delete parent', parent
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
            left_pivot = parent.left
            l_w = left_pivot.w
            if l_w in [-1, 0]:
                print 'right rotate for del'

                self.right_rotate_for_del(left_pivot)

                if l_w == 0:
                    parent.w = -1
                    left_pivot.w = 1
                else:  # l_w == -1
                    parent.w = left_pivot.w = 0

            else:  # l_w == 1
                print 'big right rotate for del'

                node = parent.left
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

                node_for_big_rotate = left_pivot.right

                self.left_rotate_for_del(node_for_big_rotate)
                self.right_rotate_for_del(node_for_big_rotate)

        elif p_w == 2:
            right_pivot = parent.right
            r_w = right_pivot.w
            if r_w in [0, 1]:
                print 'left rotate for del'

                self.left_rotate_for_del(right_pivot)

                if r_w == 0:
                    parent.w = 1
                    right_pivot.w = -1
                else:
                    parent.w = right_pivot.w = 0

            else:  # l_w == -1
                print 'big left rotate for del'

                node = parent.right
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

                node_for_big_rotate = right_pivot.left

                self.right_rotate_for_del(node_for_big_rotate)
                self.left_rotate_for_del(node_for_big_rotate)

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
                l.type = None
                self.root = l
                l.parent = None
            else:
                if typ == 'l':
                    par.left = l
                    par.w += 1
                else:  # right
                    par.right = l
                    par.w -= 1
                l.parent = par
                self.balance_for_deletion(par)

        elif not l and r:
            if typ is None:
                r.type = None
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

    def get_node_versionly(self, orig_tree, val):

        orig = orig_tree.root
        copy = self.root

        # значит копи-дерево пусто и будем работать с ориг-деревом
        if copy.val is None:
            # вроде такого быть не должно, чтобы оба дерева были пусты
            if orig.val is None:
                raise Exception("Something went wrong! Tree is empty!")

            # копируем корень ориг дерева
            copy.copy_node_attrs(orig, None)
            copy.tree_id = str(id(self))+' N'

        if copy.val == val:
            return copy

        # идем вниз, копируя,
        # fixme не обработано, если значение уже есть, то pol_id2 сувать
        child, side = (copy.left, 'l') if copy.val > val else (copy.right, 'r')

        while child.val != val:
            # создание копии ноды
            if not child.new_in_v:
                new_node = Node()
                new_node.copy_node_attrs(child, copy)
                new_node.tree_id = str(id(self))+' N'
                copy = new_node
            else:
                copy = child
            child, side = (copy.left, 'l') if copy.val > val else (copy.right, 'r')
        else:
            if not child.new_in_v:
                new_node = Node()
                new_node.copy_node_attrs(child, copy)
                new_node.tree_id = str(id(self))+' N'

                return new_node
            else:
                return child

        raise Exception("Tree was traversed, but no node found!")

    def delete_versionly(self, orig_tree, val):

        print 'all_vals', AVLTree.get_all_nodes_vals(orig_tree.root)

        # проверяем на наличие значения в ориг дереве
        node_exists = orig_tree.get_node(orig_tree.root, val)
        if not node_exists:
            raise Exception('No such element to delete!')

        node = self.get_node_versionly(orig_tree, val)
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
                self.balance_for_deletion_versionly(par)

        elif l and not r:

            if not l.new_in_v:
                l = Node.get_node_copy(l, node)

            if typ is None:
                l.type = None
                self.root = l
                l.parent = None
            else:
                if typ == 'l':
                    par.left = l
                    par.w += 1
                    l.type = 'l'
                else:  # right
                    par.right = l
                    par.w -= 1
                    l.type = 'r'
                l.parent = par
                self.balance_for_deletion_versionly(par)

        elif not l and r:

            if not r.new_in_v:
                r = Node.get_node_copy(r, node)

            if typ is None:
                r.type = None
                self.root = r
                r.parent = None
            else:
                if typ == 'l':
                    par.left = r
                    par.w += 1
                    r.type = 'l'
                else:  # right
                    par.right = r
                    par.w -= 1
                    r.type = 'r'
                r.parent = par
                self.balance_for_deletion_versionly(par)
        else:
            # берем минимум, удаляем минимум, заменяем ту ноду значением из минимума
            min_val = self.get_min(r)
            print 'min_val', min_val  # 45.7516111418
            print node
            # self.show()
            self.delete_versionly(orig_tree, min_val)
            node.val = min_val


if __name__ == "__main__":
    avl = AVLTree()

    # DELETION
    #---------------------------------------------------

    # deleting
    # x = [6,5]
    # x = [5,6]
    # x = [7,6,5]
    # x = [5,6,4]
    # x = [5,4,7,6,8]
    # x = [5,4,7,8]

    # left rotate
    # x = [6,5,7,8]
    # x = [6,5,8,7,9]
    # x = [7,6,9,5,8,10,11]
    # x = [7,6,9,5,8,11,10,12]

    # some difficult deletion
    # x = [9,4,12,3,5,11,14,2,10,13,15,16,]
    # x = [9,7,12,6,8,11,14,5,10,13,15,16,]
    # x = [9,7,12,5,8,11,14,4,10,13,15,16,]
    # x = [9,5,12,4,8,11,14,3,10,13,15,16,]

    # big right rotate
    # x = [4,2,5,3]
    # x = [4,2,5,1,3]
    # x = [3,0,4,-1,2,5,1]
    # x = [6,4,9,2,5,8,11,3,7,10,12,13]

    # big tree
    # x = [13,5,22,3,8,17,27,1,4,7,10,15,19,25,31,2,6,9,11,14,16,
    #      18,20,24,26,29,33,12,21,23,28,30,32,34,35]  # del 4

    # big left rotate
    # x = [6,5,8,7]
    # x = [6,5,8,7,9]
    # x = [7,6,10,5,8,11,9]
    # x = [8,5,10,3,6,9,12,2,4,7,11,1]  # del 9

    # for i in x:
    #     avl.add(avl.root, i)

    # avl.show()

    # avl.delete(9)
    # l()
    # avl.show()

    # ADDITION
    #---------------------------------------------------

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
    # x = [2,1,5,4,6,4.5]
    # x = [3,1,7,2,4,9,3.5,5,8,10,6]
    # x = [3,1,7,2,4,9,3.5,5,8,10,3.7]

    # for i in x:
    #     avl.add(avl.root, i)

    # avl.show()
