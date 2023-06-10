import asyncio
import signal
import socket

class Socket:

    def __init__(self,client):
        self.ons = dict()
        self.client = client

    def on(self, *args, **kwargs):
        self.ons[args[0]] = args[1]

    async def send(self, t):
        await self.client.sendall(t)

    def close(self):
        self.connection_recv_future.cancel()
        self.client.close()

class Server:

    def __init__(self,impl):
        self.impl = impl
        self.running = True

    def get_shutdown_signal_types(self):
        return [signal.SIGINT, signal.SIGTERM]

    async def _shutdown(self):
        print(" ...SIGINT or SIGTERM picked up")
        self.running = False 
        if self.accept_future is not None:
            self.accept_future.cancel()
        
    async def listen(self,host,port):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((host, port))
        server.listen()
        server.setblocking(False)
        loop = asyncio.get_event_loop()

        # assign shutdown task to shutdown signals
        loop = asyncio.get_event_loop()
        for signal_type in self.get_shutdown_signal_types():
            loop.add_signal_handler(signal_type, lambda: asyncio.create_task(self._shutdown()))

        while self.running:

            client = None
            try:
                self.accept_future = asyncio.ensure_future(loop.sock_accept(server))
                client, _ = await self.accept_future
            except asyncio.exceptions.CancelledError:
                print("cancel sock accept")

            if client:
                connection = Socket(client)
                self.impl.on_connection(connection)           
                loop.create_task(self._handle_client(connection))

    async def _handle_client(self, connection):
        loop = asyncio.get_event_loop()
        while True:
            try:
                connection.connection_recv_future = asyncio.ensure_future(
                    loop.sock_recv(connection.client, 255)
                )
                request = await connection.connection_recv_future
            except asyncio.exceptions.CancelledError:
                print("cancel sock accept")
                break
            except OSError:
                print("error")
                break

            self.impl.on_data(connection, request)


class Net:

    def create_server(impl):
        return Server(impl)

