import math

import matplotlib.pyplot as plt

from ShockWaveReflection import ShockWaveReflection
from tabulate import tabulate
from Figures import Figures
import numpy as np

def main():
    g = 1.4
    Rx = 287  # J/kg·K
    # Initial state
    V1 = 0
    Vimp = 1100  # m/s
    T1 = 25+273.15
    P1 = 101.325  # kPa
    Rho1 = P1*10**3/(Rx*T1)
    c1 = math.sqrt(g*Rx*T1)  # Speed of sound in air m/s

    # V1 is the speed used to get the Mach number
    # This is the only one required for piston effect.
    # Shock ahead of projectile
    M0 = 1.5  # initial guess
    shock1 = ShockWaveReflection(Rx, g, Vimp, M0, c1, P1, T1, Rho1)
    [M1, P2, T2, Rho2, c2] = shock1.find_new_states()
    Vs1 = round(shock1.shock_speed_quiescent(M1))
    # First reflected shock from wall
    shock2 = ShockWaveReflection(Rx, g, Vimp, M1, c2, P2, T2, Rho2)
    [M2, P3, T3, Rho3, c3] = shock2.find_new_states()
    Vs2 = round(shock2.shock_speed_moving(M2))
    # Shock reflected from projectile
    shock3 = ShockWaveReflection(Rx, g, Vimp, M2, c3, P3, T3, Rho3)
    [M3, P4, T4, Rho4, c4] = shock3.find_new_states()
    Vs3 = round(shock3.shock_speed_quiescent(M3))
    # Shock reflected from wall
    shock4 = ShockWaveReflection(Rx, g, Vimp, M3, c4, P4, T4, Rho4)
    [M4, P5, T5, Rho5, c5] = shock4.find_new_states()
    Vs4 = round(shock4.shock_speed_moving(M4))

    table = [['Mach number', 'Shock speed', 'Pressure, kPa', 'Temperature, K', 'density, km/m3', 'Speed of sound, m/s'],
            [M1, Vs1, P2, T2, Rho2, c2],
            [M2, Vs2, P3, T3, Rho3, c3],
            [M3, Vs3, P4, T4, Rho4, c4],
            [M4, Vs4, P5, T5, Rho5, c5]]
    print(tabulate(table))
    # Figures
    xp = 0  # Initial position of the projectile
    xT = 1.5 / 1000  # m, distance between blast and projectile. Used as target location
    t0 = 0
    plot_figures = Figures(xp, xT, t0, Vimp, Vs2, Vs3, Vs4)
    plot_figures.position_time()

    # PISTON EFFECT
    Vpiston = [400, 500, 600, 700, 800, 900, 1000, 1100, 1200, 1300, 1400, 1500, 1600, 1700, 1800, 1900, 2000]  # m/s
    num = len(Vpiston)
    M = np.zeros(num)
    Vs = np.zeros(num)
    M0 = 1.5  # initial guess
    for i in range(num):
        V = Vpiston[i]
        shock1 = ShockWaveReflection(Rx, g, V, M0, c1, P1, T1, Rho1)
        [M1, P2, T2, Rho2, c2] = shock1.find_new_states()
        M[i] = M1
        Vs[i] = round(shock1.shock_speed_quiescent(M1))

    plt.plot(Vpiston, Vs)
    plt.xlabel('Piston speed, m/s')
    plt.ylabel('Shock wave speed, m/s')
    plt.show()


if __name__ == '__main__':
    main()
