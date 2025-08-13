from core.Spectrum import *


if __name__ == '__main__':

    spectrum = Spectrum(*open_spectrum('C:/PyCharm Community Edition 2022.2.3/temp/Silicon.txt'))
    spectrum.draw()

    plt.show()
