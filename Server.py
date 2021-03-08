"""
CS 494P Project
IRC - Server Application
"""

import socket, select, sys
from ChatRooms import IRC_Application, ChatRoom, Member
import ChatRooms

SOCKET_LIST = []   # Maintain a list of socket connections
CLIENTS = {}    # Maintain a dictionary of clients. The key is the socket, the value is the username
irc_Application = IRC_Application()  # The object to handle the IRC side of things.
new_room = ChatRoom(ChatRooms.DEFAULT_ROOM_NAME)    # creates a new room
irc_Application.rooms[ChatRooms.DEFAULT_ROOM_NAME] = new_room  # puts the new default room into the rooms

"""
# Broadcast a message to all clients
def message_broadcast(sender_socket, message):
    user = CLIENTS[sender_socket]
    print(f"{user} > {message}", end='\r')


    # Send the message to all clients except the one that sent the messaage
    for client_socket in CLIENTS:
        if client_socket != sender_socket:
                client_socket.send(f"{user} > {message}".encode())
"""

def irc_server():
    #get the host information:
    host = socket.gethostname()
    port = ChatRooms.PORT_NUMBER #Port defined in chatrooms

    server_socket = socket.socket()    #the server socket instance
    server_socket.bind((host, port))   #bind the host address and port to the socket on line above
    print(f"Server socket bound to {host}:{port}")

    #tell the server how many clients MAX to listen to:
    server_socket.listen(ChatRooms.MAX_NUMBER_OF_CLIENTS)

    SOCKET_LIST.append(server_socket)


    # now a loop to keep doing this forever
    # TODO: Fix this to exit normally
    while True:
        # Populate a list of sockets that have been read
        read_sockets, write_sockets, err_sockets = select.select(SOCKET_LIST, [], [])

        for notified_socket in read_sockets:
            # Will look for a new connection, then it will create a new instance of a member and put the member
            # Into a default room
            if notified_socket == server_socket:
                """
                client_socket, client_address = server_socket.accept()
                SOCKET_LIST.append(client_socket)
                print(f"New connection established from {client_address}")

                # Initial message data will be username
                user = client_socket.recv(ChatRooms.MESSAGE_BUFFER).decode()
                CLIENTS[client_socket] = user
                client_socket.send(f"Welcome to the server, {user}\n".encode())
                """
                new_member_socket, new_client_address = notified_socket.accept()    # gets the connection info
                new_member_username = irc_Application.getUserName(new_member_socket)    # This get the username from the user entry
                new_member = Member(new_member_socket, str(new_member_username), ChatRooms.DEFAULT_ROOM_NAME) #creates an instance of a Member
                irc_Application.rooms[ChatRooms.DEFAULT_ROOM_NAME].Add_New_Member_to_ChatRoom(new_member)   #adds a new user to the chartoom

            else:
                message = notified_socket.recv(ChatRooms.MESSAGE_BUFFER).decode()
                
                # If client disconnected, message will be empty
                if not message:
                    notified_socket.close()
                    SOCKET_LIST.remove(notified_socket)
                    CLIENTS.pop(notified_socket)
                else:
                    irc_Application.Message_Parse(notified_socket, message)

    server_socket.close()  #gracefully exit


if __name__ == '__main__':
    irc_server()
