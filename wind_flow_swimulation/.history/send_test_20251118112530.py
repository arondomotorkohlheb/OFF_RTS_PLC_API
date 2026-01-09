import socket
import struct

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

x = 3.14
y = 1.23

# pack 2 doubles
data = struct.pack('dd', x, y)

sock.sendto(data, ("127.0.0.1", 5005))
