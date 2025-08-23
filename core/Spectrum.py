import numpy as np
import matplotlib.pyplot as plt

default_groups = {
    1: 1,
    12: 12,
    13: (12, 1),
    14: 14,
    15: (14, 1),
    17: (12, 5),
    20: (12, 8),
    21: (12, 8, 1),
    23: (14, 9),
    24: (14, 9, 1),
    28: (14, 14),
    42: (14, 14, 14)
}


def open_spectrum(link):

    wave = [[]]
    intensity = [[]]
    mask_off = [[]]
    crystal = None
    with open(link, 'r') as file:
        for line in file:
            wavelength, value, crystal, off_scale, *other = line.split('	')
            crystal = int(crystal) - 1
            wavelength = float(wavelength.replace(',', '.'))
            value = float(value.replace(',', '.'))
            off_scale = bool(int(off_scale))

            try:
                wave[crystal].append(wavelength)
                intensity[crystal].append(value)
                mask_off[crystal].append(off_scale)

            except IndexError:
                wave.append([wavelength])
                intensity.append([value])
                mask_off.append([off_scale])

    for count in range(crystal + 1):
        wave[count] = np.array(wave[count])
        intensity[count] = np.array(intensity[count])
        mask_off[count] = np.array(mask_off[count], dtype=bool)

    return wave, intensity, mask_off


class Spectrum:

    def __init__(self, wavelength, intensity, mask=None):
        self.wavelength = wavelength
        self.intensity = intensity
        self.mask = mask
        self.crystals = len(wavelength)
        self.group = [0] * self.crystals

    def set_groups(self, *args):
        curent_crystal = 0
        for group, crystals in enumerate(args):
            for crystal in range(curent_crystal, crystals + curent_crystal):
                self.group[crystal] = int(group)
            curent_crystal += crystals

    def get_slice(self, mid, numbers=30, crystal=None):
        if crystal is None:
            crystal = self.search_crystal(mid)
        peak = np.argmin(np.abs(self.wavelength[crystal] - mid))
        if peak > numbers and (len(self.wavelength[crystal]) - peak) > numbers:
            return self.wavelength[crystal][peak-numbers: peak+numbers], \
                   self.intensity[crystal][peak-numbers: peak+numbers], self.mask[crystal][peak-numbers: peak+numbers]

        elif peak <= numbers < (len(self.wavelength[crystal]) - peak):
            return self.wavelength[crystal][: peak + numbers], \
                   self.intensity[crystal][: peak + numbers], self.mask[crystal][: peak + numbers]

        elif peak > numbers > (len(self.wavelength[crystal]) - peak):
            return self.wavelength[crystal][peak - numbers:], \
                   self.intensity[crystal][peak - numbers:], self.mask[crystal][peak - numbers:]
        else:
            return self.wavelength[crystal], self.intensity[crystal], self.mask[crystal]

    def search_crystal(self, mid, multicrystal=False):
        target_crystal = None
        target_crystals = []
        for crystal in range(self.crystals):
            if np.min(self.wavelength[crystal]) < mid < np.max(self.wavelength[crystal]):
                if target_crystal is None:
                    target_crystal = crystal
                target_crystals.append(crystal)
        return target_crystals if multicrystal else target_crystal

    def draw(self, color='black', visible_crystals=False):
        for crystal in range(self.crystals):
            xnew = self.wavelength[crystal]
            ynew = self.intensity[crystal]
            plt.step(xnew, ynew, where='mid', color=color)
            mask_diods = np.where(self.mask[crystal])

            for index in mask_diods[0]:
                l = np.mean(xnew[index-1:index+1])
                r = np.mean(xnew[index:index+2])
                v = ynew[index]
                lv = np.mean(ynew[index-1:index+1])
                rv = np.mean(ynew[index:index + 2])
                plt.step([l, l, l, r, r, r], [lv, lv, v, v, rv, rv], where='mid', color='red')

            if visible_crystals:
                xc = [np.min(self.wavelength[crystal]), np.min(self.wavelength[crystal]),
                      np.max(self.wavelength[crystal]),
                      np.max(self.wavelength[crystal]),
                      np.min(self.wavelength[crystal])]
                shift = (crystal % 2) * 1.1
                yc = [-.5 - shift, -1.5 - shift, -1.5 - shift, -.5 - shift, -.5 - shift]
                plt.plot(xc, yc, linewidth=2, color='black', alpha=0.5)
                plt.text(np.mean(self.wavelength[crystal]), -1 - shift, f'{crystal + 1}', ha='center', va='center')
