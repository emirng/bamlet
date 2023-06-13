"""

    Example 002: IRC - server

    This is pseudo IRC server. The reason I call it that is because it has just a fraction of 
    functionalities that is expected on a actual IRC-server. It does however have enough
    functionalities to make at least a handshake with a IRC-client.

    The reason this code exist is because to show how one could use bamlet to develop a IRC-server
    of anything similar to an IRC-server.

    The IRC-server makes us of bamlet.handle_client, message_queue and client

    IRC-functionalities:

    * Ping-Pong
      * Server can respond to a ping with pong
      * Server can send ping and if not a valid pong it disconnects client
    * Respond with at least RPL_WELCOME on handshake
    * It has a bamlet bot on it
      * If send something to bamlet bot it responds with a reversed echo string
"""

import asyncio
import random
import time
from bamlet import Bamlet

app = Bamlet()

welcome_messages = """:{server} 001 {nick} :Welcome!
:{server} 251 {nick} :
:{server} 376 {nick} :
"""

SERVER = 'localhost'
TIME_BETWEEN_PINGS = 256
PING_TIMEOUT = 16


def random_ping_message():
    return ':'+''.join(random.choice({'x','j','!'}) for _ in range(16))


@app.handle_client( stream_async = False )
async def handle_client(client, message_queue):
    sent_welcome = False
    pending_ping = None
    next_ping = time.time() + TIME_BETWEEN_PINGS
    client_nick = None

    while True:

        for message in list(message_queue.get()): # for some reason I have to wrap a list here... worth investigate why and how to make it so it doesn't?
            message = message.strip()

            if message.startswith( 'USER' ):
                pass

            elif message.startswith( 'NICK' ):
                client_nick = message.split(' ')[1]
                if not sent_welcome:
                    send_welcome = True
                    welcome_kwargs = { 'server': SERVER, 'nick': client_nick }
                    client.send( welcome_messages.format(**welcome_kwargs).encode() )

            elif message.startswith( 'ISON' ):
                nick = message.split(' ')[1]
                if nick != "bamlet":
                    client.send( f":{SERVER} 303 {client_nick} :\r\n".encode() )
                else:
                    client.send( f":{SERVER} 303 {client_nick} :{nick}\r\n".encode() )
                    
            elif message.startswith( 'PRIVMSG') :
                ms = message.split(' ')
                to = message.split(' ')[1]
                msg_back = ' '.join(ms[2:])[1:][::-1]
                send = f':{to} PRIVMSG {client_nick} :{msg_back}\r\n'
                client.send(send.encode())

            elif message.startswith( 'PING' ):
                ping_message = message.split(' ')[1]
                client.send( f"PONG {ping_message}\r\n".encode() )

            elif message.startswith( 'PONG' ):
                ping_message = message.split(' ')[1]
                if pending_ping is not None:
                    if pending_ping[0] == ping_message:
                        pending_ping = None

        # send PING to client...
        if next_ping < time.time():
            next_ping = time.time() + TIME_BETWEEN_PINGS
            if pending_ping: raise Exception()
            ping_message = random_ping_message()
            client.send( f"PING {ping_message}\r\n".encode() )
            pending_ping = ping_message, time.time()
        
        # .. and if no response before ping timeout close connection
        if pending_ping:
            if time.time() - pending_ping[1] > PING_TIMEOUT:
                client.close()
                # TODO: add QUIT message

        await asyncio.sleep(0.1)


def main():
    app.run( 'localhost', 6667 )


async def main_async():
    try:
        await app.run_async( 'localhost', 6667 )
    except asyncio.exceptions.CancelledError:
        pass


if __name__ == '__main__':
    main()


