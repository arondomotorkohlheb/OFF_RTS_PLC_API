# the aim of this file is to test the implementation of the api TO connect the Off simulation with
# a flow of turbine states coming from an external source

import os, logging
logging.basicConfig(level=logging.ERROR)

import off.off as off
import off.off_interface as offi
import numpy as np


def main():

    # get layout of wind farm from windfarm_information.yaml
    file_name = f'{off.OFF_PATH}\\02_Examples_and_Cases\\03_Cases\\windfarm_information.yaml'

    off_interface = offi.OFFInterface()
    off_interface.init_simulation_by_path(file_name)

    for t in np.arange(off_interface.off_sim.settings_sim['time start'],
                           off_interface.off_sim.settings_sim['time end'],
                           off_interface.off_sim.settings_sim['time step']):

        wind_velocity = off_interface.off_sim.run_one_step(t)
        print(f"Time: {t}, Wind Velocity at first turbine: {wind_velocity[0]}")

        #update state of turbines

    pass


if __name__ == "__main__":
    main()