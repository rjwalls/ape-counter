__author__ = 'wallsr'

from ape.protocol.explore import ExploreProtocol

class TesterProtocol(ExploreProtocol):
    def send_hello(self):
        self.transport.write('hello')

    def send_ping(self):
        self.transport.write('ping')

    def send_goodbye(self):
        self.transport.write('goodbye')

    def handle_new_client(self):
        pass

    def get_message_type(self, message):
        #Use this method to determine message type
        return "new_client"

