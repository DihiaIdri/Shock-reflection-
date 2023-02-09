import math
from ShockWaveReflection import ShockWaveReflection
from tabulate import tabulate
import matplotlib.pyplot as plt

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
    #First reflected shock from wall
    shock2 = ShockWaveReflection(Rx, g, Vimp, M1, c2, P2, T2, Rho2)
    [M2, P3, T3, Rho3, c3] = shock2.find_new_states()
    Vs2 = round(shock2.shock_speed_moving(M2))
    #Shock reflected from projectile
    shock3 = ShockWaveReflection(Rx, g, Vimp, M2, c3, P3, T3, Rho3)
    [M3, P4, T4, Rho4, c4] = shock3.find_new_states()
    Vs3 = round(shock3.shock_speed_quiescent(M3))

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
    # projectile to target, xpf should be the same as target location
    [xpf, tpf] = xt_info(xp, t0, Vimp, xT, t0, 0)  # (xp, tp, Vp, xs2, ts2, Vs2)
    #Consider all interception point.
    [x1, t1] = xt_info(xp, t0, Vimp, xT, t0, Vs2)
    # Vs3 to wall, x2 should be xT
    [x2, t2] = xt_info(x1, t1, Vs3, xT, t1, 0)
    # Vs4 to projectile
    [x3, t3] = xt_info(xp, t0, Vimp, xT, t2, Vs4)

    xt_diagram(xp, xT, x1, x2, x3, t0, tpf, t1, t2, t3)

def xt_info(x1, t1, V1, x2, t2, V2):
    tf = (x1 - x2 + (V2*t2) - (V1*t1))/(V2-V1)
    xf = x1 + V1*(tf-t1)
    return xf, tf

def xt_diagram(xp, xT, x1, x2, x3, t0, tpf, t1, t2, t3):
    plt.plot([xp*1000, xT*1000], [t0*10**6, tpf*10**6])
    plt.plot([xT*1000, x1*1000], [t0*10**6, t1*10**6])  # Vs2 movement
    plt.plot([x1*1000, x2*1000], [t1*10**6, t2*10**6])  # Vs3 movement
    plt.plot([xT*1000, x3*1000], [t2*10**6, t3*10**6])  # Vs4 movement
    plt.xlabel('Position, mm')
    plt.ylabel('time, \u03BCs')
    plt.show()


if __name__ == '__main__':
    main()
