"""
Defintions for problem 0
"""
import numpy as np
import scipy.integrate
from scipy.integrate import DenseOutput, OdeSolver
from warnings import warn
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
from scipy.optimize import curve_fit
import scipy.sparse as sparse
from sympy import Function, dsolve, Eq, Derivative, sin, cos, symbols
from scipy.integrate import solve_ivp
import importlib

class ForwardEulerOutput(DenseOutput):
    def __init__(self, ts, ys):
        super().__init__(ts, ys)

class ForwardEuler(OdeSolver):
    def __init__(self, yFun, t0, y0, t_bound, max_step = np.inf, rtol = None, atol = None, vectorized = False, h = None):
        super(ForwardEuler, self).__init__(yFun, t0, y0, t_bound, vectorized, support_complex = True)
        self.h = h if h is not None else (t_bound - t0) / 100
        self.dir = 1
        #self.n = len(y0)

    def _step_impl(self):
        y_new = self.y + self.h * self.fun(self.t, self.y)
        self.t += self.h * self.dir
        self.y = y_new
        return True, None
        #return True, self.y
        #return True, self.h#self.dir * (self.t + self.h)
    
    def _dense_output_impl(self):
        return ForwardEulerOutput(self.t, self.y)