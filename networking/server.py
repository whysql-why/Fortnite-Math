import socket

server_ip = '0.0.0.0'
server_port = 12345

server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # new socket.
server_sock.bind((server_ip, server_port))
server_sock.listen(5) # max 5 clients.
while True:
    client_sock, client_addr = server_sock.accept()  # accept the connection
    data = client_sock.recv(1024) # only up to 1026 bytes accepted
    if data:
        print(f"{data.decode()}") # the message
    client_sock.close() # close
