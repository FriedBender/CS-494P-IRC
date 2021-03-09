"""
CS 494P Project
IRC - Server Application
"""

import socket, select, Chatrooms
from Chatrooms import IRC_Application, Chatroom

# Globals
PORT_NUMBER = 5050
SOCKET_LIST = []   # Maintain a list of socket connections
CLIENTS = {}    # Maintain a dictionary of clients. The key is the socket, the value is the username
BUFFER_SIZE = 2048  # Define the maxiumum message buffer size
MAX_NUMBER_OF_CLIENTS = 10  # Maxmimum number of clients

irc_instance = IRC_Application()  # The object to handle the IRC side of things.
default_room = Chatroom(Chatrooms.DEFAULT_ROOM_NAME)    # creates a new default room
irc_instance.rooms[default_room.name] = default_room  # puts the new default room into the room dictionary

def irc_server():
    #get the host information:
    host = socket.gethostname()
    port = PORT_NUMBER

    server_socket = socket.socket()    #the server socket instance
    server_socket.bind((host, port))   #bind the host address and port to the socket on line above
    print(f"Server socket bound to {host}:{port}")

    #tell the server how many clients MAX to listen to:
    server_socket.listen(MAX_NUMBER_OF_CLIENTS)

    SOCKET_LIST.append(server_socket)

    while True:
        # Populate a list of sockets that have been read
        read_sockets, write_sockets, err_sockets = select.select(SOCKET_LIST, [], [])

        for notified_socket in read_sockets:
            # Case where the server socket is being read from (i.e. initial client connection):
            # Add the client to the socket list and the client dictionary
            # and add the client to the default room
            if notified_socket == server_socket:
                
                new_client_socket, new_client_address = server_socket.accept()
                SOCKET_LIST.append(new_client_socket)
                print(f"New connection established from {new_client_address}")

                # The initial message data will be the username to add to the client dictionary
                user = new_client_socket.recv(BUFFER_SIZE).decode()
                CLIENTS[new_client_socket] = user
                new_client_socket.send(f"Welcome to the server, {user}\n".encode())
                
                irc_instance.rooms[Chatrooms.DEFAULT_ROOM_NAME].add_new_client_to_chatroom(user, new_client_socket)

            # Case where client socket is being read from:
            # Decode and handle the message
            else:
                message = notified_socket.recv(BUFFER_SIZE).decode()
                
                # If client disconnected, message will be empty
                # and client will be removed from socket list and client dictionary
                if not message:
                    notified_socket.close()
                    SOCKET_LIST.remove(notified_socket)
                    CLIENTS.pop(notified_socket)
                    # TODO Remove client from all rooms
                
                # Send the message to the parser to be handled
                else:
                    IRC_Application.message_parse(irc_instance, notified_socket, CLIENTS[notified_socket], message)


    server_socket.close()  #gracefully exit


if __name__ == '__main__':
    irc_server()
