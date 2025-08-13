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

        self._amplitude = None
        self._center = None
        self._background = None
        self._width = None
        self._slope = None
        self._nearest_backround = None


    def intensity(self, **kwargs):

        pass

