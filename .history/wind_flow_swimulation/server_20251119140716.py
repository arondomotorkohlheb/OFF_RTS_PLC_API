import socket
import struct
import time
import matlab.engine

# Create UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Simulink will listen on this port
SIMULINK_IP = "127.0.0.1"
SIMULINK_PORT = 5005

import matlab.engine

# Start MATLAB
eng = matlab.engine.start_matlab()

# Load your model (without .slx extension)
eng.load_system('my_model')


while True:
    data = struct.pack('!ddd', 15,15,1)
    sock.sendto(data, (SIMULINK_IP, SIMULINK_PORT))