import socket

# threading might be required when working with listening for packets.


def connect(ip, port, uuid, username):
    client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    message = f"STATUS:{uuid}:{username}:1"
    # docs:
    # packetType : playerUUID : playerUsername : 1   <<<< [ 1 = joined, 0 = left ]
    # type of packetTypes:
    # STATUS
    # PLAY
    try:
        client_sock.connect((ip, port)) # connection
        client_sock.send(message.encode())
        data = client_sock.recv(1024)
        if data:
            print(data.decode())
        return True
    except socket.error as e:
        print("==================")
        print("Server is offline!")
        print("==================")
        exit(1)
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

def disconnect(ip, port, uuid, username):
    client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    message = f"STATUS:{uuid}:{username}:0"
    client_sock.connect((ip, port))
    client_sock.send(message.encode())
