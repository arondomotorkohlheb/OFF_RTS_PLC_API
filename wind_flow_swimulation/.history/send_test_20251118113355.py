import socket
import struct

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# pack 2 doubles
data = struct.pack('ddd', (1,1,0,0))

sock.sendto(data, ("127.0.0.1", 5005))
