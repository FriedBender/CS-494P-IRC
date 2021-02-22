"""
CS 494P Project
IRC - Server Application
"""

import socket

#Number of clients the server can handle:#
number_of_clients = 10  #udjustable global


def IRC_server():
    #get the host inforation:
    host = socket.gethostname()
    port = 5050 #non standard port

    IRC_socket = socket.socket()    #the socket instance
    IRC_socket.bind((host, port))   #bind the host address and port to the socket on line above


    #tell the server how many clients MAX to listen to:
    IRC_socket.listen(number_of_clients)

    connection, address = IRC_socket.accept()   #accept a new connecction
    print("New Connection Established: " + str(address))

    #now a loop to keep doing this forever
    #TODO: Fix this to exit normally
    while True:
        data = connection.recv(2048).decode()   #take data of 2048 bytes or less.
        if not data:
            print("invalid data recieved")
        print("From user address: " + str(data))
        data = input(' -> ')
        connection.send(data.encode())  #send stuff back to the client

    connection.close()  #gracefully exit


if __name__ == '__main__':
    IRC_server()
