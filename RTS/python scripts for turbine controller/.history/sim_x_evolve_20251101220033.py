import numpy as np

betas = np.loadtxt('betas.txt')
lambdas = np.loadtxt('lambdas.txt')
ctau = np.loadtxt('ctau.txt')

betas = np.loadtxt('betas.txt', dtype=float)
lambdas = np.loadtxt('lambdas.txt', dtype=float)

def ctau_func(beta, lam):
    # Find the closest indices for beta and lambda
    
    beta_idx = (np.abs(betas - beta)).argmin()
    lambda_idx = (np.abs(lambdas - lam)).argmin()
    return ctau[lambda_idx, beta_idx]



print(ctau_func(5, 6))

# def tau_aero(beta, omega, rho = 1.225, A = 1, V =1):
#     return ctau * 0.5 * rho * A * V**2

# def tau_gen(omega, Pref):
#     return Pref / omega

# def omega_dot(tau, J = 1):
#     return tau / J