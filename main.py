from core.Spectrum import *
from core.Peak import *
from core.PeakUtilites import find_maxima
import time


if __name__ == '__main__':
    peaks = []
    spectrum = Spectrum(*open_spectrum('C:\PyCharm Community Edition 2022.2.3\\temp/Silicon.txt'))
    # spectrum.draw()
    start = time.perf_counter()
    for crystal in range(spectrum.crystals):
        maximums_id = find_maxima(spectrum.intensity[crystal])
        for i in maximums_id:
            line = spectrum.wavelength[crystal][i]
            peak = Peak(line, *spectrum.get_slice(line, crystal=crystal))
            peaks.append(peak.checker(max_width=4))
    print(time.perf_counter() - start)
    print(len(peaks))
    peak = Peak(line, *spectrum.get_slice(line))
    value = peak.find_amplitude()
    print(peak.checker(max_width=4))
    peak.draw()
    plt.show()
