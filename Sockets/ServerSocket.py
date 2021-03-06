import SocketServer
import json
import threading



class MyTcpServer(SocketServer.TCPServer):

    def initialize(self, command_dict):
        self.command_dict = command_dict
        self.allow_reuse_address = True
    
    def finish_request(self, request, client_address):
    	"""Finish one request by instantiating RequestHandlerClass."""
    	self.RequestHandlerClass(self.command_dict, request, client_address, self)

class MyTcpServerHandler(SocketServer.BaseRequestHandler):

    def __init__(self, command_dict, request, client_address, server):
        self.command_dict = command_dict
        SocketServer.BaseRequestHandler.__init__(self, request, client_address, server)

    def handle(self):
        # self.request is the TCP socket connected to the client
        self.data = self.request.recv(1024).strip()

	if self.data == "sup":
		serializedJsData = json.dumps(self.command_dict)
       		self.request.send(serializedJsData)


class MyTcpServerThread(threading.Thread):
    enabled = False

    def __init__(self):
        while not self.enabled:
            try:
                # Create the server
		HOST, PORT = "192.168.0.143", 9996
                self.MyServerObject = MyTcpServer((HOST, PORT), MyTcpServerHandler)
                self.enabled = True
                threading.Thread.__init__(self)
            except:
                self.enabled = False

    def initialize(self, command_dict):
        self.MyServerObject.initialize(command_dict)

    def run(self):
	self.MyServerObject.serve_forever()   
        	




