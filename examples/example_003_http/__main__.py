from bamlet import Bamlet


app = Bamlet()

@app.on_message()
def on_message(message):

    
    request_method, request_path, *_ = message.split(" ")

    _file = resource = {
        '/': 'index.html',
        '/example1.html': 'example1.html',
        '/example2.txt': 'example2.txt'
    }[request_path]

    with open('examples/example_003_http/{0}'.format(_file)) as f:
        index = f.read()

    return """HTTP/1.1 200 OK
Content-Length: {0}
Content-Type: {1}

{2}""".format(len(index), 'text/html' if _file.endswith('.html') else 'text', index)


app.run('localhost', 5012)

