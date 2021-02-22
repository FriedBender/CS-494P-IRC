"""
CS 494P Project
IRC - Client Application
"""

import socket

def IRC_client():
    host = socket.gethostname()
    port = 5050 #same as server

    client_socket = socket.socket()
    client_socket.connect((host, port))

    message_to_send = input(" # ")  #allows for input

    #need to stript message to get rid of any formatting etc
    while message_to_send.lower().strip() != 'exit':
        client_socket.send(message_to_send.encode()) #encode and send message to server
        data = client_socket.recv(2048).decode()    #receive the response and decode it

        print("Message from server: " + data)

        message_to_send = input(" # ")
    client_socket.close()   #close connection


if __name__ == "__main__":
    IRC_client()