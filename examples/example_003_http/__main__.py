import asyncio
from bamlet import Bamlet



app = Bamlet()

resource = {
    '/': 'index.html',
    '/example1.html': 'example1.html',
    '/example2.txt': 'example2.txt',
    '/bamlet.png': 'bamlet.png',
}


@app.handle_client()
async def handle_client(client, receiver):
  
    buffer = bytes() 
    header = None


    while True:

        buffer += await receiver()
        print(buffer)

        if b"\r\n\r\n" in buffer:
            header = buffer.split(b"\r\n\r\n")[0]
            break


    header = header.decode().split("\r\n")


    request_method, request_path, *_ = header[0].split(" ")
    _file = resource.get(request_path)

    if _file is None:
        d = b"""HTTP/1.1 404 Not Found
Content-Length: 9
Content-Type: text

Not Found"""
        print(d)
        client.send(d)
        client.close()
        return

    extension_content_type = {
        'html': 'text/html',
        'txt':  'text',
        'png':  'image/png',
    }



    extension = _file[_file.find('.')+1:]
    content_type = extension_content_type[extension]

    with open('examples/example_003_http/{0}'.format(_file),'rb') as f:
        index = f.read()

    content = index
    content_length = len(index)

    header = f"""HTTP/1.1 200 OK
Content-Length: {content_length}
Content-Type: {content_type}"""

    r = header.encode() + b"\n\n" + index
    client.send(r)
    client.close()
 
def main():
    app.run('localhost', 8080)

async def main_async():
    await app.run_async('localhost', 8080)
    pass


if __name__ == "__main__":
    main()


