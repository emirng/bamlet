import asyncio
from net import Net
from net import Socket

class Bamlet:

    handlers = set()

    def __init__( self ):
        self.on_message_func = None
        Bamlet.app = self


    def run( self, host, port ):
        Net.run( host, port, self )


    async def run_async( self, host, port ):
        await Net.run_async( host, port, self )


    def shutdown( self ):
        for handler in self.handlers:
            handler.cancel()

        self.server.close()


    def on_connection( self, socket ):
        if type(socket) != Socket: raise TypeError()                

        socket.__stream = asyncio.streams.StreamReader()
        if self.on_message_func:
            loop = asyncio.get_event_loop()

            # TODO: this handlers set can get really big if we never discard any of the
            #       "futures" it holds. we should discard on disconnect.
            self.handlers.add( asyncio.ensure_future(
                loop.create_task( self._on_message_handler( socket ) )
            ))


    def on_data( self, socket, data ):
        socket.__stream.feed_data( data )

    # TODO: add delimiter argument
    def on_message( self, *args, **kwargs ):
        def inner( func ):
            self.on_message_func = func
            return func
        return inner


    async def _on_message_handler( self, socket ):
        while True:
            msg = await socket.__stream.readuntil( b'\r\n' )
            if len(msg) == 0: break
            r = self.on_message_func( message=msg.decode()[:-2] )
            if r is None: break
            socket.send( r.encode() )


