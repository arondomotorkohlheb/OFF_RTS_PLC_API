from py_wake.examples.data.hornsrev1 import Hornsrev1Site, V80, wt_x, wt_y, wt16_x, wt16_y
from py_wake import NOJ
import matplotlib.pyplot as plt
from pathlib import Path
import yaml
from typing import Any, Dict
import numpy as np
import os
from off2pywake_support



def load_windfarm_yaml(yaml_name) -> Dict[str, Any]:
    # two levels up from this file
    base = Path(__file__).resolve().parent.parent.parent

    # build the Windows-style path in a cross-platform way
    rel = Path("OFF") / "02_Examples_and_Cases" / "03_Cases" / yaml_name
    yaml_path = base / rel

    with yaml_path.open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    return data or {}

if __name__ == "__main__": 
    os.system('cls' if os.name == 'nt' else 'clear')

    farm_dictionary = load_windfarm_yaml("windfarm_information_2x5.yaml")
    setup = build_farm_setup(farm_dictionary)


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