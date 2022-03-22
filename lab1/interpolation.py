import preprocessing as pr

EPS = 1e-5
notMonotone = 'notMonotone'
increasing = 'increasing'
decreasing = 'decreasing'


"""
    Newton interpolation
"""


def prepare_arrays_newton(arr_x, arr_y, x, power):
    num = power + 1
    if num > len(arr_x):
        print('ERROR: there are not enough points to build a Newton polynomial')
        return None, None

    arr_x, arr_y, _ = pr.sync_sort(arr_x, arr_y)

    index_x = (sorted(range(len(arr_x)), key=lambda i: abs(arr_x[i] - x)))[0]

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
        return None

    coeffs = get_coefficients_newton(x_newton, y_newton, power)

    return count_polynom(x_newton, coeffs, x, power)


"""
    Hermit interpolation
"""


def prepare_arrays_hermit(arr_x, arr_y, arr_dy, x, power):
    num = (power // 2) + 1
    if num > len(arr_x):
        print('ERROR: there are not enough points to build a Hermit polynomial')
        return None, None, None

    arr_x, arr_y, arr_dy = pr.sync_sort(arr_x, arr_y, arr_dy)

    index_x = (sorted(range(len(arr_x)), key=lambda i: abs(arr_x[i] - x)))[0]

    index_x0 = index_x - num // 2
    if index_x0 < 0:
        index_x0 = 0

    index_xn = index_x0 + num
    if index_xn > len(arr_x):
        index_xn = len(arr_x)
        index_x0 = index_xn - num

    x_new = []
    y_new = []
    dy_new = []

    for i in range(index_x0, index_xn):
        x_new.append(arr_x[i])
        x_new.append(arr_x[i])
        y_new.append(arr_y[i])
        y_new.append(arr_y[i])
        dy_new.append(arr_dy[i])

    return x_new, y_new, dy_new


def find_coeffs_hermit(arr_x, arr_y, arr_dy, power):
    coeffs = [arr_y[0]]

    for step in range(power):
        for i in range(power - step):
            if (step == 0) and (i % 2 == 0):
                arr_y[i] = arr_dy[i // 2]
            else:
                arr_y[i] = (arr_y[i + 1] - arr_y[i]) / (arr_x[i + step + 1] - arr_x[i])
        coeffs.append(arr_y[0])

    return coeffs


def approximate_hermit(arr_x, arr_y, arr_dy, x, power):
    x_hermit, y_hermit, dy_hermit = prepare_arrays_hermit(arr_x, arr_y, arr_dy, x, power)
    if x_hermit is None:
        return None

    coeffs = find_coeffs_hermit(x_hermit, y_hermit, dy_hermit, power)

    print(coeffs)

    return count_polynom(x_hermit, coeffs, x, power)


"""
    Reverse interpolation
"""


def get_type_of_monotone(arr_y):
    is_increasing = True
    is_decreasing = True

    for i in range(len(arr_y) - 1):
        if not (arr_y[i] < arr_y[i + 1]):
            is_increasing = False
    for i in range(len(arr_y) - 1):
        if not (arr_y[i] > arr_y[i + 1]):
            is_decreasing = False

    if is_increasing:
        return increasing
    if is_decreasing:
        return decreasing
    return notMonotone


def reverse_interpolation_newton(arr_x, arr_y, n):
    monotone = get_type_of_monotone(arr_y)
    arr_x, arr_y, _ = pr.sync_sort(arr_x, arr_y)

    if monotone != notMonotone:
        x_root = approximate_newton(arr_y, arr_x, 0, n)
    else:
        r = arr_x[-1]
        l = arr_x[0]
        while r - l > EPS:
            m = (r + l) / 2
            y = approximate_newton(arr_x, arr_y, m, n)
            if y < 0:
                l = m
            else:
                r = m
        x_root = l

    return x_root


def reverse_interpolation_hermit(arr_x, arr_y, arr_dy, n):
    monotone = get_type_of_monotone(arr_y)
    arr_x, arr_y, arr_dy = pr.sync_sort(arr_x, arr_y, arr_dy)

    if monotone != notMonotone:
        arr_dy_reverse = []
        for i in range(len(arr_dy)):
            if arr_dy[i] != 0:
                arr_dy_reverse.append(1 / arr_dy[i])
            else:
                arr_dy_reverse.append(0)
        x_root = approximate_hermit(arr_y, arr_x, arr_dy_reverse, 0, n)
    else:
        r = arr_x[-1]
        l = arr_y[0]
        while r - l > EPS:
            m = (r + l) / 2
            y = approximate_hermit(arr_x, arr_y, arr_dy, m, n)
            if y < 0:
                l = m
            else:
                r = m
        x_root = l

    return x_root

