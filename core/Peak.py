import numpy as np
import matplotlib.pyplot as plt
from core.PeakUtilites import *
from core.Shape import *


class Peak:

    def __init__(self, mid, wavelength, intensity, mask=None):
        self.mid = mid
        self.wavelength = wavelength
        self.y = intensity
        if mask is not None:
            self.mask = mask
        else:
            self.mask = [False for _ in range(len(wavelength))]

        n0 = np.argmin(np.abs(self.wavelength - self.mid))

        maxima = find_maxima(self.y)
        self._n0 = maxima[np.argmin(np.abs(maxima - n0))]
        self._diod = self.wavelength[self._n0] - self.wavelength[self._n0 - 1]

        self._amplitude = None
        self._center = None
        self._background = None
        self._width = None
        self._slope = None
        self._nearest_backround = None
        self._boards = None
        self._shape = None
        self._check = None

    def find_amplitude(self, **kwargs):
        self._shape = None
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
        self._amplitude = find_integral(self.wavelength, self.y - background,
                                        left, right) / self._diod

        return self._amplitude

    def _search_center(self):
        center = 0
        mass = 0

        for i, t in zip(self.wavelength[self._n0 - 2:self._n0 + 3], self.y[self._n0 - 2:self._n0 + 3]):
            center += i * t
            mass += t
        try:
            self._center = center / mass
        except ZeroDivisionError:
            self._center = self.mid

    def _find_background(self, sz=None):
        if sz is None:
            minimums_id = find_minima(self.y)
            nl, nr = find_pairs(minimums_id, self._n0)

        else:
            if self._n0 - sz < 0:
                sz = self._n0
            left_zone = self.y[self._n0 - sz: self._n0]
            nl = self._n0 - sz + int(np.where(left_zone == np.min(left_zone))[0][0])

            if self._n0 + sz > len(self.y):
                sz = self._n0
            right_zone = self.y[self._n0: self._n0 + sz]
            nr = self._n0 + int(np.where(right_zone == np.min(right_zone))[0][0])
            pass

        if nr is None:
            nl, nr = minimums_id[-2], len(self.y) - 2

        if nl == 0:
            nl = 1

        if nr == len(self.y) - 1:
            nr = len(self.y) - 2

        nl = int(nl)
        nr = int(nr)

        bl = np.mean(self.y[nl - 1:nl + 2])
        br = np.mean(self.y[nr - 1:nr + 2])
        background = np.mean((bl, br))

        self._background = [nl, nr, bl, br, background]

    def shape(self, width=2.3997, asymmetry=0.1126, ratio=0.5197):

        shift = (self.wavelength[self._n0] - self.center) / self._diod

        cut = slice(self.background[0], self.background[1])
        x, y = self.wavelength[cut], self.y[cut]
        plt.scatter(x, y, color='red', s=10)

        grid = [np.linspace(0, len(x) - 1, 50), np.linspace(min(x), max(x), 50)]
        mid = self._n0 - shift - self._background[0]
        intensity = aprox_intensity(y, mid, width, asymmetry, ratio)
        self._amplitude = intensity
        self._shape = {'intensity': intensity, 'grid': grid, 'x': x, 'y': y, 'shift': shift, 'mid': mid,
                       'width': width, 'asymmetry': asymmetry, 'ratio': ratio}

    def draw(self):
        plt.step(self.wavelength, self.y, color='black', where='mid')
        mask_diods = np.where(self.mask)
        for index in mask_diods[0]:
            l = np.mean(self.wavelength[index - 1:index + 1])
            r = np.mean(self.wavelength[index:index + 2])
            v = self.y[index]
            lv = np.mean(self.y[index - 1:index + 1])
            rv = np.mean(self.y[index:index + 2])
            plt.step([l, l, l, r, r, r], [lv, lv, v, v, rv, rv], where='mid', color='red')
        base_x = self.wavelength
        base_y = self.y
        plt.axvline(self.mid, color='blue', alpha=0.5, linestyle='--')

        if self._background and self._shape is None:
            nl, nr, bl, br, background = self._background
            plt.plot(base_x[nl - 1:nl + 2], base_y[nl - 1:nl + 2], ds='steps-mid', linewidth=3,
                     color='black')
            plt.plot(base_x[nr - 1:nr + 2], base_y[nr - 1:nr + 2], ds='steps-mid', linewidth=3, color='black')
            x1 = [base_x[nl], base_x[nl], base_x[nr], base_x[nr]]
            y2 = [bl, background, background, br]
            plt.plot(x1, y2, color='blue', alpha=0.7)

        if self._center:
            plt.axvline(self._center, color='red', alpha=0.5, linestyle='--')

        if self._amplitude and self._shape is None:
            left, right = self._boards
            xx = np.where((base_x > left) & (base_x < right))
            yy = [base_y[np.argmin(np.abs(base_x - left))], *base_y[xx[0]], base_y[np.argmin(np.abs(base_x - right))]]
            xx = [left, *base_x[xx[0]], right]

            plt.fill_between(xx, yy, self._background[4], step='mid', color='blue', alpha=0.3)
        if self._width:
            plt.text(self.wavelength[self._n0], self.y[self._n0], round(self._width, 2))

        if self._shape:
            x = self._shape['x']
            y = self._shape['y']
            grid = self._shape['grid']
            shift = self._shape['shift']
            intensity = self._shape['intensity']
            width = self._shape['width']
            asymmetry = self._shape['asymmetry']
            ratio = self._shape['ratio']

            plt.scatter(x, y, color='red', s=10)
            plt.plot(grid[1],
                     intensity * voigt(grid[0], self._n0 - shift - self._background[0], width, asymmetry, ratio) + min(
                         y))

    def checker(self, **kwargs):
        max_width = kwargs.get('max_width', None)
        min_intensity = kwargs.get('min_intensity', None)
        nearest_back = kwargs.get('nearest_back', None)
        max_slope = kwargs.get('max_slope', None)
        center_deviation = kwargs.get('center_deviation', None)
        except_clipped = kwargs.get('except_clipped', False)
        min_counts = kwargs.get('min_counts', None)

        if except_clipped:
            for i in range(self.background[0], self.background[1]):
                if self.mask[i]:
                    self._check = {'result': False, 'reason': 'clipped'}
                    return False

        if min_counts and self.background[1] - self.background[0] < min_counts:
            self._check = {'result': False, 'reason': 'min_counts'}
            return False

        if nearest_back:
            minimums_id = find_minima(self.y)
            nearest_minimum = minimums_id[np.argmin(np.abs(minimums_id - self._n0))]
            if np.abs(self._n0 - nearest_minimum) <= nearest_back:
                self._check = {'result': False, 'reason': 'nearest_back'}
                return False

        if max_slope:
            if (np.abs(self.background[2] - self.background[3]) / self.y[self._n0]) > max_slope:
                self._check = {'result': False, 'reason': 'max_slope'}
                return False

        if center_deviation and np.abs(self.center - self.mid) / self._diod > center_deviation:
            self._check = {'result': False, 'reason': 'center deviation'}
            return False

        if isinstance(max_width, (int, float)) and self._width and self.width > max_width:
            self._check = {'result': False, 'reason': 'max_width'}
            return False

        if min_intensity:
            if self._amplitude and self._amplitude < min_intensity:
                self._check = {'result': False, 'reason': 'min calculaion amplitude'}
                return False
            elif self._amplitude is None:
                if self._background is None:
                    self._find_background()
                if (self.y[self._n0] - self._background[4]) < min_intensity:
                    self._check = {'result': False, 'reason': 'min amplitude pixels - back'}
                    return False

        self._check = {'result': True, 'reason': 'all ok'}
        return True

    @property
    def validity(self):
        if self._check is None:
            self.checker(max_slope=0.3, min_intensity=0.1, max_width=4, nearest_back=2, center_deviation=1,
                         except_clipped=True, min_counts=6)
            return self._check
        else:
            return self._check

    @property
    def width(self):
        if self._width is None:
            self._width = find_width(self.y, self._n0)
        return self._width

    @property
    def center(self):
        if self._center is None:
            self._search_center()
        return self._center

    @property
    def background(self):
        if self._background is None:
            self._find_background()
        return self._background

    @property
    def amplitude(self):
        if self._amplitude:
            return self._amplitude
        else:
            raise AttributeError('Attempt to get amplitude before calculation')





