import socket

__version__ = '0.4.3'

"""
  NosoSocket

  A class to manage a EOL terminated protocol for NosoCoin, aka NosoP

"""
class NosoSocket:

    def __init__(self, sock=None):
        if sock is None:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.settimeout(30)
        else:
            self.sock = sock
            self.sock.settimeout(30)

    def connect(self, host, port):
        self.sock.connect((host, port))

    def send(self, msg):
        msg = msg + '\r\n'
        msg = str.encode(msg)
        totalsent = 0
        MSGLEN = len(msg)
        while totalsent < MSGLEN:
            sent = self.sock.send(msg[totalsent:])
            if sent == 0:
                raise RuntimeError("socket connection broken")

            totalsent = totalsent + sent

    def receive(self, EOFChar=b'\n'):
        msg = []
        MSGLEN = 1024 * 1024 * 10 # 10 MB
        while len(msg) < MSGLEN:
            chunk = self.sock.recv(MSGLEN-len(msg))
            if chunk.find(EOFChar) != -1:
                msg.append(chunk)
                #print('Found EOFChar')
                #print('Len msg:',len(msg))
                return b''.join(msg).decode('UTF-8')

            msg.append(chunk)
        #print('Did not found EOFChar')
        #print('Len msg:',len(msg))
        return b''.join(msg).decode('UTF-8')

    def close(self):
        self.sock.close()

"""
    NosoNodeInfo

    A class to contain the data provided by asking the status of a node

"""
class NosoNodeInfo:

    def __init__(self, *args):
        if args:
            self.peers = int(args[1])
            self.block = int(args[2])
            self.pending = int(args[3])
            self.sync_delta = int(args[4])
            self.branch = args[5]
            self.version = args[6]
        else:
            self.peers = -1
            self.block = -1
            self.pending = -1
            self.sync_delta = -1
            self.branch = 'NONE'
            self.version = 'UNKNOWN'

"""
    NosoNode

    A class that will ask for the status of a node

"""
class NosoNode:

    def __init__(self, name, host = 'localhost', port = 8080):
        self.sock = NosoSocket()
        self.name = name
        self.host = host
        self.port = port

    def get_info(self):
        error = False
        try:
            self.sock.connect(self.host, self.port)
            self.sock.send('NODESTATUS')
            response = self.sock.receive()

        finally:
            self.sock.close()

        elements = response.split()

        if elements[0] == 'NODESTATUS':
            return NosoNodeInfo(*elements)
        else:
            print('Wrong response from node')
            return None

"""
    NosoPoolInfo

    A class to contain the data provided by asking the status of a pool

"""
class NosoPoolInfo:

    def __init__(self, name, *args):
        self.name = name
        self.miners = list()
        if args:
            self.hash_rate = int(args[1])
            self.fee = int(args[2])
            self.share = int(args[3])
            self.miners_count = int(args[4])
            if self.miners_count > 0:
                for index in range(5, len(args)):
                    miner = args[index].split(':')
                    mi = NosoPoolMiner(*miner)
                    self.miners.append(mi)
        else:
            self.hash_rate = -1
            self.fee = -1
            self.share = -1
            self.miners_count = -1

"""
    NosoPoolMiner

    A class to contain the information of a miner on a pool

"""
class NosoPoolMiner:

    def __init__(self, *args):
        if args:
            self.address = args[0]
            self.balance = int(args[1])
            self.blocks_until_payment = int(args[2])
        else:
            self.address = ''
            self.balance = -1
            self.blocks_until_payment = -1

"""
    NosoPool

    A class that will ask for the status of a pool

"""
class NosoPool:

    def __init__(self, name, host, port, password):
        self.sock = NosoSocket()
        self.name = name
        self.host = host
        self.port = port
        self.password = password

    def get_info(self, address):
        error = False
        try:
            self.sock.connect(self.host, self.port)
            self.sock.send(self.password+' '+address+' STATUS')
            response = self.sock.receive()

        finally:
            self.sock.close()

        elements = response.split()
        #print('Before last:',elements[len(elements)-2])
        #print('Last:',elements[len(elements)-1])

        if elements[0] == 'STATUS':
            return NosoPoolInfo(self.name, *elements)
        else:
            print('Wrong response from node')
            return None

