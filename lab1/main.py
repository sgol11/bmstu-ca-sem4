import pandas as pd

import preprocessing
import interpolation


def main():

    arr_x, arr_y, arr_dy = preprocessing.read_table('test2.txt')
    x = preprocessing.input_x(min(arr_x), max(arr_x))
    power = preprocessing.input_pow()

    res_newton = interpolation.approximate_newton(arr_x, arr_y, x, power)
    res_hermit = interpolation.approximate_hermit(arr_x, arr_y, arr_dy, x, power)
    if res_newton is not None:
        print('\nNewton y(x) = ', round(res_newton, 6))
        root_newton = interpolation.reverse_interpolation_newton(arr_x, arr_y, power)
        print('Root (reverse interpolation with Newton) = ', round(root_newton, 4))
    if res_hermit is not None:
        print('\nHermit y(x) = ', round(res_hermit, 6))
        root_hermit = interpolation.reverse_interpolation_hermit(arr_x, arr_y, arr_dy, power)
        print('Root (reverse interpolation with Hermit) = ', round(root_hermit, 4))
    
    power_range = range(0, len(arr_x))

    comp_table = []
    columns = ['n', 'Newton y(x)', 'Hermit y(x)']

    for power in power_range:
        res_newton = interpolation.approximate_newton(arr_x, arr_y, x, power)
        res_hermit = interpolation.approximate_hermit(arr_x, arr_y, arr_dy, x, power)
        comp_table.append([power, res_newton, res_hermit])

    print('\nTable for comparing polynomials (n is the power of polynomial)\n')
    df = pd.DataFrame(data=comp_table, columns=columns)
    df.index = df['n']
    df = df.drop('n', axis=1)
    print(df)


if __name__ == '__main__':
    main()
