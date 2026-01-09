# the aim of this file is to test the implementation of the api TO connect the Off simulation with
# a flow of turbine states coming from an external source

import os

import off.off as off
import off.off_interface as offi
import numpy as np
import logging
lg = logging.getLogger('off')

import socket
import struct


def main():

    Nt = 10 # number of turbines, change to read from config file later

    # setting up server with one port to one port communication 
    IP_address = "127.0.0.1" # localhost
    python2simulink_port = 49160
    simulink2python_port = 49152

    py2sim_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sim2py_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    sim2py_socket.bind((IP_address, simulink2python_port))
    sim2py_socket.settimeout(1)
    py2sim_socket.settimeout(1)
    lg.info("Sockets created and bound to ports : %d (Simulink->Python) and %d (Python->Simulink)", simulink2python_port, python2simulink_port)
    
    # get layout of wind farm from windfarm_information.yaml
    file_name = f'{off.OFF_PATH}\\02_Examples_and_Cases\\03_Cases\\windfarm_information_2x5.yaml'

    off_interface = offi.OFFInterface()
    off_interface.init_simulation_by_path(file_name)
    iteration = 0

    # intializing signals so that simulink and off can run simultaneously
    simulink_input_init_perturbine = np.array([10, 0, 0]) # np.array([20, 0.06, -60/180*np.pi]) # wind speed, wind direction (rad), TI
    simulink_input = np.array([simulink_input_init_perturbine for _ in off_interface.off_sim.wind_farm.turbines])
    lg.info("initial simulink_input: %s", simulink_input)

    off_input_init_per_turbine = np.array([0, 0, 0]) # initial yaw, cp, ct
    off_input = np.array([off_input_init_per_turbine for _ in off_interface.off_sim.wind_farm.turbines])
    lg.info("initial off_input: %s", off_input)


    ## updating turbine states so that both simulink and off can run at the same time
    # since all the initial states are the same this can be done this way but only for the initial step
    for turbine in off_interface.off_sim.wind_farm.turbines:
        turbine.turbine_states.update_states(ct=off_input_init_per_turbine[2], cp=off_input_init_per_turbine[1], yaw=off_input_init_per_turbine[0])

    for t in np.arange(off_interface.off_sim.settings_sim['time start'],
                           off_interface.off_sim.settings_sim['time end'],
                           off_interface.off_sim.settings_sim['time step']):
        
        # send info to simulink -> start simulation step in simulink
        counter = 0
        while True:
            try:
                simulink_send_data = struct.pack('!' + 'd'*3*Nt, *simulink_input.flatten()) # sending array of string 
                py2sim_socket.sendto(simulink_send_data, (IP_address, python2simulink_port))
                break
            except socket.timeout:
                # print("No response when sending.")
                pass
            counter += 1
            if counter >= 100:
                print("Failed to send data to Simulink.")
                exit()

        # run off simulation step
        simulink_input = off_interface.off_sim.run_one_step(t)
        simulink_input[:, 1] = simulink_input[:, 1] * np.pi / 180  # convert to radians

        print("sent to simulink:", simulink_input)

        # receive info from simulink -> end of simulation step in simulink
        counter = 0
        while True:
            try:
                off_input_data, _ = sim2py_socket.recvfrom(1024)  # buffer size = 1024 bytes
                break
            except socket.timeout:
                pass
            counter += 1
            if counter >= 100:
                print("Failed to receive data from Simulink.")
                exit()
        
        off_input = np.array(struct.unpack('!' + 'd'*3*Nt, off_input_data))  # recieves flat array
        # convert to a matrix with shape (num_turbines, 3)
        off_input = off_input.reshape((-1, 3))
        print("Received from Simulink:", off_input)
        off_input[:, 0] = off_input[:, 0] * 180 / np.pi  # convert to degrees
        for i in range(Nt):
            lg.info(f"Turbine {i+1} - received from Simulink yaw: {off_input[i,0]}, cp: {off_input[i,1]}, ct: {off_input[i,2]}")
        
        # update turbine states
        for turbine_index, turbine in enumerate(off_interface.off_sim.wind_farm.turbines):
            turbine.turbine_states.update_states(ct=off_input[turbine_index, 2], cp=off_input[turbine_index, 1], yaw=off_input[turbine_index, 0])
        iteration += 1

    py2sim_socket.close()
    # print("Simulation finished, Python process terminated.")

if __name__ == "__main__":
    os.system('cls')
    main()