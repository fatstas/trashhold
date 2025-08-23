import matplotlib.pyplot as plt

from core.Spectrum import *
from core.Peak import *
from core.PeakUtilites import find_maxima
import time


def test1():
    peaks = []
    spectrum = Spectrum(*open_spectrum('C:\PyCharm Community Edition 2022.2.3\\temp/Silicon.txt'))
    spectrum.draw()
    start = time.perf_counter()
    for crystal in range(spectrum.crystals):
        maximums_id = find_maxima(spectrum.intensity[crystal])
        for i in maximums_id:
            line = spectrum.wavelength[crystal][i]
            peak = Peak(line, *spectrum.get_slice(line, crystal=crystal))

            peaks.append(peak)
            # if peak.checker(max_width=3.7):
            #     peak.draw()

    print(time.perf_counter() - start)
    print(len(peaks))
    plt.show()
    # value = peak.find_amplitude()
    # print(peak.checker(max_width=4))
    # peak.draw()


if __name__ == '__main__':

    # spectrum = Spectrum(*open_spectrum('C:\Atom x64 3.3 (2025.03.18)\Data\Export\GRAND_STANDARTS_14+9+1\\001-097 _ РЗ-6 - (1).txt'))
    spectrum = Spectrum(*open_spectrum('030-062 _ эт 8 - (2).txt'))
    # spectrum.draw()
    line = 269.91
    peak = Peak(line, *spectrum.get_slice(line))
    # peak.find_amplitude(search_background=35)
    peak.shape()
    peak.draw()


    plt.show()
