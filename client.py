import md5
import datetime

from pool import (
    Connection,
    ConnectionPool,
    new_connection_name,
)


CONNECTION_POOL = ConnectionPool(
    [Connection(new_connection_name()) for i in range(10)]
)


def some_random_data():
    return md5.new(str(datetime.datetime.now())).hexdigest()


class Client(object):
    def __init__(self, connection_pool=CONNECTION_POOL):
        self.connection_pool = connection_pool

    def serial_request(self, parameters=[]):
        """
        This should work for n parameters if n > self.connection_pool.size

        """
        for parameter in parameters:
            connection = self._acquire_connection()
            self._use_connection(connection, parameter)
            self._drop_connection(connection)

    def bulk_request(self, parameters=[]):
        """
        This shouldn't work for n parameters if n > self.connection_pool.size

        """
        connections = []
        for parameter in parameters:
            connection = self._acquire_connection()
            connections.append(connection)
            self._use_connection(connection, parameter)

        self._drop_connections(connections)

    def _acquire_connection(self):
        return self.connection_pool.new_connection()

    def _use_connection(self, connection, data):
        connection.data = data
        print (
            'connection %s is currently storing data %s' %
            (connection, connection.data)
        )
        return connection

    def _drop_connections(self, connections):
        for connection in connections:
            self._drop_connection(connection)

    def _drop_connection(self, connection):
        self.connection_pool.release_connection(connection)


if __name__ == '__main__':
    client = Client()

    client.serial_request([some_random_data() for x in range(10)])
    client.bulk_request([some_random_data() for x in range(10)])
    CONNECTION_POOL.flush()

    connection_pool = ConnectionPool(
        [Connection(new_connection_name()) for i in range(5)]
    )
    client = Client(connection_pool)
    client.serial_request([some_random_data() for x in range(10)])
    client.bulk_request([some_random_data() for x in range(10)])  # this fails
