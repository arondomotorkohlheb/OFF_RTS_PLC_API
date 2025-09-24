# the aim of this file is to test the implementation of the api TO connect the Off simulation with
# a flow of turbine states coming from an external source

import os, logging
logging.basicConfig(level=logging.ERROR)

import off.off as off
from off.turbine import TurbineMask
import numpy as np
import yaml


def main():
    # first create a turbine object that is a mask-> meaning only positional information
    base_location = np.array([0, 0, 1])  # x, y, z in m
    orientation = np.array([0, 0])  # yaw, tilt in degrees

    turbine_list = [TurbineMask(base_location, orientation, None) for i in range(9)]

    # now I have a list of turbine masks matching the number of turbines of the test case



    # get layout of wind farm from windfarm_information.yaml
    with open(f'{off.OFF_PATH}\\02_Examples_and_Cases\\03_Cases\\windfarm_information.yaml', 'r') as file:
        turbine_yaml = yaml.safe_load(file)

    # Update turbine_list with loaded positions
    for i, turbine in enumerate(turbine_list):
        turbine.base_location = np.array([turbine_yaml['wind_farm']['farm']['layout_x'][i],
                                           turbine_yaml['wind_farm']['farm']['layout_y'][i],
                                           turbine_yaml['wind_farm']['farm']['layout_z'][i]])
        turbine.orientation = np.array([0, 0])  # Keep orientation fixed for now
    
    # Re-create wind farm with loaded turbine layout
    wind_farm = off.wfm.WindFarm(turbine_list)
    print(wind_farm.get_layout())
    pass


if __name__ == "__main__":
    main()