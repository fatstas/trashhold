import numpy as np
import matplotlib.pyplot as plt
from core.PeakUtilites import *


class Peak:

    def __init__(self, mid, wavelength, intensity, mask=None):
        self.mid = mid
        self.wavelength = wavelength
        self.intesity = intensity
        if mask is not None:
            self.mask = mask
        else:
            self.mask = [False for _ in range(len(wavelength))]

        n0 = np.argmin(np.abs(self.wavelength - self.mid))

        maxima = find_maxima(self.intesity)
        self._n0 = maxima[np.argmin(np.abs(maxima - n0))]
        self._diod = self.wavelength[self._n0] - self.wavelength[self._n0 - 1]

        self._amplitude = None
        self._center = None
        self._background = None
        self._width = None
        self._slope = None
        self._nearest_backround = None
        self._boards = None

    def find_amplitude(self, **kwargs):
        search_background = kwargs.get('search_background', None)
        width_integration = kwargs.get('width_integration', 2.7)
        center_deviation = kwargs.get('center_deviation', None)

        self._find_background(search_background)
        nl, nr, bl, br, background = self._background

        self._search_center()

        if center_deviation is not None and np.abs(self._center - self.mid) > center_deviation:
            self._center = self.mid

        left = self._center - (width_integration / 2) * self._diod
        right = self._center + (width_integration / 2) * self._diod
        self._boards = [left, right]
        self._amplitude = find_integral(self.wavelength, self.intesity - background,
                                        left, right) / self._diod

        return self._amplitude

    def _search_center(self):
        center = 0
        mass = 0

        for i, t in zip(self.wavelength[self._n0 - 2:self._n0 + 3], self.intesity[self._n0 - 2:self._n0 + 3]):
            center += i * t
            mass += t
        self._center = center / mass

    def _find_background(self, sz=None):
        if sz is None:
            minimums_id = find_minima(self.intesity)
            nl, nr = find_pairs(minimums_id, self._n0)

        else:
            pass

        if nr is None:
            nl, nr = minimums_id[-2], len(self.intesity) - 2

        if nl == 0:
            nl = 1

        if nr == len(self.intesity) - 1:
            nr == len(self.intesity) - 2

        nl = int(nl)
        nr = int(nr)

        bl = np.mean(self.intesity[nl - 1:nl + 2])
        br = np.mean(self.intesity[nr - 1:nr + 2])
        background = np.mean((bl, br))

        self._background = [nl, nr, bl, br, background]

    def draw(self):
        plt.step(self.wavelength, self.intesity, color='black', where='mid')
        mask_diods = np.where(self.mask)
        for index in mask_diods[0]:
            l = np.mean(self.wavelength[index - 1:index + 1])
            r = np.mean(self.wavelength[index:index + 2])
            v = self.intesity[index]
            lv = np.mean(self.intesity[index - 1:index + 1])
            rv = np.mean(self.intesity[index:index + 2])
            plt.step([l, l, l, r, r, r], [lv, lv, v, v, rv, rv], where='mid', color='red')
        base_x = self.wavelength
        base_y = self.intesity
        plt.axvline(self.mid, color='blue', alpha=0.5, linestyle='--')

        if self._background:
            nl, nr, bl, br, background = self._background
            plt.plot(base_x[nl - 1:nl + 2], base_y[nl - 1:nl + 2], ds='steps-mid', linewidth=3,
                     color='black')
            plt.plot(base_x[nr - 1:nr + 2], base_y[nr - 1:nr + 2], ds='steps-mid', linewidth=3, color='black')
            x1 = [base_x[nl], base_x[nl], base_x[nr], base_x[nr]]
            y2 = [bl, background, background, br]
            plt.plot(x1, y2, color='blue', alpha=0.7)

        if self._center:
            plt.axvline(self._center, color='red', alpha=0.5, linestyle='--')

        if self._amplitude:
            left, right = self._boards
            xx = np.where((base_x > left) & (base_x < right))
            yy = [base_y[np.argmin(np.abs(base_x - left))], *base_y[xx[0]], base_y[np.argmin(np.abs(base_x - right))]]
            xx = [left, *base_x[xx[0]], right]

            plt.fill_between(xx, yy, self._background[4], step='mid', color='blue', alpha=0.3)
        if self._width:
            plt.text(self.wavelength[self._n0], self.intesity[self._n0], round(self._width, 2))

    def find_width(self):
        self._width = find_width(self.intesity, self._n0)

    def checker(self, **kwargs):
        pass

    @property
    def center(self):
        if self._center is None:
            self._search_center()
        return self._center

    @property
    def amplitude(self):
        if self._amplitude:
            return self._amplitude
        else:
            raise AttributeError('Attempt to get amplitude before calculation')





