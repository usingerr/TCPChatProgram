# -*- coding: utf-8 -*-
"""
Created on Tue Oct 30 21:54:43 2018

@author: scalesen
Network Programming Fall 2018
Final Project - Chat Program
Ross Usinger, Nick Scalese
Server
"""

import socketserver, time, select;

chatrooms = [{'name': 'default', 'room': []}];
cmdList = [{'name': '!list', 'desc': 'list all available chatrooms'}, {'name': '!help', 'desc': 'list all commands'}, {'name': '!leave', 'desc': 'leave your current chatroom'}, {'name': '!new', 'desc': 'create a new chatroom'}, {'name': '!join', 'desc': 'join an existing chatroom'}, {'name': '!nick', 'desc': 'change your nickname; use !nick [newNickName]'}]
myAddress = ('', 3333);

class MyClientHandler(socketserver.BaseRequestHandler):
    def handle(self):                         
        print (self.client_address, now() + " has connected.");   
        thisClient = {"addr": self.client_address, "req": self.request, "nickname": self.client_address[0]}; #The actual client object referenced in the chatrooms
        firstConnect = True;
        while True:            

            r, w, x = select.select((self.request,), (), (), 0); 

            if not r:
                break;                
        
            if firstConnect:
                self.request.send(("Hello " + str(self.client_address[0]) + "! Here is a list of current commands and chatrooms!").encode());
                self.request.send(helpChatroom().encode());
                self.request.send(("\n\n" + listChatroom()).encode());   
                self.request.send(("\n\n" + "Choose a chatroom to join, or make your own!").encode());
                firstConnect = False;
            
            data = self.request.recv(1024).decode();
            if data:
                currChatroom = getCurrChatroom(self.client_address); #currChatroom is the index of the current room
                    
                if data.startswith('!'):
                    if data == '!help':
                        self.request.send(helpChatroom().encode());
                        
                    elif data == '!list':
                        self.request.send(listChatroom().encode());
                        
                    elif data == '!leave':
                        poppedClient = leaveChatroom(thisClient, currChatroom);
                        for client in currChatroom['room']:
                            client['req'].send(('\n-----Client ' + poppedClient['nickname'] + ' has left the chatroom-----').encode());
                        print (self.client_address, now() + " has disconnected."); 
                        break;
                        
                    elif data[0:4] == '!new':
                        if(checkRoomExists(data[5:])):
                            self.request.send(('The room "' + data[5:] + '" already exists.').encode());
                        else:
                            chatrooms.append({"name": data[5:], "room": [thisClient]});
                            if currChatroom:
                                leaveChatroom(thisClient, currChatroom);
                                for client in currChatroom['room']:
                                    client['req'].send(("\n-----Client " + thisClient['nickname'] + " has left the chatroom-----").encode());
                                
                    elif data[0:5] == '!join':
                        if(checkRoomExists(data[6:])):
                            joinedChatroom = getChatroomByName(data[6:]);
                            if currChatroom:
                                joinedChatroom['room'].append(thisClient);
                                leaveChatroom(thisClient, currChatroom);
                                for client in currChatroom['room']:
                                    client['req'].send(("\n-----Client " + thisClient['nickname'] + " has left the chatroom-----").encode());
                            else:
                               joinedChatroom['room'].append(thisClient);
                            
                            if checkRoomExists(data[6:]):
                                for client in getChatroomByName(data[6:])['room']:
                                    client['req'].send(("\n-----Client " + thisClient['nickname'] + " has joined the chatroom-----").encode());
                        else:
                            self.request.send(('The room "' + data[6:] + '" does not exist.').encode());
                            
                    elif data[0:5] == '!nick':
                        thisClient['nickname'] = data[6:];
                        
                    else:
                        self.request.send(('"' + data + '" is not a recognized command.').encode());
                        
                else:
                    for client in currChatroom['room']:
                        print(currChatroom['name'])
                        if client == thisClient:
                            print("Yes")
                            continue;
                        client['req'].send(makeMessage(thisClient['nickname'], data).encode());
        
        self.request.close();

def now():
    return time.ctime(time.time());

def getCurrChatroom(addr):
    for chatroom in range(0, len(chatrooms)):
        for client in chatrooms[chatroom]['room']:
            if client['addr'] == addr:
                return chatrooms[chatroom];
    return [];

def getChatroomByName(name):
    for chatroom in range(0, len(chatrooms)):
        if chatrooms[chatroom]['name'] == name:
            return chatrooms[chatroom];
    return [];
            
def listChatroom():
    strChatrooms = 'The current chatrooms are:'
    for chatroom in range(0, len(chatrooms)):
        strChatrooms += '\n' + str(chatroom) + '. ' + chatrooms[chatroom]['name'];
        
    return strChatrooms;
        
def leaveChatroom(currClient, currChatroom):
    room = currChatroom['room'];
    poppedClient = '';
    for client in room:
        if client == currClient:
            poppedClient = room.remove(currClient);
            break;
            
    if not currChatroom['room']:
        chatrooms.remove(currChatroom);
        
    return poppedClient;

def helpChatroom():
    strCommands = 'The current commands are:';
    for cmd in cmdList:
        strCommands += '\n' + cmd['name'] + ': ' + cmd['desc'];
    return strCommands;

def checkRoomExists(name):
    for chatroom in chatrooms:
        if(chatroom['name'] == name):
            return True;
    return False

def makeMessage(nickName, message):
    appendMessage = "\n" + nickName + ' (' + now() + ' ): ' + message
    return appendMessage

msgServer = socketserver.ThreadingTCPServer(myAddress, MyClientHandler);
msgServer.serve_forever();
