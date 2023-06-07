import socket
import asyncio
import signal
import colorama
from colorama import Fore as cF
from colorama import Style as cS

colorama.init()




class Bamlet:

    def __init__(self):
        self.running = True
        self.accept_future = None

        # decoraters functions
        self.handle_client_func = None

    # --- decorators
    def on_message(self, *args, **kwargs):
        def inner(func):
            self.on_message_func = func
            return func
        return inner

    def handle_client(self, *args, **kwargs):
        def inner(func):
            self.handle_client_func = func
            return func
        return inner
    # ---

    # --- public methods
    def run(self, host, port):
        asyncio.run(self._inner_run(host,port))


    async def run_async(self, host, port):
        await self._inner_run(host,port)
    # ----

    # --- private methods
    async def _inner_run(self,host,port):
        print(f" * Serving {cF.BLUE}bamlet{cS.RESET_ALL} app")
        self.host = host
        self.port = port

        # assign shutdown task to shutdown signals
        loop = asyncio.get_event_loop()
        for signal_type in self.get_shutdown_signal_types():
            loop.add_signal_handler(signal_type, lambda: asyncio.create_task(self._shutdown()))

        # start server and keep running till it is done
        task_server = asyncio.create_task(self._run_server())
        await task_server


    def get_shutdown_signal_types(self):
        return [signal.SIGINT, signal.SIGTERM]


    async def _run_server(self):
        from bamlet import Client
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((self.host, self.port))
        server.listen()
        server.setblocking(False)
        loop = asyncio.get_event_loop()
        
        print(f" * Running on {cF.CYAN}{self.host}:{cF.MAGENTA}{self.port}{cS.RESET_ALL}")
        while self.running:
            try:
                self.accept_future = asyncio.ensure_future(loop.sock_accept(server))
                client, _ = await self.accept_future
                print("client connect")
                if self.handle_client_func:
                    f = self.handle_client_func
                    c = Client(client)
                    loop.create_task(f( c ))
                    loop.create_task(self.buffer_filler(c))
                else:
                    loop.create_task(self._handle_client(client))
            except asyncio.exceptions.CancelledError:
                print("cancel sock accept")

        print("server closing down... ", end="")
        server.close()
        print("OK!")


    async def buffer_filler(self, client):
        loop = asyncio.get_event_loop()
        while True:
            u = await loop.sock_recv(client.inner_client, 255)
            client.buffer += u 

    async def _handle_client(self, client):

        # TODO: this code is just temp solution. implement an actual buffer handler here

        loop = asyncio.get_event_loop()
        request = (await loop.sock_recv(client, 255)).decode('utf8').strip()
        f = self.on_message_func
        response = f(str(request))
        await loop.sock_sendall(client, response.encode('utf8'))
        print("client closing down... ", end="")
        client.close()
        print("OK!")


    async def _shutdown(self):
        print(" ...SIGINT or SIGTERM picked up")
        self.running = False 
        if self.accept_future is not None:
            self.accept_future.cancel()
    # ---
