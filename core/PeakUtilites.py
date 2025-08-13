import numpy as np


def fast_integration(interp_x, interp_y, left, right, counts=20):
    dx = (right - left) / counts
    result = 0.0
    for x in np.linspace(left, right, counts):
        idx = np.searchsorted(interp_x, x)
        if idx == 0:
            y = interp_y[0]
        elif idx == len(interp_y):
            y = interp_y[-1]
        else:
            # Линейная интерполяция
            x0, x1 = interp_x[idx-1], interp_x[idx]
            y0, y1 = interp_y[idx-1], interp_y[idx]
            y = y0 + (y1 - y0) * (x - x0) / (x1 - x0)
        result += y * dx

    return result


def find_maxima(base_y):
    out = []
    for i in range(1, len(base_y) - 1):
        if base_y[i - 1] <= base_y[i] >= base_y[i + 1]:
            out.append(i)
    return np.array(out)


def find_minima(base_y):
    out = [base_y[0]]
    for i in range(1, len(base_y) - 1):
        if base_y[i - 1] >= base_y[i] <= base_y[i + 1]:
            out.append(i)
    out.append(base_y[-1])
    return np.array(out)


def find_pairs(minimums_id, n0):
    nl, nr = None, None
    for i, index in enumerate(minimums_id[:-1]):
        if index <= n0 < minimums_id[i + 1]:
            nl, nr = index, minimums_id[i + 1]
            break
    return nl, nr
