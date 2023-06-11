import asyncio
import signal

class Net:

    def run(host,port,impl):
        n = Net(impl)
        asyncio.run(n.listen(host,port))

    async def run_async(host,port,impl):
        n = Net(impl)
        await n.listen(host,port)

    def shutdown(self):
        self.server.close()

    def __init__(self,impl):
        self.impl = impl
        self.running = True
        Net.net = self

    async def handle_echo(self, reader, writer):
        from net import Socket

        connection = Socket(writer)
        self.impl.on_connection(connection)           

        while True:
            data = await reader.read(100)
            if len(data) == 0:
                break
            self.impl.on_data(connection, data)
 
    async def listen(self,host,port):
        self.server = server = await asyncio.start_server(
            self.handle_echo, host, port)

        self.impl.server = server

        try:
            async with server:
                await server.serve_forever()
        except asyncio.exceptions.CancelledError: # try move this elsewhere. out of this class and into the examples files where it is being used?
            pass
