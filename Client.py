"""
CS 494P Project
IRC - Client Application
"""

import socket
import ChatRooms


def IRC_client():
    host = socket.gethostname()
    port = ChatRooms.PORT_NUMBER

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))

    message_to_send = input(" # ")  # allows for input

    # need to stript message to get rid of any formatting etc
    while message_to_send.lower().strip() != 'exit':
        # encode and send message to server
        client_socket.send(message_to_send.encode())
        # receive the response and decode it
        data = client_socket.recv(ChatRooms.MESSAGE_BUFFER).decode()

        print("Message from server: " + data)

        message_to_send = input(" # ")
    client_socket.close()   # close connection


if __name__ == "__main__":
    IRC_client()
