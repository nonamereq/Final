#!/bin/python2
import xmlrpclib
from SimpleXMLRPCServer import SimpleXMLRPCServer

def is_even(n):
    return n % 2 == 0

def print_lower(string):
    print string
    return string.lower()

server = SimpleXMLRPCServer(("localhost", 8000))
print "Listening on port 8000..."
server.register_function(is_even, "is_even")
server.register_function(print_lower, "lower")
server.serve_forever()
