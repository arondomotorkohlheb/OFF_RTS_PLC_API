import socket
import struct
import time

# Create UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Simulink will listen on this port
SIMULINK_IP = "127.0.0.1"
SIMULINK_PORT = 5005

while True:
    x = 3.14
    y = 1.23
    data = struct.pack('ddd', 1,1,0)
    sock.sendto(data, (SIMULINK_IP, SIMULINK_PORT))
    time.sleep(0.01)  # 100 Hz