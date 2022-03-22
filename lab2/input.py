from polynom import xIndexData, yIndexData, zIndexData, matrixIndexData, infinity
from numpy import linspace, exp

EPS = 1e-6


def f(x, y, z):
    return exp(2 * x - y) * z**2


def generate_table(sx, ex, nx, sy, ey, ny, sz, ez, nz):
    data_table = [ [], [], [], [[]] ]

    data_table[xIndexData] = linspace(sx, ex, nx)
    data_table[yIndexData] = linspace(sy, ey, ny)
    data_table[zIndexData] = linspace(sz, ez, nz)

    for i in range(nz):
        data_table[matrixIndexData].append([])
        for j in range(ny):
            data_table[matrixIndexData][i].append([])
            for k in range(nx):
                data_table[matrixIndexData][i][j].append(f(data_table[xIndexData][k],
                                                           data_table[yIndexData][j],
                                                           data_table[zIndexData][i]))

    return data_table


def read_table(filename):
    data_table = [ [], [], [], [[]] ]

    file = open(filename, 'r')

    flagaddx = False
    flagaddy = False
    zIndex = 0
    yIndex = 0

    for line in file.readlines():
        row = line.split("\n")[0].split("\t")

        if "z=" in row[0]:
            z_str = row[0].split("z=")
            data_table[zIndexData].append(float(z_str[1]))
        elif "y\\x" in row[0]:
            if flagaddx:
                continue
            for i in range(1, len(row)):
                data_table[xIndexData].append(float(row[i]))
            flagaddx = True
        else:
            if "end" in row[0]:
                continue
            if not row[0].isdigit():
                zIndex += 1
                data_table[matrixIndexData].append([])
                yIndex = 0
                flagaddy = True
                continue

            if not flagaddy:
                data_table[yIndexData].append(float(row[0]))

            data_table[matrixIndexData][zIndex].append([])
            for i in range(1, len(row)):
                data_table[matrixIndexData][zIndex][yIndex].append(float(row[i]))
            yIndex += 1

    file.close()

    return data_table
