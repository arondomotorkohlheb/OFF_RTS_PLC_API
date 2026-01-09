import socket

import subprocess
import time
start_time = time.time()

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(("127.0.0.1", 5005))   # IP and port to listen on

print("UDP server running on 127.0.0.1:5005")

while True:
    data, addr = sock.recvfrom(1024)  # receive up to 1024 bytes
    print("Received:", data, "from", addr)
    if time.time() - start_time > 10:  # run for 10 seconds
        subprocess.run(["python", "send_test.py"])
        print("Sent test data")
    elif time.time() - start_time > 10:  # run for 10 seconds
        break
print()
