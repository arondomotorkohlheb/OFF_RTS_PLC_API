import socket
import struct
import time

# ----------------------------
# Create Python UDP receive and send sockets   
# ----------------------------
IP_address = "127.0.0.1" # localhost
python2simulink_port = 49160
simulink2python_port = 49152

py2sim_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sim2py_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# py2sim_socket.bind((IP_address, python2simulink_port))
sim2py_socket.bind((IP_address, simulink2python_port))

sim2py_socket.settimeout(5)
py2sim_socket.settimeout(5)

print("Sockets created and bound to ports.")
print("server running")
counter = 0
while True:

    # sending data
    counter1 = 0
    while True:
        counter1 += 1
        if counter1 > 10:
            break
        try:
            # wind= 15, 1, 1  # example values
            send_data = struct.pack('!ddd', 10, 1, 1)  # adjust number of signals
            py2sim_socket.sendto(send_data, (IP_address, python2simulink_port))
            # print("Sent to Simulink:", (10, 10, 1))
            break
        except socket.timeout:
            # print("No response when sending.")
            pass

    # receiving data
    counter1 = 0
    while True:
        counter1 += 1
        if counter1 > 10:
            break
        try:
            data, addr = sim2py_socket.recvfrom(1024)  # buffer size = 1024 bytes
            power = struct.unpack('!ddd', data)  # adjust number of signals
            # print(type(power))
            # print("Received from Simulink:", power)
            break
        except socket.timeout:
            # print("No response when receiving.")
            pass #break
   
   
    counter += 1
    if counter >= 4:
        break

    

# ----------------------------
# Cleanup
# ----------------------------
# sim2py_socket.close()

py2sim_socket.close()
print("Simulation finished, Python process terminated.")
