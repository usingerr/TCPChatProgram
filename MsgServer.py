# -*- coding: utf-8 -*-
"""
Created on Tue Oct 30 21:54:43 2018

@author: scalesen
"""

import socketserver, time;
import json;

chatrooms = [];
myAddress = ('', 3333);

def getChatroom(addr):
    for chatroom in range(0, len(chatrooms)):
        for client in chatroom[chatroom]:
            if client['addr'] == addr:
                return chatroom;
            
def leaveChatroom(addr):

def now():
    return time.ctime(time.time())

class MyClientHandler(socketserver.BaseRequestHandler):
    def handle(self):                         
        print (self.client_address, now());   
        while True:                             
            data = self.request.recv(1024).decode();
        
            data = json.loads(data);
            
            if data['n']:
                chatrooms.append({"addr": self.client_address, "req": self.request});
            elif data['r']:
                strChatrooms = 'Chatrooms:'
                for index in range(0, len(chatrooms)):
                    strChatrooms += (index + 1);
                self.request.send(strChatrooms.decode());
            elif data['j']:
                chatrooms[data['j'] - 1].append({"addr": self.client_address, "req": self.request});
            elif data['e']:
                
                break
            elif data['m']:
                currChatroom = getChatroom(self.client_address);
                for client in chatrooms[currChatroom]:
                    if client.addr == self.client_address:
                        continue
                    client.request.send(data['m'].encode());
        
        self.request.close();

msgServer = socketserver.ThreadingTCPServer(myAddress, MyClientHandler);
msgServer.serve_forever();
