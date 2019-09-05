"""Arkanoid code used to generate level binary files.

Notes:
    The binary level files are comprised of 3 bytes (X, Y and color)
    for each brick.
    XY coordinates indicate the top left corner of the brick.
    Bricks are 13 pixels wide by 7 high.
    Common X values:
        6, 19, 32, 45, 58, 71, 84, 97, 110 (9 columns across)
        16, 28, 40, 52, 64, 76, 88, 100 (8 columns across)
    Common Y values:
        27, 34, 41, 48, 55, 62, 69, 76 (8 rows is the maximum)
    Color byte (0: Red, 1: Yellow, 2: Blue, 3: Pink, 4: Green)
"""


def generate_level01():
    """Generate the bricks."""
    bricks = bytearray(120)
    index = 0
    for row in range(12, 18, 6):
        brick_color = 1
        for col in range(16, 112, 12):
            bricks[index] = col
            bricks[index + 1] = row
            bricks[index + 2] = brick_color
            print('index: {0} = {1},{2} -> {3}'.format(index,
                                                       bricks[index],
                                                       bricks[index + 1],
                                                       bricks[index + 2]))
            index += 3
    return bricks


def generate_level02():
    """Generate the bricks."""
    bricks = bytearray(108)
    index = 0
    col_x = 0
    column_counts = [8, 7, 6, 5, 4, 3, 2, 1]
    brick_colors = [1, 1, 1, 1, 0, 1, 1, 1]
    for col in range(16, 112, 12):
        row_y = 0
        for row in range(12, 18, 6):
            if row_y >= column_counts[col_x]:
                break
            brick_color = brick_colors[col_x]
            bricks[index] = col
            bricks[index + 1] = row
            bricks[index + 2] = brick_color
            print('index: {0} = {1},{2} -> {3}'.format(index,
                                                       bricks[index],
                                                       bricks[index + 1],
                                                       bricks[index + 2]))
            index += 3
            row_y += 1
        col_x += 1
    return bricks


def generate_level03():
    """Generate the bricks."""
    pi = [
        [44, 6, 1],
        [70, 6, 1],
        [31, 9, 1],
        [44, 9, 1],
        [57, 9, 0],
        [70, 9, 1],
        [83, 9, 1],
        [44, 12, 0],
        [57, 12, 0],
        [70, 12, 0],
        [31, 15, 0],
        [44, 15, 0],
        [70, 15, 0],
        [83, 15, 0],
        [31, 18, 0],
        [57, 18, 0],
        [83, 18, 0],
        [31, 23, 0],
        [44, 23, 0],
        [70, 23, 0],
        [83, 23, 0],
        [44, 28, 0],
        [57, 28, 0],
        [70, 28, 0],
        [57, 28, 0],
    ]
    bricks = bytearray(len(pi) * 3)
    index = 0
    for row in pi:
        bricks[index] = row[0]
        bricks[index + 1] = row[1]
        bricks[index + 2] = row[2]
        index += 3
    return bricks


def generate_level04():
    """Generate the bricks."""
    pi = [
        [6, 6, 1],
        [110, 6, 1],
        [6, 9, 1],
        [19, 9, 1],
        [97, 9, 1],
        [110, 9, 1],
        [6, 12, 1],
        [19, 12, 1],
        [32, 12, 1],
        [84, 12, 1],
        [97, 12, 1],
        [110, 12, 1],
        [6, 15, 1],
        [19, 15, 1],
        [32, 15, 1],
        [45, 15, 1],
        [71, 15, 1],
        [84, 15, 1],
        [97, 15, 1],
        [110, 15, 1],
        [16, 18, 0],
        [28, 18, 0],
        [40, 18, 0],
        [52, 18, 0],
        [64, 18, 0],
        [76, 18, 0],
        [88, 18, 0],
        [100, 18, 0],
    ]
    bricks = bytearray(len(pi) * 3)
    index = 0
    for row in pi:
        bricks[index] = row[0]
        bricks[index + 1] = row[1]
        bricks[index + 2] = row[2]
        index += 3
    return bricks


def generate_level05():
    """Generate the bricks."""
    rgb = [
        [6, 6, 0],
        [6, 9, 0],
        [6, 12, 0],
        [6, 15, 0],
        [6, 18, 0],
        [19, 6, 0],
        [19, 9, 0],
        [19, 12, 0],
        [19, 15, 0],
        [19, 18, 0],
        [52, 9, 1],
        [52, 12, 1],
        [52, 15, 1],
        [52, 18, 1],
        [52, 23, 1],
        [64, 9, 1],
        [64, 12, 1],
        [64, 15, 1],
        [64, 18, 1],
        [64, 23, 1],
        [97, 9, 1],
        [97, 12, 1],
        [97, 15, 1],
        [97, 18, 1],
        [97, 23, 1],
        [110, 9, 1],
        [110, 12, 1],
        [110, 15, 1],
        [110, 18, 1],
        [110, 23, 1],
    ]
    bricks = bytearray(len(rgb) * 3)
    index = 0
    for row in rgb:
        bricks[index] = row[0]
        bricks[index + 1] = row[1]
        bricks[index + 2] = row[2]
        index += 3
    return bricks


def generate_level06():
    """Generate the bricks."""
    face = {
        13: (28, 40, 52, 64, 76, 88),
        16: (16, 28, 52, 64, 88, 100),
        19: (16, 28, 52, 64, 88, 100),
        22: (16, 28, 40, 52, 64, 76, 88, 100),
        25: (16, 28, 40, 52, 64, 76, 88, 100),
        27: (16, 40, 52, 64, 76, 100),
        31: (16, 28, 88, 100),
        34: (28, 40, 52, 64, 76, 88)}

    bricks = bytearray(sum([len(v) for v in face.values()]) * 3)
    index = 0
    for k, v in face.items():
        for x in v:
            bricks[index] = x
            bricks[index + 1] = k
            bricks[index + 2] = 1
            index += 3
    return bricks


def generate_level07():
    """Generate the bricks."""
    bricks = bytearray(9 * 6 * 3)
    color = 0
    index = 0
    for x in range(6, 111, 13):
        for y in range(13, 25, 4):
            bricks[index] = x
            bricks[index + 1] = y
            bricks[index + 2] = color
            index += 3
            color += 1
            if color >= 5:
                color = 0
    return bricks


def generate_level08():
    """Generate the bricks."""
    bricks = bytearray(8 * 5 * 3)
    colors = [1, 0, 1, 1, 1]
    index = 0
    col_x = 0
    for x in range(6, 111, 26):
        for y in range(13, 25 4):
            bricks[index] = x
            bricks[index + 1] = y
            bricks[index + 2] = colors[col_x]
            index += 3
        col_x += 1
    return bricks


def generate_level09():
    """Generate the bricks."""
    pi = [
        [19, 13, 1],
        [32, 13, 1],
        [84, 13, 1],
        [97, 13, 1],
        [45, 17, 1],
        [71, 17, 1],
        [32, 20, 1],
        [45, 20, 1],
        [58, 20, 1],
        [71, 20, 1],
        [84, 20, 1],
        [32, 24, 1],
        [45, 24, 0],
        [58, 24, 1],
        [71, 24, 0],
        [84, 24, 1],
        [19, 27, 1],
        [32, 27, 1],
        [45, 27, 1],
        [58, 27, 1],
        [71, 27, 1],
        [84, 27, 1],
        [97, 27, 1],
        [6,  30, 1],
        [19, 30, 1],
        [32, 30, 1],
        [45, 30, 1],
        [58, 30, 1],
        [71, 30, 1],
        [84, 30, 1],
        [97, 30, 1],
        [110, 30, 1],
        [6, 32, 1],
        [32, 32, 1],
        [84, 32, 1],
        [110, 32, 1],
        [6, 38, 1],
        [45, 38, 1],
        [71, 38, 1],
        [110, 38, 1],
    ]
    bricks = bytearray(len(pi) * 3)
    index = 0
    for row in pi:
        bricks[index] = row[0]
        bricks[index + 1] = row[1]
        bricks[index + 2] = row[2]
        index += 3
    return bricks


def test():

    ba = generate_level01()
    path = 'Level001.bin'
    with open(path, "w") as f:
        f.write(ba)

    ba = generate_level02()
    path = 'Level002.bin'
    with open(path, "w") as f:
        f.write(ba)


test()
