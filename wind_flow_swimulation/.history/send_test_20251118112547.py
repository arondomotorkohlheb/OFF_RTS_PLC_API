import socket
import struct

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

v

# pack 2 doubles
data = struct.pack('wind', x, y)

sock.sendto(data, ("127.0.0.1", 5005))
