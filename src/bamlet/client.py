import asyncio

class Client:

    def __init__( self, inner ):
        self._inner = inner


    def send( self, text ):
        self._inner.send(text)

    
    def close( self ):
        self._inner.close()


