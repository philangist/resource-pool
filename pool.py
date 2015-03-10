class _Accumulator(object):

    def __init__(self, start=0):
        self.value = start

    def next(self):
        self.value += 1
        return self.value

_accumulator = _Accumulator()


def new_connection_name(accumulator=_accumulator):
    return 'Connection number %d' % accumulator.next()


class Connection(object):

    def __init__(self, id=new_connection_name()):
        self.id = id
        self.called = 0
        self.data = None

    def __unicode__(self):
        return '%s(%s)' % (self.__class__.__name__, self.id)
    __repr__ = __unicode__
    __str__ = __unicode__

    def call(self):
        self.called += 1
        print 'Called connection %s' % self


class ConnectionPool(object):

    def __init__(self, connections=[]):
        self.available_connections = connections
        self.used_connections = {}

    def add_connection(self, connection):
        assert isinstance(connection, Connection)
        assert not self.used_connections.get(connection.id)
        assert not connection in self.available_connections
        self.available_connections.add(connection)

    @property
    def size(self):
        return len(self.available_connections) + len(self.used_connections)

    def new_connection(self):
        connection = self.available_connections.pop(0)
        self.used_connections[connection.id] = connection
        return connection

    def release_connection(self, connection):
        if connection.id in self.used_connections:
            connection = self.cleanup(connection)
            del self.used_connections[connection.id]
            self.available_connections.append(connection)

    def cleanup(self, connection):
        connection.data = None
        return connection

    def flush(self):
        self.available_connections = []
        self.used_connections = {}
