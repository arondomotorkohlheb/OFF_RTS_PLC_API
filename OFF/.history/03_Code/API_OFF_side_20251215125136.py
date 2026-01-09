# the aim of this file is to test the implementation of the api TO connect the Off simulation with
# a flow of turbine states coming from an external source

import os

import off.off as off
import off.off_interface as offi
import numpy as np

def main():

    # get layout of wind farm from windfarm_information.yaml
    file_name = f'{off.OFF_PATH}\\02_Examples_and_Cases\\03_Cases\\windfarm_information_1x1.yaml'

    off_interface = offi.OFFInterface()
    off_interface.init_simulation_by_path(file_name)
    iteration = 0
    for t in np.arange(off_interface.off_sim.settings_sim['time start'],
                           off_interface.off_sim.settings_sim['time end'],
                           off_interface.off_sim.settings_sim['time step']):
        
        print(off_interface.off_sim.wind_farm.turbines[0].turbine_states.create_interpolated_state(0, 1, 0, 1).get_all_states())
        simulink_input = off_interface.off_sim.run_one_step(t)
        print(f"Time: {t}, Simulink input: {simulink_input}")
        
        # update turbine states 
        print(off_interface.off_sim.wind_farm.turbines[0].turbine_states.create_interpolated_state(0, 1, 0, 1).get_all_states())
        off_interface.off_sim.wind_farm.turbines[0].turbine_states.update_states(ct=0.8, cp=0.4, yaw=10.0)
        print(off_interface.off_sim.wind_farm.turbines[0].turbine_states.create_interpolated_state(1, 0, 1, 0).get_all_states())
        print(len(off_interface.off_sim.wind_farm.turbines[0].turbine_states.states))
        iteration += 1
        exit()
        # find a way to update the turbine states here

    pass

if __name__ == "__main__":
    os.system('cls')
    main()