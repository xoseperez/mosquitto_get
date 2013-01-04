#! /usr/bin/python
# -*- utf-8 -*-
# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4

import sys
import os
import time
import ctypes
import mosquitto
from optparse import OptionParser

value = None

def on_message(obj, msg):

    global value

    try:
        value = ctypes.string_at(msg.payload, msg.payloadlen)
    except:
        value = msg.payload

def main():

    global value

    parser = OptionParser(usage="usage: %prog [options]", version="%prog 0.1", add_help_option=False)
    parser.add_option("-?", "--help", action="help", help="show this help message.")
    parser.add_option('-h', "--host", action="store", dest="host", default='localhost', help="mqtt host to connect to. Defaults to localhost.")
    parser.add_option('-p', "--port", action="store", dest="port", default=1883, help="network port to connect to. Defaults to 1883.")
    parser.add_option("-t", "--topic", action="store", dest="topic", default=False, help="mqtt topic to query.")
    parser.add_option("-o", "--timeout", action="store", dest="timeout", default=5, help="wait for a message this number of seconds.")

    (options, args) = parser.parse_args()
    if not options.topic:
        print "Option 'topic' is required"
        parser.print_help()
        sys.exit(-1)

    client = mosquitto.Mosquitto('mosquitto_get_' + str(os.getpid()))
    client.connect(options.host, options.port)
    client.on_message = on_message
    client.subscribe(options.topic)

    until = time.time() + options.timeout
    while (value==None and time.time() < until):
        client.loop()

    client.disconnect()

    if value != None:
        print value
        sys.exit(0)
    sys.exit(1)

if __name__ == '__main__':
    main()
