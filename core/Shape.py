import numpy as np
from scipy import interpolate
from scipy.optimize import minimize


def voigt(x, x0, w, a, r):
    '''
    Voigt distribution with position x0 and unit intensity.

    Args:
        x0: position;
        w: width;
        a: assymetry;
        r: ratio (in range 0-1).

    A simple asymmetric line shape profile for fitting infrared absorption spectra.
    Aaron L. Stancik, Eric B. Brauns
    https://www.sciencedirect.com/science/article/abs/pii/S0924203108000453
    '''

    sigma = 2*w / (1 + np.exp(a*(x - x0)) )
    G = np.sqrt(4*np.log(2)/np.pi) / sigma * np.exp(-4*np.log(2)*((x - x0)/sigma)**2)
    L = 2/np.pi/sigma/(1 + 4*((x - x0)/sigma)**2)
    F = r*L + (1 - r)*G

    return F


def fittness(y, interp, t):
    result = 0
    for i, value in enumerate(y):
        result += (value - t * interp(i)) ** 2
    return result


def aprox_intensity(y, x0, w, a, r):
    grid = np.linspace(0, len(y) - 1, 50)
    background = min(y)
    y = y - background
    interp_shape = interpolate.interp1d(grid, voigt(grid, x0, w, a, r))
    t0 = [1]
    res = minimize(lambda t: fittness(y, interp_shape, t[0]), t0)
    intensity = res.x[0]
    return intensity



