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
cmdList = [{'name': '!list', 'desc': 'list all available chatrooms'}, 
           {'name': '!help', 'desc': 'list all commands'}, 
           {'name': '!leave', 'desc': 'disconnect from the server'}, 
           {'name': '!new', 'desc': 'create a new chatroom'}, 
           {'name': '!join', 'desc': 'join an existing chatroom'}, 
           {'name': '!nick', 'desc': 'change your nickname; use !nick [newNickName]'}]

myAddress = ('', 3333);

class MyClientHandler(socketserver.BaseRequestHandler):
    def handle(self):                         
        print (self.client_address, now() + " has connected.");   
        thisClient = {'addr': self.client_address, 'req': self.request, 'nickname': self.client_address[0]}; #The actual client object referenced in the chatrooms
        firstConnect = True;
        while True:            
            try:
                r, w, x = select.select((self.request,), (self.request,), (), 0); 
                
                if firstConnect:
                    self.request.send(('Hello ' + str(self.client_address[0]) + '! Here is a list of current commands and chatrooms!').encode());
                    self.request.send(helpChatroom().encode());
                    self.request.send((listChatroom()).encode());   
                    self.request.send(("\n\n" + 'Choose a chatroom to join, or make your own!').encode());
                    firstConnect = False;
                
                data = self.request.recv(1024).decode();
                if data:
                    currChatroom = getCurrChatroom(self.client_address); #currChatroom is the index of the current room
                    
                    data = data.strip();
                    
                    if data.startswith('!'):
                        if data == '!help':
                            self.request.send(helpChatroom().encode());
                            
                        elif data == '!list':
                            self.request.send(listChatroom().encode());
                            
                        elif data == '!leave':
                            if currChatroom:
                                leaveChatroom(thisClient, currChatroom);
                            break;
                            
                        elif data[0:4] == '!new':
                            if(checkRoomExists(data[5:])):
                                self.request.send(('The room "' + data[5:] + '" already exists.').encode());
                            else:
                                chatrooms.append({"name": data[5:], "room": [thisClient]});
                                if currChatroom:
                                    leaveChatroom(thisClient, currChatroom);
                                self.request.send(('\nChatroom "' + data[5:] + '" has been created.').encode());
                                    
                        elif data[0:5] == '!join':
                            if(checkRoomExists(data[6:])):
                                joinedChatroom = getChatroomByName(data[6:]);
                                if currChatroom:
                                    leaveChatroom(thisClient, currChatroom);
                                    
                                joinedChatroom['room'].append(thisClient);
                                
                                if checkRoomExists(data[6:]):
                                    for client in getChatroomByName(data[6:])['room']:
                                        client['req'].send(('\n-----Client ' + thisClient['nickname'] + ' has joined the chatroom-----').encode());
                            else:
                                self.request.send(('The room "' + data[6:] + '" does not exist.').encode());
                                
                        elif data[0:5] == '!nick':
                            oldNick = thisClient['nickname'];
                            thisClient['nickname'] = data[6:];
                            if currChatroom:
                                for client in currChatroom['room']:
                                    client['req'].send(('\n-----Client ' + oldNick +  ' has changed their name to ' + thisClient['nickname'] + '-----').encode());
                            else:
                                self.request.send(('Your nickname has been changed to ' + data[6:] + '.').encode());
                            
                        else:
                            self.request.send(('"' + data + '" is not a recognized command.').encode());
                            
                    else:
                        for client in currChatroom['room']:
                            if client == thisClient:
                                continue;
                            client['req'].send(makeMessage(thisClient['nickname'], data).encode());
            except select.error:
                currChatroom = getCurrChatroom(self.client_address);
                if currChatroom:
                    leaveChatroom(thisClient, currChatroom);
                break;
        
        self.request.close();
        print (self.client_address, now() + ' has disconnected.');   

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
    strChatrooms = '\nThe current chatrooms are:'
    for chatroom in range(0, len(chatrooms)):
        strChatrooms += '\n' + str(chatroom) + '. ' + chatrooms[chatroom]['name'];
        
    return strChatrooms;
        
def leaveChatroom(currClient, currChatroom):
    room = currChatroom['room'];
    for client in room:
        if client == currClient:
            room.remove(currClient);
            break;
            
    if not room and currChatroom['name'] != 'default':
        chatrooms.remove(currChatroom);
        
    for client in currChatroom['room']:
        client['req'].send(('\n-----Client ' + currClient['nickname'] + ' has left the chatroom-----').encode());
        
def helpChatroom():
    strCommands = '\nThe current commands are:';
    for cmd in cmdList:
        strCommands += '\n' + cmd['name'] + ': ' + cmd['desc'];
    return strCommands;

def checkRoomExists(name):
    for chatroom in chatrooms:
        if(chatroom['name'] == name):
            return True;
    return False;

def makeMessage(nickName, message):
    appendMessage = '\n(' + now() + ') ' + nickName + ': ' + message;
    return appendMessage;

msgServer = socketserver.ThreadingTCPServer(myAddress, MyClientHandler);
msgServer.serve_forever();
