from py_wake.site import UniformSite
from py_wake.wind_turbines import WindTurbine
from py_wake import NOJ
import matplotlib.pyplot as plt
import numpy as np
import os
from off2pywake_support import build_farm_setup, load_windfarm_yaml, StaticCpCtYawPower
from py_wake.examples.data.hornsrev1 import Hornsrev1Site, V80, wt_x, wt_y, wt16_x, wt16_y
from py_wake.deficit_models.gaussian import BastankhahGaussian


from py_wake.wind_turbines import WindTurbines
from py_wake.wind_turbines.power_ct_functions import (
    PowerCtTabular,
    YawPowerCtFunction
)

if __name__ == "__main__": 
    os.system('cls' if os.name == 'nt' else 'clear')

    ws = 8  # wind speed
    wd = 270  # wind direction
    ti = 0.1  # turbulence intensity

    farm_dictionary = load_windfarm_yaml("windfarm_information_2x5.yaml")
    setup = build_farm_setup(farm_dictionary)

    site = UniformSite(ws=ws, ti=ti) # wd is given later in the simulation


    ws_array = np.array([ws])
    power = np.array([0.47*ws**3*])
    ct = np.array([0.74])

    base_power_ct = PowerCtTabular(ws, power, ct)

    
    windTurbines = WindTurbine(
        name="CustomTurbine",
        diameter=setup["diameter"],
        hub_height=setup["hub_height"],
        powerCtFunction=StaticCpCtYawPower()
    )

    # windTurbines = V80()
    # site = Hornsrev1Site()
    layout_x = setup["layout_x"]
    layout_y = setup["layout_y"]


    wfm = BastankhahGaussian(site, windTurbines)

    #here we import the turbine, site and wake deficit model to use.

    simulationResult = wfm(
    x=layout_x,
    y=layout_y,
    wd=[270]   # constant wind direction [deg]
    )

    simulationResult.aep()

    print ("Total AEP: %f GWh"%simulationResult.aep().sum())


    flow_map = simulationResult.flow_map(ws=ws, wd=wd)
    plt.figure(figsize=(18,10))
    flow_map.plot_wake_map()
    plt.xlabel('x [m]')
    plt.ylabel('y [m]')
    plt.title('Wake map for' + f' {ws} m/s and {wd} deg')

    plt.show()