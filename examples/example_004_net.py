import asyncio
from net import Net
from net import Socket

class Handler:

    def on_connection(self, socket):
        pass

    def on_data(self, socket, data):
        if type(socket) != Socket: raise TypeError()
        socket.send(b"x")
        socket.close()

server = Net.run('localhost',9001,Handler())


