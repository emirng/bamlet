import asyncio
import colorama
import inspect
from net import Net
from net import Socket
from colorama import Fore as cF
from colorama import Style as cS

colorama.init()

class Bamlet:

    handlers = set()

    def __init__( self ):
        self.on_message_func = None
        self.handle_client_func = None
        self.stream_async = True
        Bamlet.app = self


    def run( self, host, port ):
        print(f" * Serving {cF.BLUE}bamlet{cS.RESET_ALL} app")
        print(f" * Running on {cF.CYAN}{host}:{cF.MAGENTA}{port}{cS.RESET_ALL}")
        Net.run( host, port, self )


    async def run_async( self, host, port ):
        print(f" * Serving {cF.BLUE}bamlet{cS.RESET_ALL} app")
        print(f" * Running on {cF.CYAN}{host}:{cF.MAGENTA}{port}{cS.RESET_ALL}")
        await Net.run_async( host, port, self )


    def shutdown( self ):
        for handler in self.handlers:
            handler.cancel()
        self.server.close()


    def on_connection( self, socket ):
        from bamlet import Client
        from bamlet import Receiver
        from bamlet import MessageQueue
        if type(socket) != Socket: raise TypeError()                

        loop = asyncio.get_event_loop()

        if self.stream_async:
            socket.__stream = stream = asyncio.streams.StreamReader()
        else:
            socket.__stream = stream = bytearray()

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
                    args.append( Receiver( stream )  )
                elif parameter == 'message_queue':
                    args.append( MessageQueue( stream, separator = b'\r\n' ) )
                else:
                    raise ValueError( f'@handle_client got unknown parameter: {parameter}' )

            self.handlers.add( asyncio.ensure_future(
                loop.create_task( f(*args) )
            ))


    def on_data( self, socket, data ):
        if self.stream_async:
            socket.__stream.feed_data( data )
        else:
            socket.__stream += data

    # TODO: add delimiter argument
    def on_message( self, *args, **kwargs ):
        def inner( func ):
            self.on_message_func = func
            return func
        return inner


    def handle_client( self, *args, **kwargs ):

        if kwargs.get('stream_async') is False:
            self.stream_async = False

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


