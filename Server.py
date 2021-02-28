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

    # initialize the new IRC application
    IRCchatrooms = ChatRooms.IRC_Application()
    new_Chat_Room_To_Add = ChatRooms.ChatRoom(ChatRooms.DEFAULT_ROOM_NAME)
    IRCchatrooms.rooms[ChatRooms.DEFAULT_ROOM_NAME] = new_Chat_Room_To_Add
    # tell the server how many clients MAX to listen to:
    IRC_socket.listen(ChatRooms.MAX_NUMBER_OF_CLIENTS)

    connection, address = IRC_socket.accept()   # accept a new connecction
    # initialize the new memeber:
    new_member = ChatRooms.Member(connection, 'Rick', ChatRooms.DEFAULT_ROOM_NAME)
    IRCchatrooms.rooms[ChatRooms.DEFAULT_ROOM_NAME].Add_New_Member_to_ChatRoom(new_member)
    print("New Connection Established: " + str(address))

    # now a loop to keep doing this forever
    # TODO: Fix this to exit normally
    while True:
        # This handles the sending and recieving of data from the server.
        data = connection.recv(ChatRooms.MESSAGE_BUFFER).decode()
        IRCchatrooms.Message_Parse(new_member, data)
        if not data:
            print("invalid data recieved")
        print("From user address: " + str(data))
        data = input(" # ")
        send_To_This_Room = IRCchatrooms.rooms[ChatRooms.DEFAULT_ROOM_NAME]
        send_To_This_Room.Send_Message_To_All(new_member, data)

    connection.close()  # gracefully exit


if __name__ == '__main__':
    IRC_server()
