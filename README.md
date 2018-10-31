# TCPChatProgram

Step-by-step

Server starts, initializes the list of chat rooms (each chatroom might be a dictionary where the key is the name and the value is a list of IP addresses)

Server starts listening for some number of connections

Client connects to the server automatically (?) and is given a list of current chatrooms

Client connects to a chatroom and a message is sent to others in that room that someone has joined

Clients in rooms together can send messages that the server will receive, append their name and timestamp to, and send to other clients in that same room

If a client doesn’t send a message for some amount of time, or they explicitly leave (maybe a command like “!leave”?) then their connection is closed and their IP is taken off any lists that it’s part of

ideas
Command for changing room name? Nickname? 
