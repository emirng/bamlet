import asyncio
import signal

class Net:

    def __init__( self, handler ):
        self.handler = handler
        Net.net = self


    def run( host, port, handler ):
        net = Net( handler )
        asyncio.run( net.listen( host, port ) )


    async def run_async( host, port, handler ):
        net = Net( handler )
        await net.listen( host, port )


    def shutdown( self ):
        self.server.close()


    async def listen( self, host, port ):
        self.server = server = await asyncio.start_server( self._connect_callback, host, port )
        self.handler.server = server
        async with server:
            await server.serve_forever()


    async def _connect_callback( self, reader, writer ):
        from net import Socket

        connection = Socket( writer )
        self.handler.on_connection( connection ) 

        while True:
            data = await reader.read(256)
            if len(data) == 0: break
            self.handler.on_data( connection, data )
 

