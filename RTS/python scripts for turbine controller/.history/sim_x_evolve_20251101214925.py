def tau_aero(ctau, rho = 1.225, A = 1, V =1):
return ctau * 0.5 * rho * A * V**2

def omega_dot(tau, J = JT):
return tau / J