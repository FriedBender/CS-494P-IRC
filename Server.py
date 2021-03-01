"""
CS 494P Project
IRC - Server Application
"""

import socket, select, sys

NUM_CLIENTS = 10    # Number of clients the server can handle
BUFFER_SIZE = 2048  # Global message data buffer
SOCKET_LIST = []   # Maintain a list of socket connections
CLIENTS = {}    # Maintain a dictionary of clients. The key is the socket, the value is the username

# Broadcast a message to all clients
def message_broadcast(sender_socket, message):
    user = CLIENTS[sender_socket]
    print(f"{user} > {message}", end='\r')


    # Send the message to all clients except the one that sent the messaage
    for client_socket in CLIENTS:
        if client_socket != sender_socket:
                client_socket.send(f"{user} > {message}".encode())


def irc_server():
    #get the host information:
    host = socket.gethostname()
    port = 5050 #non standard port

    server_socket = socket.socket()    #the server socket instance
    server_socket.bind((host, port))   #bind the host address and port to the socket on line above
    print(f"Server socket bound to {host}:{port}")

    #tell the server how many clients MAX to listen to:
    server_socket.listen(NUM_CLIENTS)

    SOCKET_LIST.append(server_socket)


    # now a loop to keep doing this forever
    # TODO: Fix this to exit normally
    while True:
        # Populate a list of sockets that have been read
        read_sockets, write_sockets, err_sockets = select.select(SOCKET_LIST, [], [])

        for notified_socket in read_sockets:

            # Accept a new connection, add client socket to socket_list, and add client username to client list
            if notified_socket == server_socket:
                client_socket, client_address = server_socket.accept()
                SOCKET_LIST.append(client_socket)
                print(f"New connection established from {client_address}")

                # Initial message data will be username
                user = client_socket.recv(BUFFER_SIZE).decode()
                CLIENTS[client_socket] = user
                client_socket.send(f"Welcome to the server, {user}\n".encode())

            else:
                message = notified_socket.recv(BUFFER_SIZE).decode()
                
                # If client disconnected, message will be empty
                if not message:
                    notified_socket.close()
                    SOCKET_LIST.remove(notified_socket)
                    CLIENTS.pop(notified_socket)
                else:
                    message_broadcast(notified_socket, message)

    server_socket.close()  #gracefully exit


if __name__ == '__main__':
    irc_server()
