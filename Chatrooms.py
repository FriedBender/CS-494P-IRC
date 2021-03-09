
import socket

# Globals
DEFAULT_ROOM_NAME = '#default'


# Broadcast a message to the server and to all clients in that room
def message_broadcast(room, sender_name, sender_socket, message):
    print(f"{room.name} : {sender_name} > {message}", end='\r')

    # Send the message to all clients except the one that sent the messaage
    for client_socket in room.client_sockets:
        if client_socket != sender_socket:
            client_socket.send(f"{room.name} : {sender_name} > {message}".encode())


# The container that has rooms, which have lists of clients
class IRC_Application:
    def __init__(self):
        self.rooms = {}  # Create a dictionary of rooms with the room name as the key and the room object as the value

    # Function to create a space-separated list of rooms
    def list_all_rooms(self):
        room_list = ""
        for room in self.rooms.values():
            room_list = room_list + room.name + ' '
        room_list = room_list + '\n'
        return room_list

    # Check if the room name begins with '#', check if user is already in the room,
    # create the room if it does not exist, then join the room the user specified
    def join_room(self, room_to_join, sender_socket, sender_name):
        if room_to_join[0] != '#':
            sender_socket.send("Error: Room name must begin with a '#'\n".encode())
        else:
            if room_to_join not in self.rooms:  # Assume that the room does not exist yet
                new_room = Chatroom(room_to_join)
                self.rooms[room_to_join] = new_room
                self.rooms[room_to_join].add_new_client_to_chatroom(sender_name, sender_socket)
            else:  # otherwise, go through the room members to make sure that the sender is not in it already
                for current_members in self.rooms[room_to_join].client_sockets:
                    if sender_socket == current_members:
                        sender_socket.send(f"Error: You are already in the room: {room_to_join}\n".encode())
                    else:
                        # if we are here then the room exists and the sender is not in it.
                        self.rooms[room_to_join].add_new_client_to_chatroom(sender_name, sender_socket)

    # Check if the room exists, check if user is in the room,
    # remove user from room and delete room if it is empty
    def leave_room(self, room_to_leave, sender_socket, sender_name):
        if room_to_leave not in self.rooms:
            sender_socket.send("Error: Room does not exist\n".encode())
        elif sender_socket not in self.rooms[room_to_leave].client_sockets:
            sender_socket.send("Error: You are not in that room\n".encode())
        else:
            self.rooms[room_to_leave].remove_client_from_chatroom(sender_name, sender_socket)
            if not self.rooms[room_to_leave].client_sockets:
                self.rooms.pop(room_to_leave)

    # Check if rooms exist, check if user is in rooms,
    # if room exists and user is in it then send message, otherwise skip
    def message_rooms(self, rooms_to_send, sender_socket, sender_name, message):
        for room in rooms_to_send:
            if room not in self.rooms:
                sender_socket.send(f"Error: {room} room does not exist\n".encode())
                continue
            if sender_socket not in self.rooms[room].client_sockets:
                sender_socket.send(f"Error: You are not in the {room} room\n".encode())
                continue
            message_broadcast(self.rooms[room], sender_name, sender_socket, message)

    def message_parse(self, sender_socket, sender_name, message):
        # Case where message is not a command:
        # The message is sent to the default channel
        if message[0] != '/':
            message_broadcast(self.rooms[DEFAULT_ROOM_NAME], sender_name, sender_socket, message)

        # Case where user wants to list all rooms:
        elif message.split()[0] == "/list" and len(message.split()) == 1:
            room_list = self.list_all_rooms()
            sender_socket.send(room_list.encode())

        # Case where user wants to join a room:
        elif message.split()[0] == "/join":
            if len(message.strip().split()) < 2:
                sender_socket.send(f"/join requires a #roomname argument.\nPlease enter: /join #roomname\n".encode())
            else:
                self.join_room(message.split()[1], sender_socket, sender_name)

        # Case where user wants to leave a room:
        elif message.split()[0] == "/leave":
            if len(message.strip().split()) < 2:
                sender_socket.send(f"/leave requires a #roomname argument.\nPlease enter: /leave #roomname\n".encode())
            else:
                room_to_leave = message.strip().split()[1]
                if room_to_leave[0] != "#":
                    sender_socket.send(f"/leave requires a #roomname argument to begin with '#'.\n".encode())
                else:
                    self.leave_room(room_to_leave, sender_socket, sender_name)

        # Case where user wants to send messages to rooms:
        # Parse the string for rooms and add rooms to a list
        # Pass the rest of the string along as the message
        elif message.split()[0] == "/send":
            rooms_to_send = []
            message_to_send = []
            convert_to_str = ""  # empty string to convert array into string
            # Add all the arguments beginning with # to a list of rooms
            if len(message) < 2:
                sender_socket.send(f"/send requires a #roomname(s) argument(s).\nPlease enter: /join #roomname(s)\n".encode())
            else:
                for word in message.split():
                    if word[0] == '#':
                        rooms_to_send.append(word)
                    elif word[0] == '/':
                        continue
                    else:   # Assume the message is the string after the last room
                        message_to_send.append(word)
                if rooms_to_send.count == 0:
                    sender_socket.send(f"/send at least one #roomname(s) argument(s).\nPlease enter: /join #roomname(s)\n".encode())
                else:
                    convert_to_str = ' '.join([str(word) for word in message_to_send])
                    message_to_send.append('\n')

                    self.message_rooms(rooms_to_send, sender_socket, sender_name, convert_to_str)
        # elif message.split()[0] == "/pm":


class Chatroom:
    # Give a Chatroom a name and list of client's sockets in this room
    def __init__(self, room_name):
        self.name = room_name
        self.client_sockets = []

    # Adds a new client to a chatroom and notifies clients in that room
    def add_new_client_to_chatroom(self, client_name, new_socket):
        self.client_sockets.append(new_socket)
        message = f"{client_name} has joined the room.\n"
        message_broadcast(self, client_name, new_socket, message)

    # Removes an existing client from a chatroom and notifies the clients in that room
    def remove_client_from_chatroom(self, client_name, client_socket):
        self.client_sockets.remove(client_socket)
        message = f"{client_name} has left the room.\n"
        message_broadcast(self, client_name, client_socket, message)