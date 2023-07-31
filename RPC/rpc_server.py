#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@Project ：tools 
@File    ：rpc_server.py
@Author  ：yqbao
@Date    ：2022/10/10 16:28 
"""
import pickle
from multiprocessing.connection import Listener
from threading import Thread

from multiprocessing.context import AuthenticationError


class RPCHandler(object):
    def __init__(self):
        self._functions = {}

    def register_function(self, func):
        self._functions[func.__name__] = func

    def handle_connection(self, connection):
        try:
            while True:
                # Receive a message
                func_name, args, kwargs = pickle.loads(connection.recv())
                # Run the RPC and send a response
                try:
                    r = self._functions[func_name](*args, **kwargs)
                    connection.send(pickle.dumps(r))
                except Exception as e:
                    connection.send(pickle.dumps(e))
        except EOFError:
            pass


def rpc_server(handlers, address, authkey):
    sock = Listener(address, authkey=authkey)
    while True:
        try:
            client = sock.accept()
            t = Thread(target=handlers.handle_connection, args=(client,))
            t.daemon = True
            t.start()
        except AuthenticationError:
            pass


# Some remote functions
def add(x, y):
    return x + y


def sub(x, y):
    return x - y


if __name__ == '__main__':
    # Register with a handler
    handler = RPCHandler()
    handler.register_function(add)
    handler.register_function(sub)

    # Run the server
    rpc_server(handler, ('', 17000), authkey=b'peekaboo')
