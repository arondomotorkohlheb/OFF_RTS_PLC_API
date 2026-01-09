import socket
import struct
import time
import matlab.engine

# Create UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Simulink will listen on this port
IP_address = "127.0.0.1" # localhost
SIMULINK_PORT = 5050


eng = matlab.engine.start_matlab()
eng.cd('C:\\backup\\Study\\MSc\\research_assignment\\git\\OFF_RTS_PLC_API\\RTS')
eng.load_system('turbine')

UDP_PORT = 9090

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

print("Listening for UDP packets...")

while True:
    data, addr = sock.recvfrom(1024)
    x, y, z = struct.unpack('ddd', data)
    print("Received:", x, y, z)

exit()


while True:
    data = struct.pack('!ddd', 15,15,1)
    sock.sendto(data, (SIMULINK_IP, SIMULINK_PORT))
    
    # Run the model
    out = eng.sim('my_model', nargout=1)