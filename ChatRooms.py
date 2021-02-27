
import socket


# Globals
PORT_NUMBER = 5050
MESSAGE_BUFFER = 2048   # Max number of Bytes to send/recv
MAX_NUMBER_OF_CLIENTS = 10  # Maxmimum number of clients
DEFAULT_ROOM_NAME = 'default'


# The container that has rooms, which have members:
class IRC_Application:
    def __init__(self):
        self.rooms = {}  # Want a dictionary
        # since key:value pairs are easier to search

    def getUserName(self, new_connected_member):
        new_connected_member.socket.sendall(b'What is your name?: ')

    def Message_Parse(self, member, message):
        command = {
            '/join': 'Create or Join an existing room by using /join roomname',
            '/leave': 'Leave the chatroom',
            '/list': 'List all Chatrooms',
            '/pm': 'private message using /pm username',
            '/man': 'Show instructions',
            '/quit': 'Quit the server'
        }

        if "name: " in message:
            member.name = message.split()[1]

        elif "/join" in message:
            if len(message.split()) >= 2:   # first part of the string will be a command
                #   Second part will be the room name.

                room_Name = message.split()[1]  # Get the name of the room.
                if room_Name in self.rooms:
                    if member.name in self.rooms[room_Name].members:
                        member.socket.sendall(b'You are already in room: ' + room_Name.encode())
                    else:
                        self.rooms[member.activeRoom].Remove_Member_From_ChatRoom(member)
                        self.rooms[room_Name].Add_New_Member_to_ChatRoom(member)
                else:
                    create_New_Room = self.rooms(room_Name)
                    self.rooms[room_Name] = create_New_Room
            member.socket.sendall(command.encode())


class ChatRoom:
    # give a ChatRoom a name and list of members in this room:
    def __init__(self, name):
        self.name = name
        self.members = []   # a simple array to hold members sockets

    def Add_New_Member_to_ChatRoom(self, member):
        message = 'Welcome '
        + member.name
        + ' to the server '
        + self.name
        + '\n'

        self.members.append(member)  # Add the member to the chatroom name
        self.Send_Message_To_All(member, message.encode)
        # sendall() is NOT sending to ALL, just makes
        # sure that the whole message is sent.

    def Remove_Member_From_ChatRoom(self, member):
        message = b"User :" + member.name.encode() + b" has left " + self.name.encode()
        self.members.remove(member)
        self.Send_Message_To_All(member, message)
        # sendall() is NOT sending to ALL, just makes
        # sure that the whole message is sent.

    def Send_Message_To_All(self, member, message):
        message = member.name.encode() + b": " + message
        for membersInChatRoom in self.members:
            membersInChatRoom.socket.sendall(message.encode())
            # sendall() is NOT sending to ALL, just makes
            # sure that the whole message is sent.


# This is the member that will be assigned to one chat room at a time.
class Member:
    def __init__(self, socket, name, activeRoom):
        self.socket = socket
        self.name = name
        self.activeRoom = activeRoom
