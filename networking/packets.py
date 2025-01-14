import socket

server_ip = '127.0.0.1'
server_port = 48185

client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client_sock.connect((server_ip, server_port)) # connection

message = "hi" # message
client_sock.send(message.encode())

client_sock.close()
