import socket


def connect(ip, port, uuid, username):
    client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    message = f"ping from {uuid} as {username}!"
    try:
        client_sock.connect((ip, port)) # connection
        client_sock.send(message.encode())
        return True
    except socket.error as e:
        print(e)
        return False

def send_packet(ip, port, message):
    client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_sock.connect((ip, port))
        client_sock.send(message.encode())
        client_sock.close()
        return True
    except socket.error as e:
        print(e)
        return False