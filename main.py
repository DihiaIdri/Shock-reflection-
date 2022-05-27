import math
from sympy.solvers import solve
from sympy import Symbol
import matplotlib.pyplot as plt


def main():
    # https: // www.engineeringtoolbox.com / specific - heat - capacity - gases - d_159.html
    # Air
    g = 1.4
    Rx = 287.058  # J/kg-K
    Vp = 1100  # m/s
    d = (3.125/4)/1000  # m
    # Argon
    # g = 1.667
    # Rx = 208.13  # J/kg-K
    # Vp = 1100  # m/s
    # d = 1.5/1000  # m

    # Initial Conditions
    T1 = 20 + 273.15  # K
    P1 = 101.325  # kPa
    rho1 = P1*1000/(Rx*T1)  # kg/m^3
    C1 = math.sqrt(g*Rx*T1)
    v1 = 0
    # State 2 and shock 1
    v2 = Vp
    M1 = M_shock(g, C1, v2)
    Vs1 = C1*M1  # m/s
    [T2, P2, rho2, C2] = shock_equ(g, Rx, M1, P1, T1, rho1)
    # State 3 and shock 2
    v3 = 0
    M2 = M_shock(g, C2, v2)
    Vs2 = v2 - C2*M2
    [T3, P3, rho3, C3] = shock_equ(g, Rx, M2, P2, T2, rho2)
    # State 4 and shock 3
    v4 = Vp
    M3 = M_shock(g, C3, v4)
    Vs3 = C3*M3
    [T4, P4, rho4, C4] = shock_equ(g, Rx, M3, P3, T3, rho3)
    # State 5 and shock 4
    v5 = 0
    M4 = M_shock(g, C4, v4)
    Vs4 = v4 - C4*M4
    [T5, P5, rho5, C5] = shock_equ(g, Rx, M4, P4, T4, rho4)
    # State 6 and shock 5
    v6 = Vp
    M5 = M_shock(g, C5, v6)
    Vs5 = C5*M5
    [T6, P6, rho6, C6] = shock_equ(g, Rx, M5, P5, T5, rho5)

    print(P2, T2, rho2, C2, M1, Vs1)
    print(P3, T3, rho3, C3, M2, Vs2)
    print(P4, T4, rho4, C4, M3, Vs3)
    print(P5, T5, rho5, C5, M4, Vs4)
    print(P6, T6, rho6, C6, M5, Vs5)

    [x3, t3] = xt_info(0, 0, Vp, d, 0 , Vs2)  # (xp, tp, Vp, xs2, ts2, Vs2)
    print(x3, t3)
    [x4, t4] = xt_info(x3, t3, Vs3, d, 0 , 0)  # (xs3, ts3, Vs3, xWall, tWall, VWall)
    print(x4, t4)
    [x5, t5] = xt_info(x3, t3, Vp, x4, t4, Vs4)  # (xp, tp, Vp, xs4, ts4, Vs4)
    print(x5, t5)
    [x6, t6] = xt_info(x5, t5, Vs5, d, 0, 0)  # (xp, tp, Vp, xs4, ts4, Vs4)
    print(x5, t5)
    [xp, tp] = xt_info(0, 0, Vp, d, 0, 0)  # (xp, tp, Vp, xs4, ts4, Vs4)
    print(xp, tp)

    xt_diagram(xp, d, x3, x5, x6, tp, t3, t4, t5, t6)


def xt_info(x1, t1, V1, x2, t2, V2):
    tf = (x1 - x2 + V2*t2 - V1*t1)/(V2 - V1)
    xf = x2 + V2*(tf - t2)
    return xf, tf


def M_shock(g, C, v):
    b = (g+1)*v/(2*C)
    M = Symbol('M')
    Mpm = solve(M**2 - b*M - 1, M)  # Mpm stands for plus minus
    Mp = [val for val in Mpm if val > 0]  # Only the positive value matters
    return Mp[0]


def shock_equ(g, Rx, M, Pu, Tu, rhou):
    # u: upstream (ahead of the shock), d:downstream (new state)
    Pd = Pu*(2*g*M**2 - (g-1))/(g+1)
    Td = Tu*(2 + (g-1)*M**2)*(2*g*M**2 - (g-1))/((g+1)*M)**2
    rhod = rhou*(g+1)*M**2/(2 + (g - 1)*M**2)
    Cd = math.sqrt(g*Rx*Td)
    return Td, Pd, rhod, Cd


def xt_diagram(xp, d, x3, x5, x6, tp, t3, t4, t5, t6):
    plt.plot([0, xp], [0, tp])
    plt.plot([d, x3], [0, t3])
    plt.plot([x3, d], [t3, t4])
    plt.plot([d, x5], [t4, t5])
    plt.plot([x5, d], [t5, t6])
    plt.plot([d, d], [0, tp])
    plt.xlabel('Position, m')
    plt.ylabel('time, s')
    plt.show()


if __name__ == '__main__':
    main()
    # Nitrogen
    # g = 1.4
    # RxN = 296.8  # J/kg-K
    # rho1 = P1/(RxN*T1)
    # C1 = math.sqrt(g*RxN*T1)
