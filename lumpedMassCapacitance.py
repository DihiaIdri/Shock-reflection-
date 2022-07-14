import numpy as np
import math
import matplotlib.pyplot as plt

def main():
    Cv = 251.208  # J/kg-K
    rho = 7896  # kg/m^3
    h = 1
    Tg = [3000, 4000, 5000, 6000]  # K
    Ti = 2200  #[293.15, 2200]
    t = 200*10^-9  # s

    r = np.linspace(1*10^-6, 100*10^-6, 25)
    for i in range(0, 4, 1):
        T = Tg - (Tg[i] - Ti) * math.e ** (3 * h * t / (rho * r * Cv))
        plt.plot(r, T, 'r')
        plt.show()


if __name__ == '__main__':
    main()