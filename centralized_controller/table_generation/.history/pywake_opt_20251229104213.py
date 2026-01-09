from py_wake.site import UniformSite, 
from py_wake.wind_turbines import WindTurbine
from py_wake import NOJ
import matplotlib.pyplot as plt
import numpy as np
import os
from off2pywake_support import build_farm_setup, load_windfarm_yaml, StaticCpCtYawPower
from py_wake.examples.data.hornsrev1 import Hornsrev1Site, V80, wt_x, wt_y, wt16_x, wt16_y


if __name__ == "__main__": 
    os.system('cls' if os.name == 'nt' else 'clear')

    ws = 8  # wind speed
    wd = 270  # wind direction
    ti = 0.1  # turbulence intensity

    farm_dictionary = load_windfarm_yaml("windfarm_information_2x5.yaml")
    setup = build_farm_setup(farm_dictionary)

    site = UniformSite(ws=ws, ti=ti) # wd is given later in the simulation
    
    windTurbines = WindTurbine(
        name="CustomTurbine",
        diameter=setup["diameter"],
        hub_height=setup["hub_height"],
        powerCtFunction=StaticCpCtYawPower()
    )
    windTurbines = V80()
    site = Hornsrev1Site()
    layout_x = setup["layout_x"]
    layout_y = setup["layout_y"]


    uniform_site = XRSite(
    ds=xr.Dataset(data_vars={'WS': 10, 'P': ('wd', f), 'TI': ti},
                  coords={'wd': wd}),
    shear=PowerShear(h_ref=100, alpha=.2))

    #here we import the turbine, site and wake deficit model to use.


    noj = NOJ(site,windTurbines)

    simulationResult = noj(layout_x, layout_y)

    simulationResult.aep()

    print ("Total AEP: %f GWh"%simulationResult.aep().sum())

    wind_speed = 10
    wind_direction = 270


    flow_map = simulationResult.flow_map(ws=wind_speed, wd=wind_direction)
    plt.figure(figsize=(18,10))
    flow_map.plot_wake_map()
    plt.xlabel('x [m]')
    plt.ylabel('y [m]')
    plt.title('Wake map for' + f' {wind_speed} m/s and {wind_direction} deg')

    plt.show()