# the aim of this file is to test the implementation of the api TO connect the Off simulation with
# a flow of turbine states coming from an external source

import os

import off.off as off
import off.off_interface as offi
import numpy as np
import logging as lg

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
    sim2py_socket.settimeout(5)
    py2sim_socket.settimeout(5)
    print("Sockets created and bound to ports.")
    print("server running")


    # get layout of wind farm from windfarm_information.yaml
    file_name = f'{off.OFF_PATH}\\02_Examples_and_Cases\\03_Cases\\windfarm_information_1x1.yaml'

    off_interface = offi.OFFInterface()
    off_interface.init_simulation_by_path(file_name)
    iteration = 0

    # intializing signals so that simulink and off can run simultaneously
    simulink_input = np.array([20, 120/180*np.pi, 0.06]) # wind speed, wind direction (rad), TI
    off_input = np.array([0, 0, 0]) # initial yaw, cp, ct
    off_interface.off_sim.wind_farm.turbines[0].turbine_states.update_states(ct=off_input[2], cp=off_input[1], yaw=off_input[0])

    for t in np.arange(off_interface.off_sim.settings_sim['time start'],
                           off_interface.off_sim.settings_sim['time end'],
                           off_interface.off_sim.settings_sim['time step']):
        
        # send info to simulink -> start simulation step in simulink
        counter = 0
        while True:
            try:
                simulink_send_data = struct.pack('!ddd', simulink_input[0], simulink_input[2], simulink_input[1])
                py2sim_socket.sendto(simulink_send_data, (IP_address, python2simulink_port))
                # print("Sent to Simulink:", (simulink_input[0], simulink_input[2], simulink_input[1]))
                break
            except socket.timeout:
                # print("No response when sending.")
                pass
            counter += 1
            if counter >= 10:
                break

        # run off simulation step
        simulink_input = off_interface.off_sim.run_one_step(t)
        simulink_input[:, 1] = simulink_input[:, 1] * np.pi / 180  # convert to radians
        simulink_input = simulink_input.flatten()

        # receive info from simulink -> end of simulation step in simulink
        counter = 0
        while True:
            try:
                off_input_data, addr = sim2py_socket.recvfrom(1024)  # buffer size = 1024 bytes
                # print("Received from Simulink:", off_input)
                break
            except socket.timeout:
                # print("No response when receiving.")
                pass
            counter += 1
            if counter >= 10:
                break
        
        off_input = np.array(struct.unpack('!ddd', off_input_data))  # convert to array
        off_input[0] = off_input[0] * 180 / np.pi  # convert to degrees

        lg.info(f"Iteration {iteration}: received from Simulink yaw: {off_input[0]}, cp: {off_input[1]}, ct: {off_input[2]}")
        
        # update turbine states
        off_interface.off_sim.wind_farm.turbines[0].turbine_states.update_states(ct=off_input[2], cp=off_input[1], yaw=off_input[0])
        iteration += 1

    py2sim_socket.close()
    # print("Simulation finished, Python process terminated.")

if __name__ == "__main__":
    os.system('cls')
    main()