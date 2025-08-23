import matplotlib.pyplot as plt

from core.Spectrum import *
from core.Peak import *
from core.PeakUtilites import find_maxima
import time


def test1():
    peaks = []
    spectrum = Spectrum(*open_spectrum('001-276 _ РЗ-6 - (2).txt'))
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

    for peak in peaks:
        if peak.validity['result'] and peak.mid > 250:
            peak.find_amplitude()
            peak.draw()

            plt.show()

    print(time.perf_counter() - start)
    print(len(peaks))
    plt.show()
    # value = peak.find_amplitude()
    # print(peak.checker(max_width=4))
    # peak.draw()


if __name__ == '__main__':
    test1()
    # spectrum = Spectrum(*open_spectrum('C:\Atom x64 3.3 (2025.03.18)\Data\Export\GRAND_STANDARTS_14+9+1\\001-097 _ РЗ-6 - (1).txt'))
    start = time.perf_counter()
    spectrum = Spectrum(*open_spectrum('030-062 _ эт 8 - (2).txt'))
    print(time.perf_counter() - start)
    # spectrum.draw()
    line = 269.91
    peak = Peak(line, *spectrum.get_slice(line))
    # peak.find_amplitude(search_background=35)
    peak.shape()
    print(peak.validity)
    peak.draw()


    plt.show()
