from py_wake.site import UniformSite
from py_wake.wind_turbines import WindTurbine
from py_wake import NOJ
import matplotlib.pyplot as plt
import numpy as np
import os
from off2pywake_support import build_farm_setup, load_windfarm_yaml


if __name__ == "__main__": 
    os.system('cls' if os.name == 'nt' else 'clear')

    ws = 8  # wind speed
    wd = 270  # wind direction
    ti = 0.1  # turbulence intensity

    farm_dictionary = load_windfarm_yaml("windfarm_information_2x5.yaml")
    setup = build_farm_setup(farm_dictionary)

    site = UniformSite(ws=ws, ti=ti)
    exit()
    
    windTurbines = WindTurbine(
        name="CustomTurbine",
        diameter=setup["diameter"],
        hub_height=setup["hub_height"],
        powerCtFunction=StaticCpCtYawPower(
            cp=lambda ws, yaw: np.ones_like(ws),
            ct=lambda ws, yaw: np.ones_like(ws)
        )
    )

    exit()

    #here we import the turbine, site and wake deficit model to use.


    noj = NOJ(site,windTurbines)

    simulationResult = noj(wt16_x,wt16_y)

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