import numpy as np
import math
from scipy.optimize import fsolve

class ShockWaveReflection:
    def __init__(self, Rx, g, V, Minit, c, P, T, Rho):
        # Initializing the known variables.
        self.Rx = Rx
        self.g = g
        # used in shock_mach_number(). Either speed behind or speed ahead of shock.
        self.c = c
        self.V = V
        self.Minit = Minit
        # initial state
        self.P = P
        self.T = T
        self.Rho = Rho

    def find_new_states(self):
        M0 = np.array(self.Minit) # guess
        M = fsolve(ShockWaveReflection.shock_mach_number, M0, args=(self.c, self.g, self.V), xtol=1e-6)[0]
        M = round(M,2)
        P21 = ShockWaveReflection.pressure_downstream(self, M)
        P2 = round(self.P*P21)
        T21 = ShockWaveReflection.temperature_downstream(self, M, P21)
        T2 = round(self.T*T21)
        c2 = round(ShockWaveReflection.speed_of_sound(self, T2))

        Rho21 = ShockWaveReflection.density_downstream(P21, T21)
        Rho2 = round(self.Rho*Rho21,2)

        return M, P2, T2, Rho2, c2

    @staticmethod
    def shock_mach_number(M, c, g, V):
        F = ((2*c/(g + 1))*(M**2 - 1)/M) - V
        return F

    def shock_speed_quiescent(self, M):
        Vs = self.c*M
        return Vs

    def shock_speed_moving(self, M):
        Vs = self.V - self.c*M
        return Vs

    def pressure_downstream(self, M):
        P21 = (2*self.g*M**2 - (self.g - 1))/(self.g+1)
        return P21

    def temperature_downstream(self, M, P21):
        T21 = P21*(2 + (self.g - 1)*M**2)/((self.g+1)*M**2)
        return T21

    @staticmethod
    def density_downstream(P21, T21):
        Rho21 = P21/T21
        return Rho21

    def speed_of_sound(self, T):
        c = math.sqrt(self.g*self.Rx*T)
        return c
