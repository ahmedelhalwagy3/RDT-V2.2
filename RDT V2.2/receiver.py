class ReceiverProcess:
    """ Represent the receiver process in the application layer  """
    __buffer = list()
    x=5
    @staticmethod
    def deliver_data(data):
        """ deliver data from the transport layer RDT receiver to the application layer
        :param data: a character received by the RDT RDT receiver
        :return: no return value
        """
        ReceiverProcess.__buffer.append(data)
        return

    @staticmethod
    def get_buffer():
        """ To get the message the process received over the network
        :return:  a python list of characters represent the incoming message
        """
        return ReceiverProcess.__buffer


class RDTReceiver:
    """" Implement the Reliable Data Transfer Protocol V2.2 Receiver Side """
    def get_checksum(data):
       return ord(data)
    def __init__(self):
        self.sequence = '0'

    @staticmethod
    @staticmethod
    @staticmethod
    @staticmethod
    def is_corrupted(packet):
        return ord(packet['data'])!=packet['checksum']
        

    
    @staticmethod
    def is_expected_seq(rcv_pkt, exp_seq):
        """ Check if the received reply from receiver has the expected sequence number
         :param rcv_pkt: a python dictionary represent a packet received by the receiver
         :param exp_seq: the receiver expected sequence number '0' or '1' represented as a character
         :return: True -> if ack in the reply match the   expected sequence number otherwise False
        """
        return rcv_pkt['sequence_number'] == (exp_seq)



    @staticmethod
    def make_reply_pkt(seq, checksum):
        """ Create a reply (feedback) packet with to acknowledge the received packet
        :param seq: the sequence number '0' or '1' to be acknowledged
        :param checksum: the checksum of the ack the receiver will send to the sender
        :return:  a python dictionary represent a reply (acknowledgement)  packet
        """
        reply_pck = {
            'ack': seq,
            'checksum': checksum
        }

        return reply_pck
    


    def rdt_rcv(self, rcv_pkt):
        """Implement the RDT v2.2 for the receiver
    :param received_packet: a packet delivered by the network layer 'udt_send()' to the receiver
    :return: the reply packet
    """

        if (not RDTReceiver.is_corrupted(rcv_pkt) )and RDTReceiver.is_expected_seq(rcv_pkt, self.sequence):
            print(f"Receiver expecting sequence number= "+self.sequence)

            reply_pkt = RDTReceiver.make_reply_pkt(self.sequence, RDTReceiver.get_checksum(self.sequence))
            self.sequence = '0' if self.sequence == '1' else '1'
            ReceiverProcess.deliver_data(rcv_pkt['data'])
            print(f'Receiver reply with: {reply_pkt}')
            return reply_pkt
        else:
            print("Network_layer:corruption occured (sequence number: " + str(rcv_pkt['sequence_number'])+ " data: "+ str(rcv_pkt['data'])+" checksum: "+str(rcv_pkt['checksum'])+")")
            print(f"Receiver expecting sequence number= "+self.sequence)

            ackn = '0' if self.sequence=='1' else '1'
            reply_pkt = RDTReceiver.make_reply_pkt(ackn, ord(ackn))
            print(f'Receiver reply with: {reply_pkt}')
            return reply_pkt
        
            

       



        
