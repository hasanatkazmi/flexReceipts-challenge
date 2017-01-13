#!/usr/bin/env python

import BaseHTTPServer
import json

# API"
# To create matric:
# POST /create/<matric>
# To record a value for matric:
# POST /record/<metric>/<value>
# To retrieve stats for a matric:
# GET /statistics/<metric>


class Matric(object):
    '''Space complexity of Matrix is O(number of values for matrix)'''

    def __init__(self, name):
        super(Matric, self).__init__()
        self.name = name
        self.min_val = None
        self.max_val = None
        self.total = 0
        self.count = 0
        self.arr = []

    def record(self, val):
        # runtime complexity: O(1)
        # space complexity: O(number of value for matric)
        # its optimized to save n/2 values of matrix
        if self.count == 0:
            self.min_val = val
            self.max_val = val
        if self.min_val > val:
            self.min_val = val
        if self.max_val < val:
            self.max_val = val
        self.count += 1
        self.total += val

        self.arr.append(val)
        if len(self.arr) > 2 and self.count % 2 == 1:
            del self.arr[0]

    def summary(self):
        # runtime complexity: O(1)
        if self.count == 0:
            return None

        mean = None
        median = None
        mean = self.total / (self.count * 1.0)
        median = self.arr[0]
        if self.count % 2 == 0:
            median = (self.arr[0] + self.arr[1]) / 2.0
        return {
            'min': self.min_val,
            'max': self.max_val,
            'mean': mean * 1.0,
            'median': median * 1.0
        }


class FlexReciepts(BaseHTTPServer.BaseHTTPRequestHandler):
    '''Space complexity is O(total number of metrics * average number of values in each metric)'''
    records = {}
    ACTION_CREATE = 'create'
    ACTION_RECORD = 'record'
    ACTION_STATS = 'statistics'

    def send_no_cache_headers(self):
        self.send_header(
            'Cache-Control', 'no-cache, no-store, must-revalidate')
        self.send_header('Pragma', 'no-cache')
        self.send_header('Expires', '0')

    def parse_path(self):
        # runtime complexity for parsing is addressed by response code 414 (URI
        # Too Long) RFC 7231
        toparse = self.path.split('/')
        toparse = filter(lambda x: x != '', toparse)
        action = None
        if len(toparse) > 0:
            action = toparse[0].lower()
        matric = None
        if len(toparse) > 1:
            matric = toparse[1]
        value = None
        if len(toparse) > 2:
            try:
                value = int(toparse[2])
            except ValueError:
                pass

        return action, matric, value

    def do_GET(self):
        # runtime complexity for GET /statistics: O(1)
        # space complexity for GET /statistics: O(1)
        # self.send_no_cache_headers()
        action, matric, value = self.parse_path()

        if action != self.ACTION_STATS or matric is None:
            self.send_response(400)
            self.send_no_cache_headers()
            return

        if matric not in self.records:
            self.send_response(204)
            self.send_no_cache_headers()
            return

        stats = self.records[matric].summary()
        if stats is None:
            self.send_response(204)
            self.send_no_cache_headers()
            return

        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(stats))

    def do_POST(self):
        # self.send_no_cache_headers()
        action, matric, value = self.parse_path()

        if (action != self.ACTION_CREATE and action != self.ACTION_RECORD) or \
            (action == self.ACTION_CREATE and matric is None) or \
                (action == self.ACTION_RECORD and (matric is None or value is None)):
            self.send_response(400)
            self.send_no_cache_headers()
            return

        # runtime complexity for POST /create: O(1)
        # space complexity for POST /create: O(number of metrics)
        if action == self.ACTION_CREATE:
            if matric in self.records:
                self.send_response(409)
                self.send_no_cache_headers()
                return
            self.records[matric] = Matric(matric)
            self.send_response(201)
            self.send_no_cache_headers()
            return

        # runtime complexity for POST /record: O(1)
        # space complexity for POST /record: O(number of values in matric)
        if action == self.ACTION_RECORD:
            if matric not in self.records:
                self.send_response(400)
                self.send_no_cache_headers()
                return
            self.records[matric].record(value)
            self.send_response(204)
            self.send_no_cache_headers()
            return


if __name__ == '__main__':
    server_port = 3333
    server = BaseHTTPServer.HTTPServer(('', server_port), FlexReciepts)
    print "Starting Server on port {port}, use <Ctrl-C> to stop".format(port=server_port)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print "Shutting down the server"
        server.socket.close()
        server.shutdown()
