import asyncio
import signal
import socket

class Socket:

    def __init__(self,client):
        self.ons = dict()
        self.client = client
        self.alive = True

    def on(self, *args, **kwargs):
        self.ons[args[0]] = args[1]

    async def send(self, t):
        await self.client.sendall(t)

    def close(self):
        self.client.close()
        self.alive = False
        #await writer.wait_closed()


class Server:

    def __init__(self,impl):
        self.impl = impl
        self.running = True

    def get_shutdown_signal_types(self):
        return [signal.SIGINT, signal.SIGTERM]

    async def handle_echo(self, reader, writer):

        connection = Socket(writer)
        self.impl.on_connection(connection)           

        

        while connection.alive:
            data = await reader.read(100)
            if len(data) == 0:
                break
            self.impl.on_data(connection, data)

 
    async def listen(self,host,port):
        server = await asyncio.start_server(
            self.handle_echo, host, port)

        async with server:
            await server.serve_forever()

class Net:

    def create_server(impl):
        return Server(impl)

