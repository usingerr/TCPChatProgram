# -*- coding: utf-8 -*-
"""
Created on Tue Oct 30 21:54:43 2018

@author: scalesen
"""

import socketserver, time;

chatrooms = [{'name': 'default', 'room': []}];
cmdList = [{'name': '!list', 'desc': ''}, {'name': '!help', 'desc': ''},{'name': '!leave', 'desc': ''}, {'name': '!new', 'desc': ''}, {'name': '!join', 'desc': ''}, {'name': '!nick', 'desc': ''}]
myAddress = ('', 3333);

class MyClientHandler(socketserver.BaseRequestHandler):
    def handle(self):                         
        print (self.client_address, now());   
        firstConnect = True;
        while True:                             
            data = self.request.recv(1024).decode();
        
            if firstConnect:
                self.request.send(helpChatroom().encode());
                self.request.send(listChatroom().encode());    
                firstConnect = False;
            
            currChatroom = getChatroom(self.client_address);
            currRoom = chatrooms[currChatroom]['room'];
            currClient = getClient(self.client_address);
            if data.startsWith('!'):
                if data == '!help':
                    self.request.send(helpChatroom().encode());
                elif data == '!list':
                    self.request.send(listChatroom().encode());
                elif data == '!leave':
                    poppedClient = leaveChatroom(currClient, currChatroom);
                    for client in currRoom:
                        client['req'].send(('User ' + poppedClient['nickname'] + ' has left the chatroom.').encode());
                    break;
                elif data == '!new':
                    chatrooms.append({"name": data[5:], "room": [{"addr": self.client_address, "req": self.request, "nickname": self.client_address}]});
                elif data == '!join':
                    if(checkRoomExists(data[6:])):
                        chatrooms[data[6:]['room']].append({"addr": self.client_address, "req": self.request, "nickname": self.client_address});
                    else:
                        self.request.send(('The room "' + data[6:] + '" does not exist.').encode());
                elif data == '!nick':
                    currClient['nickname'] = data[6:];
                else:
                    self.request.send(('"' + data + '" is not a recognized command.').encode());
                    
            else:
                for client in currRoom:
                    if client == currClient:
                        continue
                    client['req'].send(makeMessage(currClient['nickname'], data).encode());
        
        self.request.close();

msgServer = socketserver.ThreadingTCPServer(myAddress, MyClientHandler);
msgServer.serve_forever();

def now():
    return time.ctime(time.time());

def getChatroom(addr):
    for chatroom in range(0, len(chatrooms)):
        for client in chatrooms[chatroom]['room']:
            if client['addr'] == addr:
                return chatroom;
            
def getClient(addr, currChatroom):
    for client in currChatroom:
        if client['addr'] == addr:
            return client;

def listChatroom():
    strChatrooms = 'Chatrooms:'
    for chatroom in range(0, len(chatrooms)):
        strChatrooms += '\n' + str(chatroom) + '. ' + chatrooms[chatroom]['name'];
        
    return strChatrooms;
        
def leaveChatroom(currClient, currChatroom):
    room = chatrooms[currChatroom]['room'];
    poppedClient = '';
    for client in room:
        if client == currClient:
            poppedClient = room.remove(currClient);
            break;
            
    if not currChatroom:
        chatrooms.pop(currChatroom);
        
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
    appendMessage = nickName + ' ' + now() + '> ' + message
    return appendMessage
