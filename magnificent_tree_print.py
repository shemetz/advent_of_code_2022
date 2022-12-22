import math


def magnificent_tree_print(tree_root, shorten_per_piece_width_by: int = 0):
    lines = []
    level = []
    next_level = []
    level.append(tree_root)
    nn = 1
    widest = 0
    while nn != 0:
        line = []
        nn = 0
        for tree_node in level:
            if tree_node is None:
                line.append(None)
                next_level.append(None)
                next_level.append(None)
            else:
                aa = tree_node.__str__()
                line.append(aa)
                widest = max(widest, len(aa))
                next_level.append(tree_node.left)
                next_level.append(tree_node.right)
                if tree_node.left:
                    nn += 1
                if tree_node.right:
                    nn += 1

        if widest % 2 == 1:
            widest += 1
        lines.append(line)
        level = next_level
        next_level = []
    perpiece = len(lines[-1]) * (widest + 4 - shorten_per_piece_width_by)
    for i in range(len(lines)):
        line = lines[i]
        hpw = int(perpiece // 2 - 1)
        if i > 0:
            for j in range(len(line)):
                # split node
                c = ' '
                if j % 2 == 1:
                    if line[j - 1] is not None:
                        c = '┘' if line[j] is None else '┴'
                    else:
                        c = ' ' if line[j] is None else '└'
                print(c, end='')
                # lines and spaces
                if line[j] is None:
                    print(' ' * math.floor(perpiece - 1), end='')
                else:
                    if j % 2 == 0:
                        print(' ' * hpw + '┌' + '─' * hpw, end='')
                    else:
                        print('─' * hpw + '┐' + ' ' * hpw, end='')
            print()
        # print line of numbers
        for j in range(len(line)):
            f = line[j] or ''
            gap1 = math.ceil(perpiece / 2 - len(f) / 2)
            gap2 = math.floor(perpiece / 2 - len(f) / 2)

            # a number
            print(" " * gap1 + f + " " * gap2, end='')
        print()
        perpiece /= 2
