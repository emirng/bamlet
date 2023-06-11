import asyncio
from net import Net
from net import Socket

class EchoHandler:

    def on_connection(self, socket):
        pass

    def on_data(self, socket, data):
        if type(socket) != Socket: raise TypeError()
        socket.send(data)
        socket.close()


def main():
    server = Net.run( 'localhost', 9001, EchoHandler() )

async def main_async():
    server = await Net.run_async( 'localhost', 9001, EchoHandler() )


