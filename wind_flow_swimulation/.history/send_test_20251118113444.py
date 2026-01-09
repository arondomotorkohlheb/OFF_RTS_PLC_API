import socket
import struct

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# pack 3 doubles
data = struct.pack('ddd', 1,1,0)

sock.sendto(data, ("127.0.0.1", 5005))


sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(("127.0.0.1", 5005))   # IP and port to listen on

print("UDP server running on 127.0.0.1:5005")

while True:
    data, addr = sock.recvfrom(1024)  # receive up to 1024 bytes
    print("Received:", data, "from", addr)
