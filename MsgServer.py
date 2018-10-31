# -*- coding: utf-8 -*-
"""
Created on Tue Oct 30 21:54:43 2018

@author: scalesen
"""

import socketserver, time;
import json;

chatrooms = [];
myAddress = ('', 3333);
defaultCnt = 1

def getChatroom(addr):
    for chatroom in range(0, len(chatrooms)):
        for client in chatroom[chatroom]['room']:
            if client['addr'] == addr:
                return chatroom;
            
def leaveChatroom(addr, currChatroom):
    room = chatrooms[currChatroom]['room']
    for client in range(0, len(room)):
        if room[client]['addr'] == addr:
            room.pop(client);
            break;
def now():
    return time.ctime(time.time())

class MyClientHandler(socketserver.BaseRequestHandler):
    def handle(self):                         
        print (self.client_address, now());   
        while True:                             
            data = self.request.recv(1024).decode();
        
            data = json.loads(data);
            
            if data['n']:
                chatrooms.append({"name": "default" + str(defaultCnt), "room": [{"addr": self.client_address, "req": self.request, "nickname": self.client_address}]});
                defaultCnt += 1;
            elif data['r']:
                strChatrooms = 'Chatrooms:'
                for index in range(0, len(chatrooms)):
                    strChatrooms += ' ' + chatrooms[index]['name'];
                self.request.send(strChatrooms.decode());
            elif data['j']:
                chatrooms[data['j'] - 1].append({"addr": self.client_address, "req": self.request, "nickname": self.client_address});
            elif data['e']:
                
                break
            elif data['m']:
                currChatroom = getChatroom(self.client_address);
                if data['m'] == '!leave':
                    leaveChatroom(self.client_address, currChatroom);
                    if not chatrooms[currChatroom]:
                        chatrooms.pop(currChatroom);
                    break;
                else:
                    for client in chatrooms[currChatroom]:
                        if client.addr == self.client_address:
                            continue
                        client.request.send(data['m'].encode());
        
        self.request.close();

msgServer = socketserver.ThreadingTCPServer(myAddress, MyClientHandler);
msgServer.serve_forever();

def makeMessage(nickName, message):
    appendMessage = nickName + ' ' + now() + '> ' + message
    return appendMessage
