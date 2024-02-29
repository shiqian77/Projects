import numpy as np
import scipy as sp
from scipy.interpolate import interp1d, BarycentricInterpolator
from scipy.special import roots_chebyt, roots_legendre
from scipy.integrate import newton_cotes
import matplotlib.pyplot as plt

class WrapperBaryCentricInterpolator:
    def __init__(self, f, I, n, way = "Chebyshev"):
        self.fun = f
        self.interval = I
        self.n = n
        self.way = way
        if self.way == "Chebyshev":
            nodes, _ = roots_chebyt(n)
        elif self.way == "Legendre":
            nodes, _ = roots_legendre(n)
        else:
            nodes = np.linspace(self.interval[0], self.interval[1], n)
            #nodes = np.linspace(-1, 1, n)
        self.nodes = I[0] + (I[1] - I[0]) * 0.5 * (nodes + 1)
        self.values = f(self.nodes)
        self.res = BarycentricInterpolator(self.nodes, self.values)
        
    def __call__(self, x):
        return self.res(x)
    
    def __str__(self):
        return "The {0} interpolation with {1} nodes on internal [{2}, {3}]".format(self.way, self.n, self.interval[0], self.interval[1])



class WrapperInterp1d:
    def __init__(self, f, I, n):
        self.fun = f
        self.n = n
        self.interval = I
        
        self.nodes = np.linspace(I[0], I[1], n)
        self.values = f(self.nodes)
        self.res = interp1d(self.nodes, self.values)
    
    def __call__(self, x):
        return self.res(x)
    
    def __str__(self):
        return "The linear interpolant with {0} equi-spaced nodes on interval [{1}, {2}]".format(self.n, self.interval[0], self.interval[1])
    
#1
class ReviseBaryCentricInterpolator:
    def __init__(self, f, I, n, way="Chebyshev"):
        self.fun = f
        self.interval = I
        self.n = n
        self.way = way
        if self.way == "Chebyshev":
            raise ValueError("No this way, skip")
        elif self.way == "Legendre":
            nodes, _ = roots_legendre(n)
            _, self.weights = roots_legendre(n)
        else:
            self.weights, _ = newton_cotes(n, equal = 1)
            nodes = np.linspace(self.interval[0], self.interval[1], n+1)
            #_, self.weights = newton_cotes(n-1)  # get the weights for n nodes
        self.nodes = I[0] + (I[1] - I[0]) * 0.5 * (nodes + 1)
        self.values = f(self.nodes)
        self.res = BarycentricInterpolator(self.nodes, self.values)

    def quad(self):
        h = (self.interval[1] - self.interval[0]) / 2
        return h * np.sum(self.weights * self.values)

    def __call__(self, x):
        return self.res(x)

    def __str__(self):
        return "The {0} Integral with {1} nodes on internal [{2}, {3}]".format(self.way, self.n, self.interval[0], self.interval[1])

class ReviseInterp1d:
    def __init__(self, f, I, n):
        self.fun = f
        self.n = n
        self.interval = I
        self.nodes = np.linspace(I[0], I[1], n)
        self.values = f(self.nodes)
        h = (self.interval[1] - self.interval[0]) / (self.n - 1)
        self.weights = np.array([h/2] + [h] * (self.n - 2) + [h/2])
        self.res = interp1d(self.nodes, self.values)

    def quad(self):
        return np.sum(self.weights * self.values)

    def __call__(self, x):
        return self.res(x)

    def __str__(self):
        return "The Integral interpolant with {0} equi-spaced nodes on interval [{1}, {2}]".format(self.n, self.interval[0], self.interval[1])
        



