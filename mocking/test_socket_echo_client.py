#!/usr/bin/env python
# Python Network Programming Cookbook -- Chapter - 1
# This program is optimized for Python 2.7.
# It may run on any other version with/without modifications.

import socket
import sys
import  time

import argparse


def echo_client(host, port):
    """ A simple echo client """
    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Connect the socket to the server
    server_address = (host, port)
    print "Connecting to %s port %s" % server_address
    sock.connect(server_address)

    while True:
        # Send data
        try:
            # Send data
            # message = raw_input()
            # print "Sending %s" % message
            # sock.sendall(message)
            # # Look for the response
            message = raw_input('\ncontinue receive data? [Y / N]')
            sendata = raw_input('send something?\n')
            if sendata is not None:
                sock.sendall(sendata)
            if message == 'N' or message == 'n':
                break
            
            data = sock.recv(1024)
            sock.sendall('reply:'+data)
            print("Received: %s" ) % data
        except socket.errno, e:
            print "Socket error: %s" %str(e)
        except Exception, e:
            print "Other exception: %s" %str(e)
        # finally:
        #     print "Closing connection to the server"
        #     # sock.close()
    print('end connection\n')
    sock.close()
    
if __name__ == '__main__':
    # parser = argparse.ArgumentParser(description='Socket Server Example')
    # parser.add_argument('-port', action="store", dest="port", type=int, required=True)
    # parser.add_argument('-host', action="store", dest="host", type=str, required=True)
    # given_args = parser.parse_args()
    # if given_args.port != None and given_args.host != None:
    #     port = given_args.port
    #     host = given_args.host
    # else:
    #     host = 'localhost'
    #     port = 9876
    # echo_client(host, port)
    stdIn = raw_input('connect to default(localhost:9876) or ip:port\n')
    if stdIn is not None:
        try:
            ip, port = stdIn.split(':')
            echo_client(ip,int(port))
        except Exception as e:
            print('error input:'+e.message)