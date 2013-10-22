#!/usr/bin/env python2.7
__author__ = 'wallsr'
import struct


from twisted.internet import protocol, reactor


class CounterServer(protocol.Protocol):
    def __init__(self, factory):
        self.connected_peers = []
        self.new_peers = []
        self.factory = factory
        self.data = ''

    def connectionMade(self):
        self.factory.clients.add(self)
        self._handle_data = self.handle_data()
        self._next_length = self._handle_data.next()

    def dataReceived(self, data):
        data = self.data + data
        next_length = self._next_length

        while len(data) >= next_length:
            data_send, data = data[:next_length], data[next_length:]
            next_length = self._handle_data.send(data_send)

        self.data = data
        self._next_length = next_length

    def handle_data(self):
        while True:
            size, = struct.unpack('!I', (yield 4))
            message = yield size
            #Remove the newlines
            message = message.strip()
            IP = self.transport.getHost().host

            print '%s from: %s' % (message, IP)

            if IP not in self.connected_peers:
                self.new_peers.append(IP)

            if message == "ping":
                self.handle_ping(IP)
            elif message == "hello":
                self.connected_peers.append(IP)
                self.new_peers.append(IP)
            elif message == "goodbye":
                self.connected_peers.remove(IP)
            else:
                pass

    def handle_ping(self, IP):
        client_str = str(';'.join(self.new_peers))

        for client in self.factory.clients:
            length = struct.pack('!I', len(client_str))
            client.transport.write(length + client_str)

        self.new_peers = []


class CounterServerFactory(protocol.Factory):
    def __init__(self):
        self.clients = set()

    def buildProtocol(self, addr):
        return CounterServer(self)


reactor.listenTCP(1234, CounterServerFactory())
reactor.run()
