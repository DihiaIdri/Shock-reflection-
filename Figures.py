import matplotlib.pyplot as plt
class Figures:

    def __init__(self, xp, xT, t0, Vimp, Vs2, Vs3, Vs4):
        self.xp = xp
        self.xT = xT
        self.t0 = t0
        self.Vimp = Vimp
        self.Vs2 = Vs2
        self.Vs3 = Vs3
        self.Vs4 = Vs4

    def position_time(self):
        xp = self.xp
        xT = self.xT
        t0 = self.t0
        Vimp = self.Vimp
        Vs2 = self.Vs2
        Vs3 = self.Vs3
        Vs4 = self.Vs4

        # projectile to target, xpf should be the same as target location
        [xpf, tpf] = Figures.xt_info(xp, t0, Vimp, xT, t0, 0)  # (xp, tp, Vp, xs2, ts2, Vs2)
        # Consider all interception point.
        [x1, t1] = Figures.xt_info(xp, t0, Vimp, xT, t0, Vs2)
        # Vs3 to wall, x2 should be xT
        [x2, t2] = Figures.xt_info(x1, t1, Vs3, xT, t1, 0)
        # Vs4 to projectile
        [x3, t3] = Figures.xt_info(xp, t0, Vimp, xT, t2, Vs4)

        Figures.xt_diagram(xp, xT, x1, x2, x3, t0, tpf, t1, t2, t3)

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