

def tau_aero(beta, omega, rho = 1.225, A = 1, V =1):
    return ctau * 0.5 * rho * A * V**2

def tau_gen(omega, Pref):
    return Pref / omega

def omega_dot(tau, J = JT):
    return tau / J