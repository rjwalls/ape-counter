#!/usr/bin/env python2.7
__author__ = 'wallsr'

import struct

from ape.protocol.explore import ExploreProtocol
from ape.protocol.factory import ProtocolFactory
from ape.protocol.driver import TesterDriver


class TesterProtocol(ExploreProtocol):
    def send_hello(self):
        self.transport.write(struct.pack('!I', 5) + 'hello')

    def send_ping(self):
        self.transport.write(struct.pack('!I', 4) + 'ping')

    def send_goodbye(self):
        self.transport.write(struct.pack('!I', 7) + 'goodbye')

    def handle_new_client(self, data):
        pass

    def get_message_type(self, message):
        #Use this method to determine message type
        return "new_client"


driver = TesterDriver(TesterProtocol)
driver.run()
