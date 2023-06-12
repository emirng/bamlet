import asyncio
from bamlet import Bamlet

app = Bamlet()

resources = {
    '/': 'index.html',
    '/example1.html': 'example1.html',
    '/example2.txt': 'example2.txt',
    '/bamlet.png': 'bamlet.png',
}

extension_content_type = {
    'html': 'text/html',
    'txt':  'text',
    'png':  'image/png',
}



def quick_response( client, status ):
    text = {
        404: 'NOT FOUND',
        405: 'METHOD NOT ALLOWED',
    }[status]

    r = f"""HTTP/1.0 {status} {text}
Content-Length: {len(text)}
Content-Type: text

{text}"""
    client.send( r.encode() )
    client.close()


@app.handle_client()
async def handle_client( client, receiver ):
 
    # wait for header data 
    header = None
    buffer = bytes() 
    while True:
        buffer += await receiver()
        if b'\r\n\r\n' in buffer:
            header = buffer.split(b'\r\n\r\n')[0]
            break
    header = header.decode().split("\r\n")[0]

    request_method, request_path, *_ = header.split(" ")

    if request_method != 'GET':
        return quick_response( client, 405 )

    _file = resources.get(request_path)

    if _file is None:
        return quick_response( client, 404 )

    extension = _file[_file.find('.')+1:]
    content_type = extension_content_type[extension]

    with open( 'examples/example_003_http/{0}'.format( _file ), 'rb') as f:
        content = f.read()

    header = f"""HTTP/1.1 200 OK
Content-Length: {len(content)}
Content-Type: {content_type}

"""

    r = header.encode() + content
    client.send(r)
    client.close()

 
def main():
    app.run( 'localhost', 8080 )


async def main_async():
    try:
        await app.run_async( 'localhost', 8080 )
    except asyncio.exceptions.CancelledError:
        pass


if __name__ == "__main__":
    main()


