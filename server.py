import cgi
import os
import sys

from socketio import socketio_manage
from socketio.server import SocketIOServer

from socketio.namespace import BaseNamespace

import intrpt
import tutorial

class TermNamespace(BaseNamespace):

    def initialize(self):
        self.sh = intrpt.Shell()
        self.texts = tutorial.texts[:]
        self.next()

    def next(self):
        next_help = self.texts[0].split("\n")
        self.texts = self.texts[1:] + self.texts[0:1]
        for line in next_help:
            self.add_line(line)

    def add_line(self, line):
        print line
        self.emit("update", {"line": cgi.escape(line)})

    def on_code(self, message):
        line = message["line"]
        if line == "next()":
            self.next()
            return
        self.add_line(">>> %s" % line)
        if not self.sh.push(line):
            output = self.sh.flush_output()
            [self.add_line(line) for line in output]

def chat(environ, start_response):
    print "Connection opened."
    if environ['PATH_INFO'].startswith('/socket.io'):
        return socketio_manage(environ, {'/term': TermNamespace})

sio_server = SocketIOServer(
    ('', 8080), chat, 
    policy_server=False)
sio_server.serve_forever()

