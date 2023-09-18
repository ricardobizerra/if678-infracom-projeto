import struct # what is struct? https://docs.python.org/3/library/struct.html
import socket

class Rdt3_0():

    def __init__(self, socket:socket.socket):
        self.sock = socket

    def extract(self, rcvpkt):
        _, _, seq, msg_encoded = struct.unpack("I32s", rcvpkt)
        msg = msg_encoded.decode()
        return msg, seq
    
    def wait_for_seq(self, seq, initial_address=None):
        while True:
            rcvpkt, address = self.sock.recvfrom(1024)
            rcvmsg, rcvseq = self.extract(rcvpkt)
            if rcvseq == seq and (initial_address == None or address == initial_address):
                return rcvmsg, address
            
    def wait_for_ack(self, address, seq, sndpkt):
        while True:
            try:
                rcvpkt, _ = self.sock.recvfrom(1024)
                rcvmsg, rcvseq = self.extract(rcvpkt)
                if rcvseq == seq:
                    return rcvmsg
            except socket.timeout:
                self.sock.sendto(sndpkt, address)
    
    def make_pkt(self, ack, seq, msg):
        msg_encoded = msg.encode()
        msg_size = len(msg_encoded)

        packet_made = struct.pack("I32s", msg_size, ack, seq, msg_encoded)
        return packet_made
    
    def send(self, msg, address):
        sndpkt = self.make_pkt(1, 0, 'ACK')

        self.sock.sendto(sndpkt, address)
        self.sock.settimeout(2)
        rcvpkt = self.wait_for_ack(address, 0, sndpkt)
        
        sndpkt = self.make_pkt(0, 1, msg)

        self.sock.sendto(sndpkt, address)
        self.sock.settimeout(2)
        rcvpkt = self.wait_for_ack(address, 1, sndpkt)
    
    def deliver(self):
        _, initial_address = self.wait_for_seq(0)
        data, address = self.wait_for_seq(1, initial_address)

        return data, address

class Server(Rdt3_0):
    def __init__(self, socket):
        super().__init__(socket)

class Client(Rdt3_0):
    def __init__(self, socket):
        super().__init__(socket)