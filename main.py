from core.Spectrum import *
from core.Peak import *


if __name__ == '__main__':
    line = 253.24
    spectrum = Spectrum(*open_spectrum('C:\PyCharm Community Edition 2022.2.3\\temp/Silicon.txt'))
    # spectrum.draw()
    peak = Peak(line, *spectrum.get_slice(line))

    value = peak.find_amplitude()
    peak.find_width()
    peak.draw()
    plt.show()
