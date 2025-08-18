import numpy as np
import matplotlib.pyplot as plt


def find_integral(base_x, base_y, left, right, counts=20):
    dx = (right - left) / counts
    result = 0.0
    for x in np.linspace(left, right, counts):
        idx = np.searchsorted(base_x, x)
        if idx == 0:
            y = base_y[0]
        elif idx == len(base_y):
            y = base_y[-1]
        else:
            x0, x1 = base_x[idx - 1], base_x[idx]
            y0, y1 = base_y[idx - 1], base_y[idx]
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
    return int(nl), int(nr)


def find_width(y, n0):
    minimums_id = find_minima(y)
    nl, nr = find_pairs(minimums_id, n0)
    if nl is None or nr is None:
        return None
    background = np.mean((y[nl], y[nr]))
    half_value = (y[n0] - background) / 2 + background
    y = y[nl: nr + 1]
    y_hat = []
    for i, value in enumerate(y):
        if value > half_value:
            y_hat.append(i)

    x0, x1 = y_hat[0] - 1, y_hat[0]
    y0, y1 = y[x0], y[x1]
    left = x0 + (half_value - y0) / (y1 - y0)

    x0, x1 = y_hat[-1], y_hat[-1] + 1
    y0, y1 = y[x0], y[x1]
    right = x1 - (half_value - y1) / (y0 - y1)
    result = right - left

    # debug
    # plt.step([i for i, _ in enumerate(y)], y, color='black', where='mid')
    # plt.plot([i for i, _ in enumerate(y)], y, color='black')
    # plt.axvline(left, color='green', alpha=0.5, linestyle='--')
    # plt.axvline(right, color='green', alpha=0.5, linestyle='--')
    # plt.axhline(half_value, color='green', alpha=0.5, linestyle='--')
    # plt.scatter(x1, y[x1])
    # plt.scatter(x0, y[x0])
    # plt.show()
    return result
