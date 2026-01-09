from py_wake.site import UniformSite
from py_wake.wind_turbines import WindTurbine
from py_wake import NOJ
import matplotlib.pyplot as plt
import numpy as np
import os
from off2pywake_support import build_farm_setup, load_windfarm_yaml, rotate_points
from py_wake.deficit_models.gaussian import BastankhahGaussian
from py_wake.deflection_models import JimenezWakeDeflection
from py_wake.wind_turbines import WindTurbines
from py_wake.wind_turbines.power_ct_functions import PowerCtTabular
from py_wake.examples.data.hornsrev1 import V80
from py_wake.examples.data.iea37._iea37 import IEA37Site, IEA37_WindTurbines
from py_wake.turbulence_models import STF2017TurbulenceModel


if __name__ == "__main__": 
    os.system('cls' if os.name == 'nt' else 'clear')

    ws = 8  # wind speed
    wd = 90  # wind direction
    ti = 0  # turbulence intensity

    farm_dictionary = load_windfarm_yaml("windfarm_information_2x5.yaml")
    setup = build_farm_setup(farm_dictionary)

    site = UniformSite(ws=ws, ti=ti) # wd is given later in the simulation


    ws_array = np.array([ws])
    power = np.array([0.47*ws**3*setup["A"]*1.225])  # in MW
    ct = np.array([0.74])

    power_ct = PowerCtTabular(ws = ws_array, power = power, ct = ct, power_unit='MW')

    windTurbines = WindTurbines(
        names=['Turbine'],
        diameters=[setup["diameter"]],
        hub_heights=[setup["hub_height"]],
        powerCtFunctions=[power_ct]
    )


    # windTurbines = V80()
    # site = Hornsrev1Site()
    layout_x = setup["layout_x"]
    layout_y = setup["layout_y"]

    # create the order of turbines based on their positions and winf direction
    wind_aligned_distance = np.zeros_like(layout_y)
    for i in range(len(layout_x)):
        _, wind_aligned_distance[i] = rotate_points(layout_x[i], layout_y[i], -wd)
        wind_aligned_distance[i] = -1*wind_aligned_distance[i]

    opt_order = np.argsort(wind_aligned_distance)
    print('Turbine order based on wind direction:')
    for i in opt_order:
        print(f'Turbine {i}: x = {layout_x[i]}, y = {layout_y[i]}')

    wfm = BastankhahGaussian(site, windTurbines, deflectionModel=JimenezWakeDeflection(), turbulenceModel=STF2017TurbulenceModel())

    #here we import the turbine, site and wake deficit model to use.

    # 0 relative yaw as a starting point
    yaws = [0 for _ in range(setup["n_turbines"])] 

    simulationResult = wfm(
    x=layout_x,
    y=layout_y,
    wd=[wd],   # constant wind direction [deg]
    yaw=yaws,
    tilt = 0
    )

    # get the average sum power generated
    sumpower = simulationResult.Power.sum().values
    
    # find the best yaw for the 'first' turbine in the wind direction
    best_yaw = 0
    best_power = sumpower
    left_end_point = -30
    right_end_point = 30

    for yaw in range(-30,31,5):
        yaws_opt = yaws.copy()
        yaws_opt[opt_order[0]] = yaw
        simulationResult_opt = wfm(
            x=layout_x,
            y=layout_y,
            wd=[wd],   # constant wind direction [deg]
            yaw=yaws_opt,
            tilt = 0
        )
        sumpower_opt = simulationResult_opt.Power.sum().values
        if sumpower_opt > best_power:
            best_power = sumpower_opt
            best_yaw = yaw

    exit()


    flow_map = simulationResult.flow_map(ws=ws, wd=wd)

    # get summa power
    total_power = simulationResult.Power.values.sum()
    print(f'Total Power Output: {total_power} MW')
    flow_map.plot_wake_map()
    plt.xlabel('x [m]')
    plt.ylabel('y [m]')
    plt.title('Wake map for' + f' {ws} m/s and {wd} deg')

    # get the turbulence intensity at each turbine
    tis = simulationResult.TI_eff.values.squeeze()
    for i, ti in enumerate(tis):
        print(f'Turbine {i+1}: Effective Turbulence Intensity = {ti}')

    plt.show()