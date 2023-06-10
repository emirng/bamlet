import asyncio
from syrup import Syrup

class Handler:

    def on_connection(self,conn):
        pass

    def on_data(self,conn,data):
        print(data)

server = Syrup.create_server(Handler())
asyncio.run(server.listen('localhost',9000))


