# coding: utf-8
from __future__ import unicode_literals

import os
import platform
from itertools import imap


def get_A_B(x1, y1, x2, y2):
    """
        Неточно все считает )))
    """
    x1 = float(x1)
    x2 = float(x2)
    y1 = float(y1)
    y2 = float(y2)

    if not x1:
        b = y1
        a = (y2-b)/x2
    elif not x2:
        b = y2
        a = (y1-b)/x1
    else:
        x_diff = x1/x2
        b = (y1-x_diff*y2)/(1-x_diff)
        a = (y1-b)/x1
    return [a, b]


def coord_processing(pol_id, icoords):
    to_return = []
    prev, next = icoords.next(), icoords.next()
    while next:
        y1 = prev[0]
        x1 = prev[1]
        cut_ind_y1 = y1.index('.')+10
        cut_ind_x1 = x1.index('.')+10
        cut_y1, prec_y1 = y1[:cut_ind_y1], y1[cut_ind_y1:]
        cut_x1, prec_x1 = float(x1[:cut_ind_x1]), x1[cut_ind_x1:]

        y2 = next[0]
        x2 = next[1]
        cut_ind_y2 = y2.index('.')+10
        cut_ind_x2 = x2.index('.')+10
        cut_y2, prec_y2 = y2[:cut_ind_y2], y2[cut_ind_y2:]
        cut_x2, prec_x2 = float(x2[:cut_ind_x2]), x2[cut_ind_x2:]

        if cut_x1 < cut_x2:
            li = [float(x1), prec_x1, x1, y1, x2, y2, ]
        elif cut_x2 < cut_x1:
            li = [float(x2), prec_x2, x2, y2, x1, y1, ]
        else:
            if prec_x1 < prec_x2:
                li = [float(x1), prec_x1, x1, y1, x2, y2, ]
            elif prec_x2 < prec_x1:
                li = [float(x2), prec_x2, x2, y2, x1, y1, ]
            else:
                print 'Warning, pol_id={0} has vertical line, what to do???'.format(pol_id)
                print 'x1: ', x1, 'y1: ', y1, 'x2: ', x2, 'y2: ', y2
                try:
                    prev = next
                    next = icoords.next()
                except StopIteration:
                    next = None
                continue

        li.append(pol_id)
        li.extend(get_A_B(x1, y1, x2, y2))

        to_return.append(li)

        try:
            prev = next
            next = icoords.next()
        except StopIteration:
            next = None
    return to_return

if platform.system() == 'Windows':
    # fixme прописать нужное
    files_dir = 'c://python27/tree/EttonProducts/offline/Files/{0}'
    # dma_file = 'c://python27/tree/EttonProducts/offline/dma.data'
    dma_file = 'c://python27/tree/EttonProducts/offline/dma-cut'
else:
    files_dir = '/home/damir/Projects/EttonProducts/offline/Files/{0}'
    dma_file = '/home/damir/Projects/EttonProducts/offline/dma.data'


with open(dma_file) as dma:  # 210 polygons, 9797 coordinates (8792)
    j = 0
    l = []
    for line in dma:
        pol_id, s, coords = line.split('\t')
        icoords = imap(lambda x: x.split(), coords.split(','))
        l.extend(coord_processing(pol_id, icoords))

        if len(l) > 1000:
            print len(l), 'len is up 1000'

            l.sort(key=lambda el: (el[0], el[1]))

            with open(files_dir.format('f{0}'.format(j)), 'w') as f:
                for li in l:
                    f.write(' '.join(imap(str, li))+'\n')

            l = []
            j += 1

            # if j == 2:
            #     break

files_ = next(os.walk(files_dir.format('')))[2]


def get_file_next_line(filename):
    """
    Returns next line of opened file or None
    """
    try:
        f_line = filename.next()
    except StopIteration:
        # print filename, 'Stop ietr'
        f_line = None
    return f_line


def merge(files):
    # не обрабатывается, если все данные уместились в один файл изначально
    if len(files) > 1:
        f1_name, f2_name = files[:2]
        with open(files_dir.format(f1_name+f2_name), 'w') as f_merge:
            with open(files_dir.format(f1_name)) as f1:
                with open(files_dir.format(f2_name)) as f2:
                    f1_line = get_file_next_line(f1)
                    f2_line = get_file_next_line(f2)
                    while 1:
                        if f1_line and f2_line:
                            f1_info = f1_line.split()
                            f2_info = f2_line.split()
                            f1_x = float(f1_info[0])
                            f2_x = float(f2_info[0])
                            if f1_x < f2_x:
                                f_merge.write(f1_line)
                                f1_line = get_file_next_line(f1)
                            elif f1_x > f2_x:
                                f_merge.write(f2_line)
                                f2_line = get_file_next_line(f2)
                            else:
                                if f1_info[1] < f2_info[1]:
                                    f_merge.write(f1_line)
                                    f1_line = get_file_next_line(f1)
                                elif f1_info[1] > f2_info[1]:
                                    f_merge.write(f2_line)
                                    f2_line = get_file_next_line(f2)
                                else:
                                    f_merge.write(f1_line)
                                    f_merge.write(f2_line)
                                    f1_line = get_file_next_line(f1)
                                    f2_line = get_file_next_line(f2)

                        elif f1_line is None and f2_line is None:
                            break
                        elif f2_line is None:
                            while f1_line:
                                f_merge.write(f1_line)
                                f1_line = get_file_next_line(f1)
                            break
                        else:  # f1_line is None
                            while f2_line:
                                f_merge.write(f2_line)
                                f2_line = get_file_next_line(f2)
                            break

        os.remove(files_dir.format(f1_name))
        os.remove(files_dir.format(f2_name))

        new_files = files[2:] + [f1_name+f2_name, ]
        merge(new_files)

    # либо в конце остался только последний отсортированный,
    # либо изначально был только 1 файл тоже отсортированный
    else:
        pass
merge(files_)
