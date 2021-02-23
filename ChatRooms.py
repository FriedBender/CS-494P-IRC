
import socket


# Globals
PORT_NUMBER = 5050
MESSAGE_BUFFER = 2048
MAX_NUMBER_OF_CLIENTS = 10


# The container that has rooms, which have members:
class IRC_Application:
    def __init__(self):
        self.rooms = {}  # Want a dictionary
        # since key:value pairs are easier to search

    def Join_Chat_Room(self, member):
        if len(self.rooms) == 0:
            print("bleh")  # Need to figure out rooms

    # Need a structure(?)/enum for the values defined in the RTF
    # Not sure how to go about that


class ChatRoom:
    # give a ChatRoom a name and list of members in this room:
    def __init__(self, name):
        self.name = name
        self.members = []   # a simple array

    def Add_New_Member_to_ChatRoom(self, member):
        message = "Welcome "
        + member.name
        + " to the server "
        + self.name
        + '\n'

        self.members.append(member)  # Add the member to the chatroom name
        self.Send_Message_To_All(member, message)
        # sendall() is NOT sending to ALL, just makes
        # sure that the whole message is sent.

    def Remove_Member_From_ChatRoom(self, member):
        message = b"User :" + member.name + b" has left " + self.name.encode()
        self.members.remove(member)
        self.Send_Message_To_All(member, message)
        # sendall() is NOT sending to ALL, just makes
        # sure that the whole message is sent.

    def Send_Message_To_All(self, member, message):
        message = member.name.encode() + b": " + message
        for membersInChatRoom in self.members:
            membersInChatRoom.socket.sendall(message)
            # sendall() is NOT sending to ALL, just makes
            # sure that the whole message is sent.


# This is the member that will be assigned to one chat room at a time.
class Member:
    def __init__(self, socket, name, activeRoom):
        self.socket = socket
        self.name = name
        self.activeRoom = activeRoom
