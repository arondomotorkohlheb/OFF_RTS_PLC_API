# the aim of this file is to test the implementation of the api TO connect the Off simulation with
# a flow of turbine states coming from an external source

import os, logging
logging.basicConfig(level=logging.ERROR)

import off.off as off
import off.off_interface as offi
from off.turbine import TurbineMask
import numpy as np
import yaml


def main():

    # get layout of wind farm from windfarm_information.yaml
    file_name = f'{off.OFF_PATH}\\02_Examples_and_Cases\\03_Cases\\windfarm_information.yaml'

    off_interface = offi.OFFInterface()
    off_interface.init_simulation_by_path(file_name)

    for t in np.arange(off_interface.off_sim.settings_sim['time start'],
                           off_interface.off_sim.settings_sim['time end'],
                           off_interface.off_sim.settings_sim['time step']):

        wind_vprint(off_interface.off_sim.run_one_step(t))





    # update the states of the turbines
    # apply zoh until turbine states are updated again
    # run simulation for one time step in a while loop

    # base_location = np.array([0, 0, 1])  # x, y, z in m
    # orientation = np.array([0, 0])  # yaw, tilt in degrees

    # turbine_list = [TurbineMask(base_location, orientation, None) for i in range(9)]

    # # Update turbine_list with loaded positions
    # for i, turbine in enumerate(turbine_list):
    #     turbine.base_location = np.array([turbine_yaml['wind_farm']['farm']['layout_x'][i],
    #                                        turbine_yaml['wind_farm']['farm']['layout_y'][i],
    #                                        turbine_yaml['wind_farm']['farm']['layout_z'][i]])
    #     turbine.orientation = np.array([0, 0])  # Keep orientation fixed for now
    
    # # Re-create wind farm with loaded turbine layout
    # wind_farm = off.wfm.WindFarm(turbine_list)
    # os.makedirs("empty_dir", exist_ok=True)

    # settings_sim = turbine_yaml['sim']
    # settings_wke = turbine_yaml['wake']['settings']
    # settings_sol = turbine_yaml['solver']
    # settings_cor = turbine_yaml['ambient']
    # settings_vis = {}
    # off_obj = off.OFF(wind_farm, settings_cor=settings_cor, settings_sim=settings_sim,
    #                   settings_wke=settings_wke, settings_sol=settings_sol, settings_ctr={},
    #                   vis=settings_vis)

    # off_obj.init_sim(
    #         np.array([turbine_yaml["ambient"]["flow_field"]["wind_speeds"][0],
    #                   turbine_yaml["ambient"]["flow_field"]["wind_directions"][0],
    #                   turbine_yaml["ambient"]["flow_field"]["turbulence_intensities"][0]]),
    #         np.array([1 / 3, 0, 0]))
    pass


if __name__ == "__main__":
    main()