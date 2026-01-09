import socket
import struct
import time
import matlab.engine

# Create UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Simulink will listen on this port
IP_address = "127.0.0.1" # localhost
python2simulink_port = 49160
simulink2python_port = 49152

py2sim_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sim2py_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

py2sim_socket.bind((IP_address, python2simulink_port))
sim2py_socket.bind((IP_address, simulink2python_port))


eng = matlab.engine.start_matlab()
eng.cd('C:\\backup\\Study\\MSc\\research_assignment\\git\\OFF_RTS_PLC_API\\RTS')
print("1. ")
eng.load_system('turbine')
print("2. ")
eng.set_param('turbine', 'SimulationCommand', 'start', nargout=0)
print("3. ")
sim2py_socket.settimeout(2)
running = True
while running:
    # out = eng.sim('turbine', nargout=0)
    # 1. Receive data from Simulink
    data, addr = sim2py_socket.recvfrom(1024)
    power = struct.unpack('!d', data)  # adjust number of signals
    print("Powr Received:", power)

    # 2. Send data to Simulink
    # data = struct.pack('!ddd', 15,15,1)
    # py2sim_socket.sendto(data, (IP_address , 49160))
    
    # Run the model
    

    # 3. Check if simulation is finished
    sim_status = eng.get_param('turbine', 'SimulationStatus')
    if sim_status == 'stopped':
        running = False

    time.sleep(0.01)  # avoid busy-wait

# --- Cleanup ---
py2sim_socket.close()
sim2py_socket.close()
eng.quit()
print("Simulation finished, Python process terminated.")

exit()

import socket
import struct
import matlab.engine
import time

# ----------------------------
# UDP configuration
# ----------------------------
UDP_IP = "127.0.0.1"      # Simulink is on same machine
SIM2PY_PORT = 5000        # Port Simulink sends data to

# ----------------------------
# Create Python UDP receive socket
# ----------------------------
recv_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
recv_sock.bind((UDP_IP, SIM2PY_PORT))
recv_sock.settimeout(0.01)  # allows checking simulation status

print(f"Listening for UDP packets on port {SIM2PY_PORT}...")

# ----------------------------
# Start MATLAB and load Simulink model
# ----------------------------

eng = matlab.engine.start_matlab()
eng.cd('C:\\backup\\Study\\MSc\\research_assignment\\git\\OFF_RTS_PLC_API\\RTS')
print("1. ")
eng.load_system('turbine')
print("2. ")
eng.set_param('turbine', 'SimulationCommand', 'start', nargout=0)
print("3. ")

# ----------------------------
# Main loop: receive data
# ----------------------------
running = True
while running:
    # Receive data from Simulink
    try:
        data, addr = recv_sock.recvfrom(1024)  # buffer size = 1024 bytes
        power = struct.unpack('!d', data)  # adjust number of signals
        print("Received from Simulink:", sim_values)
    except socket.timeout:
        # No data this iteration
        pass

    # Check if simulation has finished
    sim_status = eng.get_param('turbine', 'SimulationStatus')
    if sim_status == 'stopped':
        running = False

    time.sleep(0.01)  # small delay to avoid busy-wait

# ----------------------------
# Cleanup
# ----------------------------
recv_sock.close()
eng.quit()
print("Simulation finished, Python process terminated.")