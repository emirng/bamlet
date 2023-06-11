class MessageQueue:

    def __init__(self, client):
        self.client = client


    def __iter__(self):
        self.queue_string = ""
        return self

    def __next__(self):
        string = self.buffer_to_string()
        assert type(string) == str, type(string)

        self.queue_string += string 
        if '\r\n' in self.queue_string:
            r = self.queue_string[:self.queue_string.find('\r\n')]
            self.queue_string = self.queue_string[self.queue_string.find('\r\n')+2:]
            return r

        raise StopIteration


    def buffer_to_string(self):
        b = self.client.buffer
        self.client.buffer = bytes()
        return b.decode()


