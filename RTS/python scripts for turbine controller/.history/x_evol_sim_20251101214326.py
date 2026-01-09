JT = 1

IEA-22-280-RWT_Cp_Ct_Cq.txt
def ctau(beta, lambda_):
    return beta * lambda_

def tau_aero(ctau, rho = 1.225, A = 1, V =1):
    return ctau * 0.5 * rho * A * V**2

def omega_dot(tau, J = JT):
    return tau / J