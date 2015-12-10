__author__ = 'JoaoCosta'

import scipy as sp
from scipy import linalg
from scipy import sparse
from scipy.sparse import lil_matrix as lil_wayne
import pylab as pl

def potential_well(X, Y, x0, y0, a, b, v0):
    V = sp.zeros(X.shape)
    indexes = sp.where(((X-x0)/a)**2 + ((Y-y0)/b)**2 > 1.0)
    V[indexes] = v0
    return V

def absorving_borders_box(X, Y, xyL, vM):
    x = abs(X)
    y = abs(Y)
    B = sp.zeros(X.shape, dtype = complex)
    id = sp.where(x > x - xyL)
    B[id] += (x[id] - (x[id]-xyL))**2
    id = sp.where(y > y - xyL)
    B[id] += (y[id] - (y[id]-xyL))**2
    return 1j*vM*B


def ravelIdx(idx, shape):
    idx = [shape[i] + idx[i] if idx[i] < 0 else idx[i] for i in range(len(idx))]
    I = 0
    dim = 1
    for i in range(-1, -len(idx) - 1, -1):
        I += idx[i]*dim
        dim *= shape[i]
    return I

def laplacianMatrix(shape):
    L = sp.zeros((shape[0]*shape[1], shape[0]*shape[1]))

    for i in range(1, shape[0] - 1):
        for j in range(1, shape[1] - 1):
            L[ravelIdx((i, j), shape), ravelIdx((i, j), shape)] -= 4
            L[ravelIdx((i, j), shape), ravelIdx((i, j - 1), shape)] += 1
            L[ravelIdx((i, j), shape), ravelIdx((i, j + 1), shape)] += 1
            L[ravelIdx((i, j), shape), ravelIdx((i - 1, j), shape)] += 1
            L[ravelIdx((i, j), shape), ravelIdx((i + 1, j), shape)] += 1

    for i in range(1, shape[0] - 1):
        L[ravelIdx((i, 0), shape), ravelIdx((i - 1, 0), shape)] += 1
        L[ravelIdx((i, 0), shape), ravelIdx((i + 1, 0), shape)] += 1

        L[ravelIdx((i, 0), shape), ravelIdx((i, 1), shape)] -= 5
        L[ravelIdx((i, 0), shape), ravelIdx((i, 2), shape)] += 4
        L[ravelIdx((i, 0), shape), ravelIdx((i, 3), shape)] -= 1


        L[ravelIdx((i, -1), shape), ravelIdx((i - 1, -1), shape)] += 1
        L[ravelIdx((i, -1), shape), ravelIdx((i + 1, -1), shape)] += 1

        L[ravelIdx((i, -1), shape), ravelIdx((i, -2), shape)] -= 5
        L[ravelIdx((i, -1), shape), ravelIdx((i, -3), shape)] += 4
        L[ravelIdx((i, -1), shape), ravelIdx((i, -4), shape)] -= 1


    for j in range(1, shape[1] - 1):
        L[ravelIdx((0, j), shape), ravelIdx((0, j - 1), shape)] += 1
        L[ravelIdx((0, j), shape), ravelIdx((0, j + 1), shape)] += 1

        L[ravelIdx((0, j), shape), ravelIdx((1, j), shape)] -= 5
        L[ravelIdx((0, j), shape), ravelIdx((2, j), shape)] += 4
        L[ravelIdx((0, j), shape), ravelIdx((3, j), shape)] -= 1


        L[ravelIdx((-1, j), shape), ravelIdx((-1, j - 1), shape)] += 1
        L[ravelIdx((-1, j), shape), ravelIdx((-1, j + 1), shape)] += 1

        L[ravelIdx((-1, j), shape), ravelIdx((-2, j), shape)] -= 5
        L[ravelIdx((-1, j), shape), ravelIdx((-3, j), shape)] += 4
        L[ravelIdx((-1, j), shape), ravelIdx((-4, j), shape)] -= 1


    L[ravelIdx(( 0,  0), shape), ravelIdx(( 0,  0), shape)] += 4
    L[ravelIdx(( 0,  0), shape), ravelIdx(( 0,  1), shape)] -= 5
    L[ravelIdx(( 0,  0), shape), ravelIdx(( 1,  0), shape)] -= 5
    L[ravelIdx(( 0,  0), shape), ravelIdx(( 0,  2), shape)] += 4
    L[ravelIdx(( 0,  0), shape), ravelIdx(( 2,  0), shape)] += 4
    L[ravelIdx(( 0,  0), shape), ravelIdx(( 0,  3), shape)] -= 1
    L[ravelIdx(( 0,  0), shape), ravelIdx(( 3,  0), shape)] -= 1

    L[ravelIdx(( 0, -1), shape), ravelIdx(( 0, -1), shape)] += 4
    L[ravelIdx(( 0, -1), shape), ravelIdx(( 0, -2), shape)] -= 5
    L[ravelIdx(( 0, -1), shape), ravelIdx(( 1, -1), shape)] -= 5
    L[ravelIdx(( 0, -1), shape), ravelIdx(( 0, -3), shape)] += 4
    L[ravelIdx(( 0, -1), shape), ravelIdx(( 2, -1), shape)] += 4
    L[ravelIdx(( 0, -1), shape), ravelIdx(( 0, -4), shape)] -= 1
    L[ravelIdx(( 0, -1), shape), ravelIdx(( 3, -1), shape)] -= 1

    L[ravelIdx((-1,  0), shape), ravelIdx((-1,  0), shape)] += 4
    L[ravelIdx((-1,  0), shape), ravelIdx((-1,  1), shape)] -= 5
    L[ravelIdx((-1,  0), shape), ravelIdx((-2,  0), shape)] -= 5
    L[ravelIdx((-1,  0), shape), ravelIdx((-1,  2), shape)] += 4
    L[ravelIdx((-1,  0), shape), ravelIdx((-3,  0), shape)] += 4
    L[ravelIdx((-1,  0), shape), ravelIdx((-1,  3), shape)] -= 1
    L[ravelIdx((-1,  0), shape), ravelIdx((-4,  0), shape)] -= 1

    L[ravelIdx((-1, -1), shape), ravelIdx((-1, -1), shape)] += 4
    L[ravelIdx((-1, -1), shape), ravelIdx((-1, -2), shape)] -= 5
    L[ravelIdx((-1, -1), shape), ravelIdx((-2, -1), shape)] -= 5
    L[ravelIdx((-1, -1), shape), ravelIdx((-1, -3), shape)] += 4
    L[ravelIdx((-1, -1), shape), ravelIdx((-3, -1), shape)] += 4
    L[ravelIdx((-1, -1), shape), ravelIdx((-1, -4), shape)] -= 1
    L[ravelIdx((-1, -1), shape), ravelIdx((-4, -1), shape)] -= 1

    return L

if __name__ == '__main__':

    # Problem definition
    v0 = 100.0
    delta = 0.5
    a = 1.0 + delta
    b = 1.0
    x0 = 0.0
    y0 = 0.0

    xyMin = -3.0
    xyMax = 3.0
    dxy = 0.1
    X, Y = sp.mgrid[xyMin:xyMax:dxy, xyMin:xyMax:dxy]

    L = laplacianMatrix(X.shape)
    V = sp.diag((potential_well(X, Y, x0, y0, a, b, v0) + absorving_borders_box(X, Y, 1.0, 200)).ravel())
    H = -L + V

    energies, states = linalg.eig(H)
    indexes = energies.argsort()
    energies = energies(indexes)
    states = states[:, indexes]

    psi1 = states[0]

    pl.figure()
    pl.contourf(X,Y, psi1)
    pl.show()