"""
matlib.py

Put any requested function or class definitions in this file.  You can use these in your script.

Please use comments and docstrings to make the file readable.
"""
"""
matlib.py

Put any requested function or class definitions in this file.  You can use these in your script.

Please use comments and docstrings to make the file readable.
"""

import scipy.linalg as la
import matplotlib.pyplot as plt
import numpy as np
import time
from scipy.linalg import cholesky
import math
from scipy.stats import norm
from scipy.linalg import eigh
from scipy.linalg import eigvalsh

# Problem 0
def matrixandeigenvalue(n, howmanymatrices, part):
    e = []
    for x in range(howmanymatrices):
        A = np.random.normal(0,1,size = (n,n))
        B = np.maximum(A,A.transpose()) #symmetric matrix 
        e_value = eigvalsh(B)  # Compute only the eigenvalue
        #e_value , e_vector = la.eig(B)
        if part == 'a':
            for x in e_value:
                e.append(x)
        elif part == 'b':
            #e.append(max(e_value))
            e.append(e_value[-1]) # compute only the largest eigenvalue 
        elif part == 'c':
            e_value.sort()
            #sorted(e_value)
            max_gap = 0
            for y in range(1, len(e_value)):
                max_gap = max(max_gap, e_value[y]-e_value[y-1]) ## compute the largest gap between consecutive eigenvalues
            e.append(max_gap)
        elif part == 'd':
            U, S, V = la.svd(B)
            #row, col = np.shape(S)
            #e.append(min(row,col))
            e.extend(S)
        elif part == 'e':
            U, S, V = la.svd(B)
            condition_num = S[0] / S[-1]
            e.append(condition_num)
            #row, col = np.shape(S)
            #condition_num = S[0][0]/S[min(row-1,col-1)][min(row-1,col-1)]
    return e

 
# Problem 1

# Part A...

def solve_chol(A,b):
  U = cholesky(A, lower = False)
  U_T = U.transpose()
  y = la.solve(U_T, b)
  x = la.solve(U, y)
  return x

def comparison():
    nn = np.round(np.logspace(1, np.log10(2000), 10), 0).astype(int)
    t_lu = []
    t_cho = []

    for x in nn:
        A = np.random.randn(x, x)
        A = A @ A.transpose()

        t0 = time.time()
        la.lu(A)
        t1 = time.time()
        t_lu.append(t1-t0)

        t0 = time.time()
        la.cholesky(A)
        t1 = time.time()
        t_cho.append(t1-t0)

    return nn, t_lu, t_cho

def main():
    nn, t_lu, t_cho = comparison()

    plt.loglog(nn, t_lu, label='LU')
    plt.loglog(nn, t_cho, label='Cholesky')
    plt.legend()
    plt.xlabel('Size of matrix (n)')
    plt.ylabel('Time taken (s)')
    plt.title('Time comparison between LU and Cholesky decompositions')
    plt.show()

  

# Part C...  
def matrix_pow(A,n):
  e_value,Q = la.eigh(A)
  L = np.diag(e_value)
  QT = np.linalg.inv(Q)
  R = Q 
  for x in range(1,n+1):
    R = R @ L
  R = R @ QT
  return R
  
# Part D... 
def abs_det(A):
  P, L, U = la.lu(A)
  det = 1
  row, col = np.shape(L)
  for x in range(0,min(row,col)):
    det = L[x][x] * det
  row, col = np.shape(U)
  for x in range(0,min(row,col)):
    det = U[x][x] * det
  return abs(det)

# Problem 2
# Part A...
class my_complex:
  def __init__(self, real, imaginary):
    self.r = real
    self.i = imaginary
  def __add__(self,other):
    return my_complex(self.r + other.r, self.i + other.i)
  def __mul__(self,other):
    return my_complex(self.r * other.r - self.i * other.i, self.r * other.i + self.i * other.r)
  def conj(self):
    return my_complex(self.r, -self.i)
  def real(self):
    return self.r
  def imag(self):
    return self.i
  def __repr__(self):
    return f'{self.r} + {self.i}i'

# Part B...
def generate_favourite(n):
    listta = []
    for x in range(1, n+1):
        listta.append(my_complex(x, 7*x))
    return listta

def generate_favourite_np(n):
    listta = np.empty((0,n), np.cdouble)
    for x in range(1, n+1):
        num = np.cdouble((x,7*x))
        listta.append(num)
    return listta

def dot_p_v(V1, V2):
  result = my_complex(0,0)
  row1, col1 = np.shape(V1)
  row2, col2 = np.shape(V2)
  if row1 != row2 or col1 != col2:
    return 'MLGB'
  for x in range (0, row1):
    for y in range(0, col1):
      dp = V1[x][y] * V2[x][y]
      result += dp
  return result






      
  






      
  
