__author__ = 'wallsr'


from twisted.internet import protocol, reactor


class CounterServer(protocol.Protocol):
    def __init__(self, factory):
        self.connected_peers = []
        self.new_peers = []
        self.factory = factory

    def connectionMade(self):
        self.factory.clients.add(self)

    def dataReceived(self, message):
        #Remove the newlines
        message = message.strip()
        IP = self.transport.getHost().host

        if IP not in self.connected_peers:
            self.new_peers.append(IP)

        if message == "ping":
            self.handle_ping(IP)
        elif message == "hello":
            print 'Hello from: %s' %IP
            self.connected_peers.append(IP)
            self.new_peers.append(IP)
        elif message == "goodbye":
            self.connected_peers.remove(IP)
        else:
            pass

    def handle_ping(self, IP):
        for client in self.factory.clients:
            client.transport.write(';'.join(self.new_peers))

        self.new_peers = []


class CounterServerFactory(protocol.Factory):
    def __init__(self):
        self.clients = set()

    def buildProtocol(self, addr):
        return CounterServer(self)


reactor.listenTCP(1234, CounterServerFactory())
reactor.run()