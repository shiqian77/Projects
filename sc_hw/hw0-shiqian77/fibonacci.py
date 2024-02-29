"""
fibonacci

functions to compute fibonacci numbers

Complete problems 2 and 3 in this file.
"""

import time # to compute runtimes
from tqdm import tqdm # progress bar
import numpy as np
from egyptian import egyptian_multiplication
import math
import matplotlib.pyplot as plt

# Question 2
'''
This function uses a recursive technique to calculate the nth Fibonacci number. It returns 0 if n is equal to zero, 1 if n is equal to one, and recursively computes the Fibonacci numbers for other n values.
'''
def fibonacci_recursive(n):
    if n == 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fibonacci_recursive(n-1) + fibonacci_recursive(n-2)


# Question 2
'''
This function uses an iterative strategy to calculate the nth Fibonacci number. It returns 0 for n = 0, 1 for n = 1, and recursively computes the Fibonacci numbers for other values of n by keeping track of the previous two Fibonacci numbers in two variables, previous and now, and updating them in a loop until the desired Fibonacci number is reached.
'''
def fibonacci_iter(n):
    if n == 0:
        return 0
    elif n == 1:
        return 1
    else:
        previous = 0
        now = 1
        for x in range (2,n+1):
            nextone = previous + now
            previous = now
            now = nextone
        return now

if __name__ == '__main__':
    n = 30
    print('Print the sequence by using iteration method:')
    for x in range(0,n):
        res1 = fibonacci_iter(x)
        print('{}'.format(res1), end = '')
        if x!= n-1:
            print(',',end = '')
    print()
    
    print('Print the sequence by using recursive method:')
    for x in range(0,n):
        res2 = fibonacci_recursive(x)
        print('{}'.format(res2), end = '')
        if x!= n-1:
            print(',',end = '')

# Question 3
def fibonacci_power(n):
    '''
    x_n = [F_n, F_{n-1}]^T
    x_n-1 = [F_n-1, F_{n-2}]^T
    x_n  =  A x_n-1 (1)
    x_n-1 = A x_n-2 (2)
    plug in (2) into (1)
    x_n = A A x_n-2
    x_n =  A**2 x_n-2
    note: 2+n-2=n
    then we will ultimately get x_n = A**n-1 x_1 since n-1+1=n
    Perform Egyptian multiplication between two matrix elements from matrices A_n_1 and A, and update the corresponding element in the matrix A_n_1.
    '''
    
    x_1 = np.array([[1],[0]])
    A = np.array([[1,1],[1,0]])
    A_n_1 = A
    if n == 0:
        return 0
    for x in range(2,n):
        a = egyptian_multiplication(A_n_1.item((0,0)),A.item((0,0)))
        b = egyptian_multiplication(A_n_1.item((0,1)),A.item((1,0)))
        add1 = a + b
        c = egyptian_multiplication(A_n_1.item((0,0)),A.item((0,1)))
        d = egyptian_multiplication(A_n_1.item((0,1)),A.item((1,1)))
        add2 = c + d
        e = egyptian_multiplication(A_n_1.item((1,0)),A.item((0,0)))
        f = egyptian_multiplication(A_n_1.item((1,1)),A.item((1,0)))
        add3 = e + f
        g = egyptian_multiplication(A_n_1.item((1,0)),A.item((0,1)))
        h = egyptian_multiplication(A_n_1.item((1,1)),A.item((1,1)))
        add4 = g + h
        A_n_1 = np.array([[add1,add2],[add3,add4]]) ## Finally, update A_n_1 with a new 2x2 matrix
    return A_n_1.item((0,0)) ## The first element of x_n is F_n, which is what we want
    
    
if __name__ == '__main__':
    """
    this section of the code only executes when
    this file is run as a script.
    """
    def get_runtimes(ns, f):
        """
        get runtimes for fibonacci(n)

        e.g.
        trecursive = get_runtimes(range(30), fibonacci_recusive)
        will get the time to compute each fibonacci number up to 29
        using fibonacci_recursive
        """
        ts = []
        for n in tqdm(ns):
            t0 = time.time()
            fn = f(n)
            t1 = time.time()
            ts.append(t1 - t0)

        return ts


    nrecursive = range(35)
    trecursive = get_runtimes(nrecursive, fibonacci_recursive)

    niter = range(10000)
    titer = get_runtimes(niter, fibonacci_iter)

    npower = range(10000)
    tpower = get_runtimes(npower, fibonacci_power)

    ## write your code for problem 4 below...
    '''
    plot the runtime of three functions(iteration, recursion,power) to cumpute Fibonacci sequence
    '''
    plt.loglog(nrecursive,trecursive, label='frecursive')
    plt.loglog(niter,titer, label='fiteration')
    plt.loglog(npower,tpower, label='fpower')
    plt.legend()
    plt.xlabel('n')
    plt.ylabel('runtime')
    plt.title('fibonacci analysis')
    #plt.show()
    plt.savefig('fibonacci_runtime.png')
