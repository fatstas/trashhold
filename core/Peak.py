import numpy as np
import matplotlib.pyplot as plt
from PeakUtilites import *


class Peak:

    def __init__(self, mid, wavelength, intensity, mask=None):
        self.mid = mid
        self.wavelength = wavelength
        self.intesity = intensity
        if mask is not None:
            self.mask = mask
        else:
            self.mask = [False for _ in range(len(wavelength))]

        self._n0 = np.argmin(np.abs(self.wavelength - self.mid))

        self._amplitude = None
        self._intensity = None
        self._center = None
        self._background = None
        self._width = None
        self._slope = None
        self._nearest_backround = None

    def intensity(self, **kwargs):
        search_zone = kwargs.get('search_zone', None)

        self._find_background(search_zone)



        pass

    def _find_background(self, sz=None):
        if sz is None:
            minimums_id = find_minima(self.intesity)
            nl, nr = find_pairs(minimums_id, self._n0)
            if nr is None:
                nl, nr = minimums_id[-2], len(self.intesity) - 2

            if nl == 0:
                nl = 1

            if nr == len(self.intesity) - 1:
                nr == len(self.intesity) - 2

            self._background = nl, nr

        else:
            pass


