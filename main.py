from core.Spectrum import *
from core.Peak import *


if __name__ == '__main__':

    spectrum = Spectrum(*open_spectrum('C:/Atom x64 23/noname.txt'))
    spectrum.draw()
    peak = Peak(307.38, *spectrum.get_slice(307.38))

    value = peak.find_amplitude()
    value1 = peak.amplitude
    print(value == value1)
    peak.draw()
    plt.show()
