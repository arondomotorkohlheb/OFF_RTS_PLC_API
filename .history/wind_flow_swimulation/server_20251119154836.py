import socket
import struct
import time
import matlab.engine

# Create UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Simulink will listen on this port
IP_address = "127.0.0.1" # localhost
python2simulink_port = 5050
simulink2python_port = 9090

py2sim_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sim2py_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

py2sim_socket.bind((IP_address, python2simulink_port))
sim2py_socket.bind((IP_address, simulink2python_port))


# eng = matlab.engine.start_matlab()
# eng.cd('C:\\backup\\Study\\MSc\\research_assignment\\git\\OFF_RTS_PLC_API\\RTS')
# eng.load_system('turbine')


while True:
    data, addr = sim2py_socket.recvfrom(1024)
    x, y, z = struct.unpack('!d', data)
    print("Received from Simulink:", x, y, z)
    time.sleep(1)
    send_data = struct.pack('ddd', x+1, y+1, z+1)
    py2sim_socket.sendto(send_data, (IP_address, python2simulink_port))


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