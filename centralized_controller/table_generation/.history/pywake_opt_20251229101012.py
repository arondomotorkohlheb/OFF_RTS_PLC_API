from py_wake.site import UniformSite
from py_wake.wind_turbines import WindTurbine
from py_wake import NOJ
import matplotlib.pyplot as plt
import numpy as np
import os
from off2pywake_support import build_farm_setup, load_windfarm_yaml


if __name__ == "__main__": 
    os.system('cls' if os.name == 'nt' else 'clear')

    

    farm_dictionary = load_windfarm_yaml("windfarm_information_2x5.yaml")
    setup = build_farm_setup(farm_dictionary)

    site = UniformSite(wind_speed=8, wind_direction=270, turbulence_intensity=0.1)
    
    #here we import the turbine, site and wake deficit model to use.
    windTurbines = V80()
    site = Hornsrev1Site()
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