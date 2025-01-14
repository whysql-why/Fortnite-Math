import socket, time

server_ip = '0.0.0.0'
server_port = 25565

server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # new socket.
server_sock.bind((server_ip, server_port))
server_sock.listen(5) # max 5 clients.

print("Fortnite Math Server loaded.")
print(f"Config show that you are running server on\n Port: {server_port}")
print(f"You need to configure your firewall to allow connections from port {server_port}!")
print("Or else, only local connections are accepted.")

# print("Server will now begin in 5 seconds.")
for j in range(10):
    print(" \n ")
for i in range(5):
    time.sleep(1)
    print(f"Server will now begin in {5 - (i + 1)} seconds.")
    for j in range(10):
        print(" \n ")
print("Server started!")

players = []

while True:
    client_sock, client_addr = server_sock.accept()  # accept the connection
    data = client_sock.recv(1024) # only up to 1026 bytes accepted
    if data:
        packet_extract = data.decode().split(':')
        # print(packet_extract)
        if(packet_extract[0] == "STATUS" and packet_extract[3] == "1"):
            print(f"{packet_extract[2]} joined the game!")
            client_sock.send("asdasd".encode())
            temp_array = [packet_extract[2], packet_extract[1]] # username and UUID
            players.append(temp_array) # add the player to the list.
        if(packet_extract[0] == "STATUS" and packet_extract[3] == "0"):
            print(f"{packet_extract[2]} left the game!")
            temp_array = [packet_extract[2], packet_extract[1]]
            players.remove(temp_array) # remove the player from the list
    client_sock.close() # close
