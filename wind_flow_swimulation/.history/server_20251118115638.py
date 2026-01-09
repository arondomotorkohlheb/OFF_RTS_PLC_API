import socket
import struct
import time

# Create UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Simulink will listen on this port
SIMULINK_IP = "127.0.0.1"
SIMULINK_PORT = 5005

while True:
    data = struct.pack('ddd', 10,10,0)
    sock.sendto(data, (SIMULINK_IP, SIMULINK_PORT))
    time.sleep(0.001)  # 10 Hz