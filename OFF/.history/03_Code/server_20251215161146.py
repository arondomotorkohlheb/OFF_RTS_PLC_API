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
    time.sleep(0.5)
    try:
        # wind= 15, 1, 1  # example values
        send_data = struct.pack('!ddd', 10, 10, 1)  # adjust number of signals
        py2sim_socket.sendto(send_data, (IP_address, python2simulink_port))
        print("Sent data to Simulink")
    except socket.timeout:
        print("No response when sending.")
        break
    # try:
    #     data, addr = sim2py_socket.recvfrom(1024)  # buffer size = 1024 bytes
    #     power = struct.unpack('!d', data)  # adjust number of signals
    #     print("Received from Simulink:", power)
    # except socket.timeout:
        #print("No response when receiving.")
    #     pass #break
    counter += 1
    if counter >= 100:
        break

    

# ----------------------------
# Cleanup
# ----------------------------
# sim2py_socket.close()
py2sim_socket.close()
print("Simulation finished, Python process terminated.")