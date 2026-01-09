# the aim of this file is to test the implementation of the api TO connect the Off simulation with
# a flow of turbine states coming from an external source

import os

import off.off as off
import off.off_interface as offi
import numpy as np

import socket
import struct
import time

def main():

    # setting up server with one port to one port communication 
    IP_address = "127.0.0.1" # localhost
    python2simulink_port = 49160
    simulink2python_port = 49152

    py2sim_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sim2py_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    sim2py_socket.bind((IP_address, simulink2python_port))
    sim2py_socket.settimeout(1)
    py2sim_socket.settimeout(1)
    print("Sockets created and bound to ports.")
    print("server running")


    # get layout of wind farm from windfarm_information.yaml
    file_name = f'{off.OFF_PATH}\\02_Examples_and_Cases\\03_Cases\\windfarm_information_1x1.yaml'

    off_interface = offi.OFFInterface()
    off_interface.init_simulation_by_path(file_name)
    iteration = 0

    # intializing signals so that simulink and off can run simultaneously
    simulink_input = off_interface.off_sim.wind_farm.turbines[0].get_simulink_input_signals()
    for t in np.arange(off_interface.off_sim.settings_sim['time start'],
                           off_interface.off_sim.settings_sim['time end'],
                           off_interface.off_sim.settings_sim['time step']):

        simulink_input = off_interface.off_sim.run_one_step(t)
        
        # update turbine states
        off_interface.off_sim.wind_farm.turbines[0].turbine_states.update_states(ct=0.8, cp=0.4, yaw=10.0)
        iteration += 1
        exit()
        # find a way to update the turbine states here

    pass

if __name__ == "__main__":
    os.system('cls')
    main()