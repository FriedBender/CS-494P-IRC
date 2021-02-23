"""
CS 494P Project
IRC - Server Application
"""

import socket
import ChatRooms


def IRC_server():
    # get the host information:
    host = socket.gethostname()
    port = ChatRooms.PORT_NUMBER
    # the socket instance, specifying that it is a TCP connection
    IRC_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # bind the host address and port to the socket on line above
    IRC_socket.bind((host, port))

    # tell the server how many clients MAX to listen to:
    IRC_socket.listen(ChatRooms.MAX_NUMBER_OF_CLIENTS)

    connection, address = IRC_socket.accept()   # accept a new connecction
    print("New Connection Established: " + str(address))

    # now a loop to keep doing this forever
    # TODO: Fix this to exit normally
    while True:
        # This handles the sending and recieving of data from the server.
        data = connection.recv(ChatRooms.MESSAGE_BUFFER).decode()
        if not data:
            print("invalid data recieved")
        print("From user address: " + str(data))
        data = input(" # ")
        connection.send(data.encode())  # send stuff back to the client

    connection.close()  # gracefully exit


if __name__ == '__main__':
    IRC_server()
