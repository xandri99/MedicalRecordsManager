# DB Sync Server
# Receive records.db from one client at a time. Show error in client if another tries to connect.
# From the client database, get items with isSynced == FALSE, and replace in local (master) DB
# Set isSynced = TRUE for all items in server DB and send to client.

import socket
import tqdm
import os
from DBManager import DBManager
import pyAesCrypt

# device's IP address
SERVER_HOST = "0.0.0.0"
SERVER_PORT = 5001
# receive 4096 bytes each time
BUFFER_SIZE = 4096
SEPARATOR = "<SEPARATOR>"

# create the server socket
# TCP socket
s = socket.socket()
# bind the socket to our local address
s.bind((SERVER_HOST, SERVER_PORT))
# enabling our server to accept connections
# 5 here is the number of unaccepted connections that
# the system will allow before refusing new connections
s.listen(1)
print(f"[*] Listening as {SERVER_HOST}:{SERVER_PORT}")

while 1:
    # accept connection if there is any
    client_socket, address = s.accept()
    # if below code is executed, that means the sender is connected
    print(f"[+] {address} is connected.")

    # receive message
    mode = client_socket.recv(1024).decode()
    print("CLIENT SAYS " + mode)
    client_socket.sendall("OK".encode())

    if mode == "PUSH":
        # receive the file infos
        # receive using client socket, not server socket
        received = client_socket.recv(BUFFER_SIZE).decode()
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
                bytes_read = client_socket.recv(BUFFER_SIZE)
                if not bytes_read:
                    # nothing is received
                    # file transmitting is done
                    break
                # write to the file the bytes we just received
                f.write(bytes_read)
                # update the progress bar
                progress.update(len(bytes_read))

        bufferSize = 64 * 1024
        password = "vaQHNUUvxNrOXVoraeYyjwpHEwpSgUgqTxADSq5jCLG6jhwwsJ9CXZwbBOBDGi8hub2a8z7gRgaEpnxyGszMJZfQqK8SHhVF6Q48hnn2jjeAgLsQo5hMErbj1rEXL4cO"
        pyAesCrypt.decryptFile("records.db.aes", "records.db", password, bufferSize)
        os.remove("records.db.aes")

        # make changes to DB
        remote = DBManager("records.db")
        local = DBManager("local.db")

        # get unsynced changes
        new_records = remote.get_new_records()
        # add them to local db
        for r in new_records:
            local.update_patients_by_record(r)
        # set them as synced
        local.sync_new_records()
        local.close()
        remote.close()

    # send new DB
    elif mode == "PULL":
        bufferSize = 64 * 1024
        password = "vaQHNUUvxNrOXVoraeYyjwpHEwpSgUgqTxADSq5jCLG6jhwwsJ9CXZwbBOBDGi8hub2a8z7gRgaEpnxyGszMJZfQqK8SHhVF6Q48hnn2jjeAgLsQo5hMErbj1rEXL4cO"
        # encrypt
        pyAesCrypt.encryptFile("local.db", "local.db.aes", password, bufferSize)
        filename = "local.db.aes"
        filesize = os.path.getsize(filename)
        # send the filename and filesize
        client_socket.send(f"{filename}{SEPARATOR}{filesize}".encode())
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
                client_socket.sendall(bytes_read)
                # update the progress bar
                progress.update(len(bytes_read))
        client_socket.close()
        os.remove("local.db.aes")
# close the socket
s.close()
