import numpy as np

betas = np.loadtxt('betas.txt')
lambdas = np.loadtxt('lambdas.txt')
ctau = np.loadtxt('ctau.txt')

betas = np.loadtxt('betas.txt', dtype=float)
lambdas = np.loadtxt('lambdas.txt', dtype=float)

def 

print(ctau_func(5, 6))

# def tau_aero(beta, omega, rho = 1.225, A = 1, V =1):
#     return ctau * 0.5 * rho * A * V**2

# def tau_gen(omega, Pref):
#     return Pref / omega

# def omega_dot(tau, J = 1):
#     return tau / J