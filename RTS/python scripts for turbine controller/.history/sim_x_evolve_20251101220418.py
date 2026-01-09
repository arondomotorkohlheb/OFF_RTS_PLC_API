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

    beta1 = betas[beta_idx]
    beta2 = betas[beta_idx + 1] if beta_idx + 1 < len(betas) else beta_idx
    lambda1 = lambdas[lambda_idx]
    lambda2 = lambdas[lambda_idx + 1] if lambda_idx + 1 < len(lambdas) else lambda_idx

    Q11 = ctau[lambda_idx, beta_idx]
    Q12 = ctau[lambda_idx, beta_idx + 1]
    Q21 = ctau[lambda_idx + 1, beta_idx]
    Q22 = ctau[lambda_idx + 1, beta_idx + 1]

    return (Q11 * (beta2 - beta) * (lambda2 - lam) +
            Q21 * (beta2 - beta) * (lam - lambda1) +
            Q12 * (beta - beta1) * (lambda2 - lam) +
            Q22 * (beta - beta1) * (lam - lambda1)) / ((beta2 - beta1) * (lambda2 - lambda1))


    # beta_idx = (np.abs(betas - beta)).argmin()
    # lambda_idx = (np.abs(lambdas - lam)).argmin()
    # return ctau[lambda_idx, beta_idx]



print(ctau_func(5, 6))

JT = 100

def tau_aero(beta, omega, rho = 1.225, A = 63, V =10, R = 5):
    return ctau_func(beta, omega*R/V) * 0.5 * rho * A * V**2

def tau_gen(omega, Pref):
    return Pref / omega

def omega_dot(tau, J = JT):
    return tau / J

for t in range