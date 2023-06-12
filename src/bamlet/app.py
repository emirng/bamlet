import asyncio
import inspect
from net import Net
from net import Socket

class Bamlet:

    handlers = set()

    def __init__( self ):
        self.on_message_func = None
        self.handle_client_func = None
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
        from bamlet import Client
        from bamlet import Receiver
        if type(socket) != Socket: raise TypeError()                

        loop = asyncio.get_event_loop()
        socket.__stream = stream = asyncio.streams.StreamReader()

        # if @on_message
        if self.on_message_func:

            # TODO: this handlers set can get really big if we never discard any of the
            #       "futures" it holds. we should discard on disconnect.
            self.handlers.add( asyncio.ensure_future(
                loop.create_task( self._on_message_handler( socket ) )
            ))

        # if @handle_client
        if self.handle_client_func:
            f = self.handle_client_func
            args = [] 
            for parameter in inspect.signature(f).parameters:
                if parameter == 'client':
                    args.append( Client( socket ))
                elif parameter == 'receiver':
                    args.append( Receiver(stream)  )
                else:
                    raise ValueError( f'@handle_client got unknown parameter: {parameter}' )

            self.handlers.add( asyncio.ensure_future(
                loop.create_task( f(*args) )
            ))


    def on_data( self, socket, data ):
        socket.__stream.feed_data( data )


    # TODO: add delimiter argument
    def on_message( self, *args, **kwargs ):
        def inner( func ):
            self.on_message_func = func
            return func
        return inner


    def handle_client( self, *args, **kwargs ):
        def inner( func ):
            self.handle_client_func = func
            return func
        return inner


    async def _on_message_handler( self, socket ):
        while True:
            msg = await socket.__stream.readuntil( b'\r\n' )
            if len(msg) == 0: break
            r = self.on_message_func( message=msg.decode()[:-2] )
            if r is None: break
            socket.send( r.encode() )


