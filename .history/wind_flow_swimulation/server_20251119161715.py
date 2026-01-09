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
eng.load_system('turbine')
eng.set_param('turbine', 'SimulationCommand', 'start')

sim2py_socket.settimeout(10)

while True:
    try:
        data, addr = sim2py_socket.recvfrom(1024)
        power = struct.unpack('!d', data)
        print(power)
    except socket.timeout:
        print("No data received from Simulink within timeout period.")
        break
    # send_data = struct.pack('ddd', x+1, y+1, z+1)
    # py2sim_socket.sendto(send_data, (IP_address, python2simulink_port))

while running:
    # 1. Receive data from Simulink
    try:
        data, addr = sim2py_socket.recvfrom(1024)
        sim_values = struct.unpack('!d', data)  # adjust number of signals
        print("Received from Simulink:", sim_values)
    except socket.timeout:
        pass

    # 2. Send data to Simulink
    x, y, z = 10.0, 20.0, 30.0  # example data
    send_sock.sendto(struct.pack('ddd', x, y, z), (UDP_IP, PYTHON_SEND_PORT))

    # 3. Check if simulation is finished
    sim_status = eng.get_param('turbine', 'SimulationStatus')
    if sim_status == 'stopped':
        running = False

    time.sleep(0.01)  # avoid busy-wait

# --- Cleanup ---
recv_sock.close()
send_sock.close()
eng.quit()
print("Simulation finished, Python process terminated.")




import socket
import struct
import matlab.engine
import time

# --- UDP configuration ---
UDP_IP = "127.0.0.1"
PYTHON_RECV_PORT = 5000   # Receives from Simulink
PYTHON_SEND_PORT = 5001   # Sends to Simulink

# Create receive socket (Simulink → Python)
recv_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
recv_sock.bind((UDP_IP, PYTHON_RECV_PORT))
recv_sock.settimeout(0.01)  # small timeout

# Create send socket (Python → Simulink)
send_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# --- Start MATLAB and Simulink ---
eng = matlab.engine.start_matlab()
eng.load_system('turbine')  # replace with your model name
eng.set_param('turbine', 'SimulationCommand', 'start')

# --- Main loop ---
running = True
while running:
    # 1. Receive data from Simulink
    try:
        data, addr = recv_sock.recvfrom(1024)
        sim_values = struct.unpack('ddd', data)  # adjust number of signals
        print("Received from Simulink:", sim_values)
    except socket.timeout:
        pass

    # 2. Send data to Simulink
    x, y, z = 10.0, 20.0, 30.0  # example data
    send_sock.sendto(struct.pack('ddd', x, y, z), (UDP_IP, PYTHON_SEND_PORT))

    # 3. Check if simulation is finished
    sim_status = eng.get_param('turbine', 'SimulationStatus')
    if sim_status == 'stopped':
        running = False

    time.sleep(0.01)  # avoid busy-wait

# --- Cleanup ---
recv_sock.close()
send_sock.close()
eng.quit()
print("Simulation finished, Python process terminated.")



exit()

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

print("Listening for UDP packets...")

while True:
    data, addr = sock.recvfrom(1024)
    x, y, z = struct.unpack('ddd', data)
    print("Received:", x, y, z)




while True:
    data = struct.pack('!ddd', 15,15,1)
    sock.sendto(data, (SIMULINK_IP, SIMULINK_PORT))
    
    # Run the model
    out = eng.sim('my_model', nargout=1)