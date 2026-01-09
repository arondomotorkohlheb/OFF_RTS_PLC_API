# the aim of this file is to test the implementation of the api TO connect the Off simulation with
# a flow of turbine states coming from an external source

import os, logging

import off.off as off
import off.off_interface as offi
import numpy as np
import pandas as pd
def main():

    # get layout of wind farm from windfarm_information.yaml
    file_name = f'{off.OFF_PATH}\\02_Examples_and_Cases\\03_Cases\\windfarm_information_3x3.yaml'

    off_interface = offi.OFFInterface()
    off_interface.init_simulation_by_path(file_name)
    iteration = 0
    measurements = pd.DataFrame()
    for t in np.arange(off_interface.off_sim.settings_sim['time start'],
                           off_interface.off_sim.settings_sim['time end'],
                           off_interface.off_sim.settings_sim['time step']):

        off_interface.off_sim.wind_farm.turbines[0].turbine_states.set_ct(0.1)
        simulink_input = off_interface.off_sim.run_one_step(t)
        print(f"Time: {t}, Simulink input: {simulink_input}")
        iteration += 1
        exit()
        # find a way to update the turbine states here

    pass

if __name__ == "__main__":
    os.system('cls')
    main()