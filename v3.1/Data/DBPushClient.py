# DB Push Client
# Send records.db to server

import tqdm
import os
import socket                   # Import socket module
import pyAesCrypt

SEPARATOR = "<SEPARATOR>"
BUFFER_SIZE = 4096              # send 4096 bytes each time step
# the ip address or hostname of the server, the receiver
host = "127.0.0.1"
# the port, let's use 5001
port = 5001

bufferSize = 64 * 1024
password = "vaQHNUUvxNrOXVoraeYyjwpHEwpSgUgqTxADSq5jCLG6jhwwsJ9CXZwbBOBDGi8hub2a8z7gRgaEpnxyGszMJZfQqK8SHhVF6Q48hnn2jjeAgLsQo5hMErbj1rEXL4cO"
# encrypt
pyAesCrypt.encryptFile("records.db", "records.db.aes", password, bufferSize)

# the name of file we want to send, make sure it exists
filename = "records.db.aes"
# get the file size
filesize = os.path.getsize(filename)
# create the client socket
s = socket.socket()
print(f"[+] Connecting to {host}:{port}")
s.connect((host, port))
print("[+] Connected.")

# request push
s.sendall("PUSH".encode())
print("SERVER SAYS " + s.recv(1024).decode())

# send the filename and filesize
s.send(f"{filename}{SEPARATOR}{filesize}".encode())
# start sending the file
progress = tqdm.tqdm(range(filesize), f"Sending {filename}", unit="B", unit_scale=True, unit_divisor=1024)
with open(filename, "rb") as f:
    while True:
        # read the bytes from the file
        bytes_read = f.read(BUFFER_SIZE)
        if not bytes_read:
            # file transmitting is done
            break
        # we use sendall to assure transmission in
        # busy networks
        s.sendall(bytes_read)
        # update the progress bar
        progress.update(len(bytes_read))
# close the socket
s.close()
os.remove("records.db.aes")