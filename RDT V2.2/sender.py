import random

class SenderProcess:
    """ Represent the sender process in the application layer  """

    __buffer = list()

    @staticmethod
    def set_outgoing_data(buffer):
        """ To set the message the process would send out over the network
        :param buffer:  a python list of characters represent the outgoing message
        :return: no return value
        """
        SenderProcess.__buffer = buffer
        return

    @staticmethod
    def get_outgoing_data():
        """ To get the message the process would send out over the network
        :return:  a python list of characters represent the outgoing message
        """
        return SenderProcess.__buffer


class RDTSender:
    """ Implement the Reliable Data Transfer Protocol V2.2 Sender Side """

    def __init__(self, net_srv):
        """ This is a class constructor
            It initialize the RDT sender sequence number  to '0' and the network layer services
            The network layer service provide the method udt_send(send_pkt)
        """
        self.sequence = '0'
        self.net_srv = net_srv

    @staticmethod
    def get_checksum(data):
       return ord(data) 

    @staticmethod
    def clone_packet(packet):
        """ Make a copy of the outgoing packet
        :param packet: a python dictionary represent a packet
        :return: return a packet as python dictionary
        """
        pkt_clone = {
            'sequence_number': packet['sequence_number'],
            'data': packet['data'],
            'checksum': packet['checksum']
        }
        return pkt_clone

    @staticmethod
    def is_corrupted(reply):
    
        return reply['checksum']!=ord(reply['ack'])
    

    @staticmethod
    def is_expected_seq(reply, exp_seq):
        """ Check if the received reply from receiver has the expected sequence number
        :param reply: a python dictionary represent a reply sent by the receiver
        :param exp_seq: the sender expected sequence number '0' or '1' represented as a character
        :return: True -> if ack in the reply match the   expected sequence number otherwise False
        """
        return reply['ack'] == exp_seq


    @staticmethod
    def make_pkt(seq, data, checksum):
        """ Create an outgoing packet as a python dictionary
        :param seq: a character represent the sequence number of the packet, the one expected by the receiver '0' or '1'
        :param data: a single character the sender want to send to the receiver
        :param checksum: the checksum of the data the sender will send to the receiver
        :return: a python dictionary represent the packet to be sent
        """
        packet = {
            'sequence_number': seq,
            'data': data,
            'checksum': checksum
        }
        return packet

    def rdt_send(self, process_buffer):
        """ Implement the RDT v2.2 for the sender
    :param process_buffer: a list storing the message the sender process wishes to send to the receiver process
    :return: terminate without returning any value
    """
    
        i = 0
        j=0
        while i < len(process_buffer):
            data = process_buffer[i]  
            temp = i  
            checksum = RDTSender.get_checksum(data)
            no_corruption=False
            
            pkt = RDTSender.make_pkt(self.sequence, data, checksum)
           

            while not no_corruption:
                clonepkt = RDTSender.clone_packet(pkt)
                print(f"Sender: expecting sequence number: {self.sequence} and checksum: {ord(self.sequence)}")
                print(f"Sender: sending {pkt}")
                reply = self.net_srv.udt_send(clonepkt)
            
                if not RDTSender.is_corrupted(reply) and RDTSender.is_expected_seq(reply, self.sequence):
                    print(f"Sender: received {reply}")

                    self.sequence = '1' if self.sequence == '0' else '0'
                    no_corruption = True
                    j+=1
                else:
                    
                    print(f"Sender: received {reply}")

                ##print(f'Sender resending {pkt}')
        
            i += 1
        
        print('Sender done')
        return
                
                
            
            

                        