from polynom import *
from input import *


def main():
    xs, xe, nx = -5, 5, 20
    ys, ye, ny = -3, 4, 50
    zs, ze, nz = -1, 2, 30
    table = generate_table(xs, xe, nx,
                           ys, ye, ny,
                           zs, ze, nz)

    # table = read_table("data.txt")

    x = float(input("Введите аргумент x: "))
    y = float(input("Введите аргумент y: "))
    z = float(input("Введите аргумент z: "))

    print()

    nx = int(input("Введите степень аппроксимации nx: "))
    ny = int(input("Введите степень аппроксимации ny: "))
    nz = int(input("Введите степень аппроксимации nz: "))

    print("\nResult:", end=" ")

    print(multidimensional_interpolation(table, nx, ny, nz, x, y, z))
    print("Real value: ", f(x, y, z))


if __name__ == '__main__':
    main()
