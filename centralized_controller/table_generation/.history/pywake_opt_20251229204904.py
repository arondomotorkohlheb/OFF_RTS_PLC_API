from py_wake.site import UniformSite
from py_wake.wind_turbines import WindTurbine
from py_wake import NOJ
import matplotlib.pyplot as plt
import numpy as np
import os
from off2pywake_support import build_farm_setup, load_windfarm_yaml
from py_wake.deficit_models.gaussian import BastankhahGaussian
from py_wake.deflection_models import JimenezWakeDeflection
from py_wake.wind_turbines import WindTurbines
from py_wake.wind_turbines.power_ct_functions import PowerCtTabular
from py_wake.examples.data.hornsrev1 import V80
from py_wake.examples.data.iea37._iea37 import IEA37Site, IEA37_WindTurbines


if __name__ == "__main__": 
    os.system('cls' if os.name == 'nt' else 'clear')

    ws = 8  # wind speed
    wd = 200  # wind direction
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


    wfm = BastankhahGaussian(site, windTurbines, deflectionModel=JimenezWakeDeflection())

    #here we import the turbine, site and wake deficit model to use.
    yaws = [20 * (-1)**i for i in range(10)]  # example yaw angles for each turbine in degrees
    simulationResult = wfm(
    x=layout_x,
    y=layout_y,
    wd=[wd],   # constant wind direction [deg]
    yaw=yaws,
    tilt = 0
    )


    flow_map = simulationResult.flow_map(ws=ws, wd=wd)
    plt.figure(figsize=(18,10))
    flow_map.plot_wake_map()
    plt.xlabel('x [m]')
    plt.ylabel('y [m]')
    plt.title('Wake map for' + f' {ws} m/s and {wd} deg')

    # get the turbulence intensity at each turbine
    ti_turbines = simulationResult.ti_eff().values
    for i, ti in enumerate(ti_turbines):
        print(f'Turbine {i+1}: Effective Turbulence Intensity = {ti:.2f} %')

    plt.show()