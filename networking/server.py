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
time.sleep(5)
for j in range(10):
    print(" \n ")
for i in range(5):
    time.sleep(1)
    print(f"Server will now begin in {5 - (i + 1)} seconds.")
    for j in range(10):
        print(" \n ")
print("Server started!")
print("[!] Warning this is a VERY early version of the server.")
print("[!] Stuff will go wrong!")
players = []

while True:
    client_sock, client_addr = server_sock.accept()  # accept the connection
    data = client_sock.recv(1024) # only up to 1026 bytes accepted
    if data:
        packet_extract = data.decode().split(':')
        print("======= RAW PACKET ========\n", packet_extract, "\n===========================")
        if(packet_extract[0] == "STATUS" and packet_extract[3] == "1"):
            print(f"UUID of player {packet_extract[2]} is {packet_extract[1]}")
            print(f"{packet_extract[2]} joined the game")
            print(f"{packet_extract[2]} [/{client_addr[0]}:{client_addr[1]}] logged in")
            temp_array = [packet_extract[2], packet_extract[1]] # username and UUID
            players.append(temp_array) # add the player to the list.
        if(packet_extract[0] == "STATUS" and packet_extract[3] == "0"):
            print(f"{packet_extract[2]} lost connection: player quit the game.")
            print(f"{packet_extract[2]} left the game")
            temp_array = [packet_extract[2], packet_extract[1]]
            players.remove(temp_array) # remove the player from the list
    client_sock.close() # close


# TO DO HERE:
# add keep alive packet, so we will know when python crashes, and we can remove the player accordingly.
# JUST MAKE SOLID CLIENT TO SERVER COMMUNICATION THROUGH THESE "PACKETS".