#!/bin/python2

import xmlrpclib

proxy = xmlrpclib.ServerProxy("http://localhost:8000/")
print "3 is even: %s" % str(proxy.is_even(3))
print "100 is even: %s" % str(proxy.is_even(100))

print "ABEL lower: %s" % proxy.lower("ABEL")
