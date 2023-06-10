import asyncio
import socket

class Connection:

    def __init__(self,client):
        self.ons = dict()
        self.client = client

    def on(self, *args, **kwargs):
        self.ons[args[0]] = args[1]

    async def send(self, t):
        await self.client.sendall(t)

class Server:

    def __init__(self,impl):
        self.impl = impl

    ons = dict()
    def on(self, *args, **kwargs):
        self.ons[args[0]] = args[1]
        
    async def listen(self,host,port):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((host, port))
        server.listen()
        server.setblocking(False)
        loop = asyncio.get_event_loop()

        while True: 
            try:
                self.accept_future = asyncio.ensure_future(loop.sock_accept(server))
                client, _ = await self.accept_future
                connection = Connection(client)
                self.impl.on_connection(connection)
            except asyncio.exceptions.CancelledError:
                print("cancel sock accept")
            
            loop.create_task(
                self._handle_client(connection)
            )


    async def _handle_client(self, connection):


        loop = asyncio.get_event_loop()
        while True:
            request = (await loop.sock_recv(connection.client, 255))
        #await loop.sock_sendall(client, request)
        #print("client closing down... ", end="")
        #client.close()
        #print("OK!")
            self.impl.on_data(connection, request)




class Syrup:

    def create_server(impl):
        return Server(impl)

