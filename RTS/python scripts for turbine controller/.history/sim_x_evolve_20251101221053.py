import numpy as np

betas = np.loadtxt('betas.txt')
lambdas = np.loadtxt('lambdas.txt')
ctau = np.loadtxt('ctau.txt')

betas = np.loadtxt('betas.txt', dtype=float)
lambdas = np.loadtxt('lambdas.txt', dtype=float)

def ctau_func(beta, lam):
    # Find the closest indices for beta and lambda
    # beta_idx = (np.abs(betas - beta)).argmin()
    # lambda_idx = (np.abs(lambdas - lam)).argmin()

    # beta1 = betas[beta_idx]
    # beta2 = betas[beta_idx + 1] if beta_idx + 1 < len(betas) else beta_idx
    # lambda1 = lambdas[lambda_idx]
    # lambda2 = lambdas[lambda_idx + 1] if lambda_idx + 1 < len(lambdas) else lambda_idx

    # Q11 = ctau[lambda_idx, beta_idx]
    # Q12 = ctau[lambda_idx, beta_idx + 1]
    # Q21 = ctau[lambda_idx + 1, beta_idx]
    # Q22 = ctau[lambda_idx + 1, beta_idx + 1]

    # return (Q11 * (beta2 - beta) * (lambda2 - lam) +
    #         Q21 * (beta2 - beta) * (lam - lambda1) +
    #         Q12 * (beta - beta1) * (lambda2 - lam) +
    #         Q22 * (beta - beta1) * (lam - lambda1)) / ((beta2 - beta1) * (lambda2 - lambda1))


    beta_idx = (np.abs(betas - beta)).argmin()
    lambda_idx = (np.abs(lambdas - lam)).argmin()
    return ctau[lambda_idx, beta_idx]



print(ctau_func(5, 6))

JT = 100

def tau_aero(beta, omega, rho = 1.225, A = 63, V =1, R = 5):
    return ctau_func(beta, omega*R/V) * 0.5 * rho * A * V**2

def tau_gen(omega, Pref):
    return Pref / omega

def omega_dot(tau, J = JT):
    return tau / J


betadot = 0.0
beta = 5.0
omega = 30.0
Pref = 0
for t in range(1000):
    omega += omega_dot(tau_aero(beta, omega) - tau_gen(omega, Pref)) * 0.1
    beta += betadot * 0.1
    if t == 0:
        omega_values = [omega]
        beta_values = [beta]
    else:
        omega_values.append(omega)
        beta_values.append(beta)


import matplotlib.pyplot as plt
t = np.arange(len(omega_values)) * 0.1

plt.figure(figsize=(8, 4))
plt.plot(t, omega_values, label='omega (rad/s)')
plt.plot(t, beta_values, label='beta (deg)')
plt.xlabel('time (s)')
plt.ylabel('value')
plt.title('Omega and Beta vs Time')
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()