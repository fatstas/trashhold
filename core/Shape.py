import numpy as np


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