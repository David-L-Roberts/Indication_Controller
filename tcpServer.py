# Echo Server
import socket
import sys

HOST_NAME = "localhost"
PORT = 10_000
server_address = (HOST_NAME, PORT)
TIMEOUT_SEC = 10

def service_connection(connection, client_address):
    with connection:
        print('client connected:', client_address)
        while True:
            # recieve data from client
            data: bytes = connection.recv(16)
            print('received: %s' % data.hex(sep=" ").upper())

            # send data back to client
            if not data:
                break
            print(f"Sending: {data}")
            connection.sendall(data)

# Create a TCP/IP socket
with socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM) as sock:
    # Bind the socket to the address
    print('starting up on %s port %s' %server_address)
    sock.bind(server_address)
    # enable port to listen for and accept connections
    sock.listen(1)
    sock.settimeout(TIMEOUT_SEC)

    while True:
        # block execution, wait for a connection, and accept it
        try:
            print('waiting for a connection')
            connection, client_address = sock.accept()
            service_connection(connection, client_address)
        except TimeoutError:
            try:
                print(f"No connnection within {TIMEOUT_SEC} seconds. Listening again.")
            except KeyboardInterrupt:
                print("Closing socket and exiting [ctl+c].")
                break
    
