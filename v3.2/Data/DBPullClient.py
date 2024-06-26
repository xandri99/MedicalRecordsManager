import pyAesCrypt
import tqdm
import os
from shutil import copyfile
import socket

# receive new DB
SEPARATOR = "<SEPARATOR>"
BUFFER_SIZE = 4096 # send 4096 bytes each time step
f1 = open("server.txt", "r")
host = f1.readline().rstrip()
f1.close()

f2 = open("port.txt", "r")
port = int(f2.readline())
f2.close()

# create the client socket
s = socket.socket()
print(f"[+] Connecting to {host}:{port}")
s.connect((host, port))
print("[+] Connected.")

# request pull
s.sendall("PULL".encode())
print("SERVER SAYS " + s.recv(2).decode())

# receive the file infos
# receive using client socket, not server socket
received = s.recv(BUFFER_SIZE).decode()
filename, filesize = received.split(SEPARATOR)
# remove absolute path if there is
filename = os.path.basename(filename)
# convert to integer
filesize = int(filesize)

# start receiving the file from the socket
# and writing to the file stream
progress = tqdm.tqdm(range(filesize), f"Receiving {filename}", unit="B", unit_scale=True, unit_divisor=1024)
with open(filename, "wb") as f:
    while True:
        # read 1024 bytes from the socket (receive)
        bytes_read = s.recv(BUFFER_SIZE)
        if not bytes_read:
            # nothing is received
            # file transmitting is done
            break
        # write to the file the bytes we just received
        f.write(bytes_read)
        # update the progress bar
        progress.update(len(bytes_read))
s.close()

bufferSize = 64 * 1024
password = "vaQHNUUvxNrOXVoraeYyjwpHEwpSgUgqTxADSq5jCLG6jhwwsJ9CXZwbBOBDGi8hub2a8z7gRgaEpnxyGszMJZfQqK8SHhVF6Q48hnn2jjeAgLsQo5hMErbj1rEXL4cO"
pyAesCrypt.decryptFile("local.db.aes", "local.db", password, bufferSize)

# replace DB
os.remove("records.db")
os.remove("local.db.aes")
copyfile("local.db", "records.db")
os.remove("local.db")
