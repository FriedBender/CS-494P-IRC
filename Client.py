"""
CS 494P Project
IRC - Client Application
"""

import socket, select, sys

BUFFER_SIZE = 2048  # Define the maxiumum message buffer size

# Give the user a prompt for input
def user_input(username):
    sys.stdout.write(f"{username} > ")
    sys.stdout.flush()

def irc_client():
    # Get the host IP and port for the server
    host = socket.gethostname()
    port = 5050

    username = input("Username: ")

    # Create the server socket and connect to the server
    server_socket = socket.socket()
    server_socket.connect((host, port))
    print(f"Connected to server at {host}:{port}")

    # Send initial message to server with username
    server_socket.send(username.encode())

    # Loop to receive and send messages
    while True:
        # Check stdin for messages from the client and check the server socket for messages from the server
        socket_list = [sys.stdin, server_socket]
        read_sockets, write_sockets, error_sockets = select.select(socket_list , [], [])

        # Handle each socket that is read from
        for notified_socket in read_sockets:

            # Handle message from server
            if notified_socket == server_socket:
                message = server_socket.recv(BUFFER_SIZE).decode()
                # If server shuts down, recv will return an empty string
                if not message:
                    server_socket.shutdown(2)
                    server_socket.close()
                    print("\rDisconnected from the server")
                    sys.exit()
                # Erase the current line, then print the received message
                sys.stdout.write('\r')
                sys.stdout.flush()
                sys.stdout.write(message)
                user_input(username)
                
            # Handle input from user
            else:
                message = sys.stdin.readline()
                server_socket.send(message.encode())
                user_input(username)

    server_socket.close()   #close connection

if __name__ == "__main__":
    irc_client()