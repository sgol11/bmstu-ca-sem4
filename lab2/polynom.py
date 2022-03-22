xIndexData = 0
yIndexData = 1
zIndexData = 2
matrixIndexData = 3
infinity = None


def sync_sort(arr_x, arr_y, arr_dy=None):
    indices = sorted(range(len(arr_x)), key=lambda i: arr_x[i])

    arr_x = [arr_x[i] for i in indices]
    arr_y = [arr_y[i] for i in indices]
    if arr_dy:
        arr_dy = [arr_dy[i] for i in indices]

    return arr_x, arr_y, arr_dy


def prepare_arrays_newton(arr_x, arr_y, x, power):
    num = power + 1
    if num > len(arr_x):
        print('ERROR: there are not enough points to build a Newton polynomial')
        return None, None

    arr_x, arr_y, _ = sync_sort(arr_x, arr_y)

    indices = (sorted(range(len(arr_x)), key=lambda i: abs(arr_x[i] - x)))

    if abs(arr_x[indices[0]] - x) == abs(arr_x[indices[1]] - x):
        indices[0], indices[1] = indices[1], indices[0]

    index_x = indices[0]

    index_x0 = index_x - num // 2
    if index_x0 < 0:
        index_x0 = 0

    index_xn = index_x0 + num
    if index_xn > len(arr_x):
        index_xn = len(arr_x)
        index_x0 = index_xn - num

    x_new = arr_x[index_x0: index_xn]
    y_new = arr_y[index_x0: index_xn]

    return x_new, y_new


def get_coefficients_newton(arr_x, arr_y, power):
    coeffs = [arr_y[0]]

    for step in range(power):
        for i in range(power - step):
            arr_y[i] = (arr_y[i + 1] - arr_y[i]) / (arr_x[i + step + 1] - arr_x[i])
        coeffs.append(arr_y[0])

    return coeffs


def count_polynom(arr_x, coeffs, x, power):
    res = 0

    for i in range(power + 1):
        tmp = coeffs[i]
        for j in range(i):
            tmp *= (x - arr_x[j])
        res += tmp

    return res


def approximate_newton(arr_x, arr_y, x, power):
    x_newton, y_newton = prepare_arrays_newton(arr_x, arr_y, x, power)
    if x_newton is None:
        print('Something went wrong')
        return None

    coeffs = get_coefficients_newton(x_newton, y_newton, power)

    return count_polynom(x_newton, coeffs, x, power)


def multidimensional_interpolation(data, nx, ny, nz, xp, yp, zp):
    matrix = data[matrixIndexData]
    x_coeffs = data[xIndexData]
    y_coeffs = data[yIndexData]
    z_coeffs = data[zIndexData]

    z_values = []
    z_res_values = []

    for k in range(len(z_coeffs)):
        y_values = []
        y_res_values = []

        for j in range(len(y_coeffs)):
            x_values = []
            x_res_values = []

            for i in range(len(x_coeffs)):
                x_values.append(x_coeffs[i])
                x_res_values.append(matrix[k][j][i])

            y_values.append(y_coeffs[j])
            y_res_values.append(approximate_newton(x_values, x_res_values, xp, nx))

        z_values.append(z_coeffs[k])
        z_res_values.append(approximate_newton(y_values, y_res_values, yp, ny))

    return approximate_newton(z_values, z_res_values, zp, nz)
