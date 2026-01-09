

import numpy as np


ctau = np.load('ctau.npy')
betas = np.load('betas.npy')
lambdas = np.load('lambdas.npy')

def ctau_func(beta, lambda_):
    # bilinear interpolation of ctau over betas and lambdas
    return np.interp(beta, betas, np.interp(lambda_, lambdas, ctau, axis=0), axis=0)

def tau_aero(beta, omega, rho = 1.225, A = 1, V =1):
    return ctau * 0.5 * rho * A * V**2

def tau_gen(omega, Pref):
    return Pref / omega

def omega_dot(tau, J = 1):
    return tau / J

