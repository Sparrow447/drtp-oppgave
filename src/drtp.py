import struct

# Packet header packing and unpacking utilities
def pack_header(seq_num, ack_num, flags):
    """Pack data into a DRTP header using struct.
    Args:
        seq_num (int): Sequence number of the packet.
        ack_num (int): Acknowledgment number of the packet.
        flags (int): Flags indicating packet type (SYN, ACK, FIN).
    Returns:
        bytes: Packed header.
    """
    return struct.pack('!HHH', seq_num, ack_num, flags)

def unpack_header(packet):
    """Unpack data from a DRTP header.
    Args:
        packet (bytes): The received packet.
    Returns:
        tuple: Sequence number, Acknowledgment number, Flags.
    """
    return struct.unpack('!HHH', packet[:6])
