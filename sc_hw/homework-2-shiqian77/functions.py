"""
A library of functions
"""
import numpy as np
import matplotlib.pyplot as plt
import numbers

class AbstractFunction:
    """
    An abstract function class
    """

    def derivative(self):
        """
        returns another function f' which is the derivative of x
        """
        raise NotImplementedError("derivative")


    def __str__(self):
        return "AbstractFunction"


    def __repr__(self):
        return "AbstractFunction"


    def evaluate(self, x):
        """
        evaluate at x

        assumes x is a numeric value, or numpy array of values
        """
        raise NotImplementedError("evaluate")


    def __call__(self, x):
        """
        if x is another AbstractFunction, return the composition of functions

        if x is a string return a string that uses x as the indeterminate

        otherwise, evaluate function at a point x using evaluate
        """
        if isinstance(x, AbstractFunction):
            return Compose(self, x)
        elif isinstance(x, str):
            return self.__str__().format(x)
        else:
            return self.evaluate(x)


    # the rest of these methods will be implemented when we write the appropriate functions
    def __add__(self, other):
        """
        returns a new function expressing the sum of two functions
        """
        return Sum(self, other)


    def __mul__(self, other):
        """
        returns a new function expressing the product of two functions
        """
        return Product(self, other)


    def __neg__(self):
        return Scale(-1)(self)


    def __truediv__(self, other):
        return self * other**-1


    def __pow__(self, n):
        return Power(n)(self)


    def plot(self, vals=np.linspace(-1,1,100), **kwargs):
        """
        plots function on values
        pass kwargs to plotting function
        """
        num = self.evaluate(vals)
        return plt.plot(vals, num, **kwargs)
        #raise NotImplementedError("plot")

    def taylor_series(self, x0, deg=5):
        """
        Returns the Taylor series of f centered at x0 truncated to degree k
        """
        f0 = self.evaluate(x0)#this is the first term, special cased to avoid 0 power
        terms = [0]*(deg+1)#k degree Taylor series has k+1 terms
        terms[0] = Constant(f0)
        offset = Polynomial(1, x0)
        for i in range(deg+1):#loop puts each element of the sum in terms[]
            if i == 0:#base case
                pass
            else:
                ith_deriv = self#initialize i_th deriv
                for j in range(i):#takes i_th derivative of f
                   ith_deriv = ith_deriv.derivative()
                ith_deriv = Constant(ith_deriv.evaluate(x0))
                prefactor = Constant((1/np.math.factorial(i)))
                terms[i] = prefactor * ith_deriv * (offset ** i)#completed term
        t_series = np.sum(terms)#sum all of the
        return t_series


class Polynomial(AbstractFunction):
    """
    polynomial c_n x^n + ... + c_1 x + c_0
    """

    def __init__(self, *args):
        """
        Polynomial(c_n ... c_0)

        Creates a polynomial
        c_n x^n + c_{n-1} x^{n-1} + ... + c_0
        """
        self.coeff = np.array(list(args))


    def __repr__(self):
        return "Polynomial{}".format(tuple(self.coeff))


    def __str__(self):
        """
        We'll create a string starting with leading term first

        there are a lot of branch conditions to make everything look pretty
        """
        s = ""
        deg = self.degree()
        for i, c in enumerate(self.coeff):
            if i < deg-1:
                if c == 0:
                    # don't print term at all
                    continue
                elif c == 1:
                    # supress coefficient
                    s = s + "({{0}})^{} + ".format(deg - i)
                else:
                    # print coefficient
                    s = s + "{}({{0}})^{} + ".format(c, deg - i)
            elif i == deg-1:
                # linear term
                if c == 0:
                    continue
                elif c == 1:
                    # suppress coefficient
                    s = s + "{0} + "
                else:
                    s = s + "{}({{0}}) + ".format(c)
            else:
                if c == 0 and len(s) > 0:
                    continue
                else:
                    # constant term
                    s = s + "{}".format(c)

        # handle possible trailing +
        if s[-3:] == " + ":
            s = s[:-3]

        return s


    def evaluate(self, x):
        """
        evaluate polynomial at x
        """
        if isinstance(x, numbers.Number):
            ret = 0
            for k, c in enumerate(reversed(self.coeff)):
                ret = ret + c * x**k
            return ret
        elif isinstance(x, np.ndarray):
            x = np.array(x)
            # use vandermonde matrix
            return np.vander(x, len(self.coeff)).dot(self.coeff)


    def derivative(self):
        if len(self.coeff) == 1:
            return Polynomial(0)
        return Polynomial(*(self.coeff[:-1] * np.array([n+1 for n in reversed(range(self.degree()))])))


    def degree(self):
        return len(self.coeff) - 1


    def __add__(self, other):
        """
        Polynomials are closed under addition - implement special rule
        """
        if isinstance(other, Polynomial):
            # add
            if self.degree() > other.degree():
                coeff = self.coeff
                coeff[-(other.degree() + 1):] += other.coeff
                return Polynomial(*coeff)
            else:
                coeff = other.coeff
                coeff[-(self.degree() + 1):] += self.coeff
                return Polynomial(*coeff)

        else:
            # do default add
            return super().__add__(other)


    def __mul__(self, other):
        """
        Polynomials are clused under multiplication - implement special rule
        """
        if isinstance(other, Polynomial):
            return Polynomial(*np.polymul(self.coeff, other.coeff))
        else:
            return super().__mul__(other)


class Affine(Polynomial):
    """
    affine function a * x + b
    """
    def __init__(self, a, b):
        super().__init__(a, b)

class Compose(AbstractFunction):
    def __init__(self, f, g):
        self.f = f
        self.g = g
    def __repr__(self):
        return "Compose({}, {})".format(self.f, self.g)
    def __str__(self):
        return "{0}({1})".format(self.f,self.g)

    def evaluate(self, x):
        return self.f(self.g(x))
    def derivative(self):
        return Product(Compose(self.f.derivative(), self.g), self.g.derivative())


class Sum(AbstractFunction):
    def __init__(self, f, g):
        self.f = f
        self.g = g
    def evaluate(self, x):
        return self.f(x) + self.g(x)
    def derivative(self):
        return Sum(self.f.derivative(), self.g.derivative())
    def __repr__(self):
        return "Sum({}, {})".format(self.f, self.g)
    def __str__(self):
        return "{0} + {1}".format(str(self.f), str(self.g))
        #return "{0} + {1}".format(str(self.f).replace("{0}", "{{0}}"), str(self.g))

class Product(AbstractFunction):
    def __init__(self, f, g):
        self.f = f
        self.g = g
    def evaluate(self, x):
        return self.f(x) * self.g(x)
    def __repr__(self):
        return "Product({}, {})".format(self.f, self.g)
    def __str__(self):
        return "{0} * {1}".format(self.f, self.g)
        #return "{0} * {1}".format(str(self.f).replace("{0}", "{{0}}"), str(self.g))
    def derivative(self):
        return Sum(Product(self.f.derivative(), self.g), Product(self.f, self.g.derivative()))


class Power(AbstractFunction):
    def __init__(self, p):
        self.power = p
    def evaluate(self, x):
        return np.power(x, self.power)
    def derivative(self):
        return Product(Constant(self.power), Power(self.power - 1))
    def __repr__(self):
        return "Power({0})".format(self.power)
    def __str__(self):
        return "()^{0}".format(self.power)


class Scale(Polynomial):
    def __init__(self, num):
        super().__init__(num, 0)

class Constant(Polynomial):
    def __init__(self, c):
        super().__init__(c)

class Log(AbstractFunction):
    def evaluate(self, num):
        return np.log(num)
    def derivative(self):
        return Reciprocal()
    def __str__(self):
        return "ln({0})"
    def __repr__(self):
        return "Log({0})"

class Reciprocal(AbstractFunction):
    def evaluate(self, x):
        return 1.0 / x
    def _str__(self):
        return "1/{0}"

class Exponential(AbstractFunction):
    def evaluate(self, x):
        return np.exp(x)
    def derivative(self):
        return self
    def __str__(self):
        return "exp({0})"
    def __repr__(self):
        return "Exponential()"

class Sin(AbstractFunction):
    def evaluate(self, x):
        return np.sin(x)
    def derivative(self):
         return Cos()
    def __str__(self):
        return "sin({0})"

    def __repr__(self):
        return "Sin()"

class Cos(AbstractFunction):
    def evaluate(self, x):
        return np.cos(x)
    def derivative(self):
        return Product(Constant(-1),Sin())
    def __str__(self):
        return "cos({0})"
    def __repr__(self):
        return "Cos()"

class Symbolic(AbstractFunction):
    def __init__(self, funcName):
        self.name = funcName;

    def __str__(self):
        return "{fName}({{0}})".format(fName = self.name);

    def __repr__(self):
        return "Symbolic(\"{}\")".format(self.name);

    def __call__(self, *args):
        return "{fName}({fInput})".format(fName = self.name, fInput = ','.join(map(str,args)));

    def derivative(self):
        return Symbolic("{fName}'".format(fName = self.name));







def newton_root(f, x0, tol=1e-8):
    """
    find a point x so that f(x) is close to 0,
    measured by abs(f(x)) < tol

    Use Newton's method starting at point x0
    """

    # If f is not a instance of AbstractFunction, raise an error
    if not (isinstance(f, AbstractFunction)):
        raise ValueError("f needs to be an AbstractFunction");
    # If f is a instance of Symbolic, raise an error
    if (isinstance(f, Symbolic)):
        raise ValueError("f cannot bt a Symbolic");

    x = x0; # Set the starting point to x

    while(True):
        # Newton's method to find the next value of x
        x_new = x - f.evaluate(x) / f.derivative().evaluate(x);
        if abs(f.evaluate(x_new)) < tol: # Check tolerance
            return x_new;
        x = x_new;

def newton_extremum(f, x0, tol=1e-8):
    """
    find a point x which is close to a local maximum or minimum of f,
    measured by abs(f'(x)) < tol

    Use Newton's method starting at point x0
    """

    fPrime = f.derivative(); # Derivative of f
    # Use newton's method to find the root of f derivative
    # The root of f derivative will be a extremum of f
    fPrimeRoot = newton_root(fPrime, x0, tol);

    return fPrimeRoot;


if __name__ == '__main__':

    # Construct our sin(exp(x)) function
    sinExp = Sin()(Exponential());

    # Find the root with newton_root function
    sinExpRoot = newton_root(sinExp, 1.0);
    print("Root of Sin(exp(x)) is {root}.".format(root = sinExpRoot));

    # Plot the sin(exp(x)) function and scatter the root found
    vals = np.linspace(-1,2,100);
    num = sinExp.evaluate(vals);

    plt.plot(vals, num, label = "function sin(exp(x))");
    plt.xlabel("x");
    plt.ylabel("f(x)");
    plt.title("sin(exp(x)) and its root");
    plt.legend();
    plt.scatter(sinExpRoot, sinExp(sinExpRoot));

    plt.show();

    # Find the extremum with newton_extremum function
    sinExpExtrema = newton_extremum(sinExp, 0.0);
    print("Extrema of Sin(exp(x)) is {extrema}.".format(extrema = sinExpExtrema));

    # Plot the sin(exp(x)) function and scatter the extremum found
    plt.plot(vals, num, label = "function sin(exp(x))");
    plt.xlabel("x");
    plt.ylabel("f(x)");
    plt.title("sin(exp(x)) and its extrema");
    plt.legend();
    plt.scatter(sinExpExtrema, sinExp(sinExpExtrema));

    plt.show();
