import asyncio
import socket
from bamlet import MessageQueue

class Client:

    def __init__(self, inner_client : socket.socket):
        #if type(inner_client) != socket.socket: raise TypeError()
        self.inner_client = inner_client
        self.buffer = bytes() 
        self.message_queue = MessageQueue(self)


    async def send(self,text):
        socket = self.inner_client.client
        loop = asyncio.get_event_loop()
        await loop.sock_sendall(socket, text)

    async def send_message(self,text):
        loop = asyncio.get_event_loop()
        await loop.sock_sendall(self.inner_client, text+b"\r\n")



    
    def close(self):
        self.inner_client.client.close()

