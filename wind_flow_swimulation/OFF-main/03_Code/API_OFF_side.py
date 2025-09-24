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

    # create windfarm object 
    wind_farm = off.wfm.WindFarm(turbine_list)


    # get layout of wind farm from turbine_mask.yaml
    with open(f'{off.OFF_PATH}\\02_Examples_and_Cases\\00_Inputs\\01_FLORIS\\03_Turbine_model\\turbine_mask.yaml', 'r') as file:
        turbine_yaml = yaml.safe_load(file)
    
    print(turbine_yaml)

    # Re-create wind farm with loaded turbine layout
    wind_farm = off.wfm.WindFarm(turbine_list)
    pass


if __name__ == "__main__":
    main()