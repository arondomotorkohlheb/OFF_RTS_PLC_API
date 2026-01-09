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

while True:
    out = eng.sim('turbine', nargout=0)
    print('')
    # 1. Receive data from Simulink
    try:
        data, addr = sim2py_socket.recvfrom(1024)
        power = struct.unpack('!d', data)  # adjust number of signals
        print("Powr Received:", power)
    except sim2py_socket.timeout:
        print("No data received from Simulink within timeout period.")
        exit()

    # 2. Send data to Simulink
    # data = struct.pack('!ddd', 15,15,1)
    # py2sim_socket.sendto(data, (IP_address , 49160))
    
    # Run the model
    

    # 3. Check if simulation is finished
    sim_status = eng.get_param('turbine', 'SimulationStatus')
    if sim_status == 'stopped':
        break

    time.sleep(0.01)  # avoid busy-wait

# --- Cleanup ---
py2sim_socket.close()
sim2py_socket.close()
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