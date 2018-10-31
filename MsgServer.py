# -*- coding: utf-8 -*-
"""
Created on Tue Oct 30 21:54:43 2018

@author: scalesen
"""

import socketserver, time;

chatrooms = [{'name': 'default', 'room': []}];
myAddress = ('', 3333);
switch = cmdSwitcher();
defaultCnt = 1

def getChatroom(addr):
    for chatroom in range(0, len(chatrooms)):
        for client in chatroom[chatroom]['room']:
            if client['addr'] == addr:
                return chatroom;
            

def now():
    return time.ctime(time.time())

class MyClientHandler(socketserver.BaseRequestHandler):
    def handle(self):                         
        print (self.client_address, now());   
        firstConnect = True;
        while True:                             
            data = self.request.recv(1024).decode();
        
            if firstConnect:
                self.request.send(helpChatroom().encode());
                self.request.send(listChatroom().encode());                
            
            currChatroom = getChatroom(self.client_address);
            if data.startsWith('!'):
                if data == '!help':
                    self.request.send(helpChatroom().encode());
                elif data == '!list':
                    self.request.send(listChatroom());
                elif data == '!leave':
                    leaveChatroom(self.client_address, currChatroom);
                    break;
                elif data == '!new':
                    chatrooms.append({"name": "default" + str(defaultCnt), "room": [{"addr": self.client_address, "req": self.request, "nickname": self.client_address}]});
                    defaultCnt += 1;
                elif data == '!join':
                    chatrooms[data['j'] - 1].append({"addr": self.client_address, "req": self.request, "nickname": self.client_address});
            else:
                for client in chatrooms[currChatroom]['room']:
                    if client['addr'] == self.client_address:
                        continue
                    client.request.send(data.encode());
        
        self.request.close();

msgServer = socketserver.ThreadingTCPServer(myAddress, MyClientHandler);
msgServer.serve_forever();

def listChatroom():
    strChatrooms = 'Chatrooms:'
    for index in range(0, len(chatrooms)):
        strChatrooms += ' ' + chatrooms[index]['name'];
        
    return strChatrooms;
        
def leaveChatroom(addr, currChatroom):
    room = chatrooms[currChatroom]['room']
    for client in range(0, len(room)):
        if room[client]['addr'] == addr:
            room.pop(client);
            break;
            
    if not room:
        chatrooms.pop(currChatroom);

def helpChatroom():
    return '';


def makeMessage(nickName, message):
    appendMessage = nickName + ' ' + now() + '> ' + message
    return appendMessage
