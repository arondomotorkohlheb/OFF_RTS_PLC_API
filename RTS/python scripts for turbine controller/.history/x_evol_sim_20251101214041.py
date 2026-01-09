JT = 1


def tau_aero(ctau, rho = 1.225, ):
    """
    Calculate the aerodynamic stopping time (tau_aero) for a particle.

    Parameters:
    ctau : float
        Dimensionless stopping time coefficient.
    rho : float
        Gas density (kg/m^3).
    r : float
        Particle radius (m).
    v_rel : float
        Relative velocity between the particle and the gas (m/s).
    c_d : float, optional
        Drag coefficient (default is 1.0).

    Returns:
    float
        Aerodynamic stopping time (s).
    """
    tau = ctau * (4.0 * r * rho) / (3.0 * c_d * v_rel)
    return tau