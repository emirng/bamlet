"""

    Example 002: IRC - server

    This is pseudo IRC server. The reason I call it that is because it has just a fraction of 
    functionallities that is expected on a actual IRC-server. It does however have enough
    functionallities to make a handshake with a IRC-client.

    The reason this code exist is because to show how one could use bamlet to develop a IRC-server
    of anything similar to an IRC-server.

    The IRC-server makes us of bamlet.handle_client, client.message_queue and client.send.

    IRC-functionallities:

    * Ping-Pong
      * Server can respond to a ping with pong
      * Server can send ping and if not a valid pong it disconnects client
    * Respond with a RPL_WELCOME on a User message

"""

import asyncio
import string
import random
import time
from bamlet import Bamlet

app = Bamlet()

welcome_messages = """:{server} 001 {nick} :Welcome!
:{server} 251 {nick} :
:{server} 376 {nick} :
"""


TIME_BETWEEN_PINGS = 256
PING_TIMEOUT = 16

def random_ping_message():
    return ':'+''.join(random.choice({'x','j','!'}) for _ in range(16))

@app.handle_client()
async def handle_client(client):

    sent_welcome = False
    pending_ping = None
    next_ping = time.time() + TIME_BETWEEN_PINGS
    client_nick = None
    server = 'localhost'

    while True:

        mq = list(client.message_queue)
        for message in mq:
            message = message.strip()
            print(message)

            if message.startswith("USER"):
                pass           
            elif message.startswith("NICK"):
                nick = message.split(' ')[1]
                client_nick = nick

                if not sent_welcome:
                    send_welcome = False
                    nick = message.split(' ')[1]
                    welcome_kwargs = { 'server': 'localhost', 'nick': nick }
                    client_nick = nick
                    await client.send(welcome_messages.format(**welcome_kwargs).encode())
 

            elif message.startswith("ISON"):
                nick = message.split(' ')[1]
                if nick != "bamlet":
                    await client.send(f":{server} 303 {client_nick} :\r\n".encode())
                else:
                    await client.send(f":{server} 303 {client_nick} :{nick}\r\n".encode())
                    
            elif message.startswith('PRIVMSG'):
                ms = message.split(' ')
                to = message.split(' ')[1]
                msg = message.split(' ')[2][1:]
                msg_back = msg[::-1]
                msg_back = ' '.join(ms[2:])[1:][::-1]
                send = f':{to} PRIVMSG {client_nick} :{msg_back}\r\n'
                await client.send(send.encode())

            elif message.startswith("PING"):
                ping_message = message.split(' ')[1]
                await client.send(f"PONG {ping_message}\r\n".encode())

            elif message.startswith("PONG"):
                ping_message = message.split(' ')[1]
                if pending_ping is not None:
                    if pending_ping[0] == ping_message:
                        print(",,,")
                        pending_ping = None

        if next_ping < time.time():
            next_ping = time.time() + TIME_BETWEEN_PINGS
            if pending_ping: raise Exception()
            ping_message = random_ping_message()
            await client.send(f"PING {ping_message}\r\n".encode())
            pending_ping = ping_message, time.time()
        
        if pending_ping:
            if time.time() - pending_ping[1] > PING_TIMEOUT:
                client.close()

        await asyncio.sleep(0.1)

def main():
    app.run(host="localhost", port=6667)


if __name__ == '__main__':
    main()
