import socket
import struct

from values import BUFFER_SIZE
from get_time import get_time

class Rdt3_0():

    def __init__(self, socket, isServer):
        self.sock = socket
        self.isServer = isServer

    def formatted_print(self, msg):
        if (self.isServer): 
            print(f"{msg} {get_time()}")

    def extract(self, rcvpkt):
        msg_size, ack, seq, msg_encoded = struct.unpack(f"i2i200s", rcvpkt)
        msg = msg_encoded[:msg_size].decode()
        return msg_size, ack, seq, msg
    
    def wait_for_seq(self, seq, initial_address=None):
        state = f'S{seq}'
        self.formatted_print(f"rdt_receiver | Esperando sequência {seq}...")

        while state == f'S{seq}':
            data, address = self.sock.recvfrom(BUFFER_SIZE)
            _, _, return_seq, return_msg = self.extract(data)
            
            if (return_seq == seq) and ((initial_address == address) or (initial_address == None)):
                sndpkt = self.make_pkt(ack=seq^1, seq=seq^1, msg='OK')
                state = f'S{seq^1}'
                self.formatted_print(f"rdt_receiver | Recebido pacote com sequência {return_seq}, enviando ACK {seq^1}...")
            else:
                sndpkt = self.make_pkt(ack=seq, seq=seq, msg='NO')
                self.formatted_print(f"rdt_receiver | Recebido pacote com sequência {return_seq}, enviando NACK {seq}...")

            self.sock.sendto(sndpkt, address)
        
        return return_msg, address
            
    def wait_for_ack(self, address, ack_value, sndpkt):
        state = f'A{ack_value}'

        while state == f'A{ack_value}':
            try:
                data, recv_address = self.sock.recvfrom(1024)
                _, return_ack, _, _ = self.extract(data)

                if (recv_address == address) and (return_ack == ack_value^1):
                    self.sock.settimeout(None)
                    state = f'A{ack_value^1}'
                    self.formatted_print(f"rdt_sender   | Recebido ACK {return_ack}, esperando próximo passo...")

                    return True
                else:
                    continue
            
            except socket.timeout:
                self.sock.sendto(sndpkt, address) 
                self.sock.settimeout(2)
                self.formatted_print(f"rdt_sender   | Timeout. Reenviando pacote com ACK {ack_value}...")

    def make_pkt(self, ack:int, seq:int, msg:str):
        msg_size = len(msg)
        msg = msg.ljust(200, "#")
        msg_encoded = msg.encode()

        packet_made = struct.pack(f"i2i200s", msg_size, ack, seq, msg_encoded)
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
    
    def receive(self):
        _, initial_address = self.wait_for_seq(0)
        data, address = self.wait_for_seq(1, initial_address)

        return data, address

class Server(Rdt3_0):
    def __init__(self, socket):
        super().__init__(socket, True)

class Client(Rdt3_0):
    def __init__(self, socket):
        super().__init__(socket, False)