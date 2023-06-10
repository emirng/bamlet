import asyncio
from net import Net
from net import Socket

class Handler:

    def on_connection(self, socket):
        pass

    def on_data(self, socket, data):
        if type(socket) != Socket: raise TypeError()
        socket.close()

server = Net.create_server(Handler())
asyncio.run(server.listen('localhost',9001))


