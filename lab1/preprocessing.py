def read_table(filename):

    with open(filename) as f:
        table = [line.split() for line in f]

    arr_x = [float(dot[0]) for dot in table]
    arr_y = [float(dot[1]) for dot in table]
    arr_dy = [float(dot[2]) for dot in table]

    return arr_x, arr_y, arr_dy


def sync_sort(arr_x, arr_y, arr_dy=None):

    indices = sorted(range(len(arr_x)), key=lambda i: arr_x[i])

    arr_x = [arr_x[i] for i in indices]
    arr_y = [arr_y[i] for i in indices]
    if arr_dy:
        arr_dy = [arr_dy[i] for i in indices]

    return arr_x, arr_y, arr_dy


def input_x(min_x, max_x):

    flag = 0
    x = 0
    print("\nEnter X (from interval [{}, {}]): ".format(min_x, max_x), end='')
    while not flag:
        x = input()
        try:
            val = float(x)
            flag = 1
        except ValueError:
            print("Incorrect value for X. Try again:", end='')

    return float(x)


def input_pow():

    flag = 0
    pow = 0
    print("Enter power: ", end='')
    while not flag:
        pow = input()
        try:
            val = int(pow)
            flag = 1
        except ValueError:
            print("Incorrect value for power. Try again:", end='')

    return int(pow)

