import unittest
from drtp import pack_header, unpack_header


class TestDRTPProtocol(unittest.TestCase):

    def test_header_packing(self):
        """Test that headers are packed correctly."""
        seq_num = 1
        ack_num = 1
        flags = 0x01  # Example: Assuming 0x01 represents SYN
        packed_data = pack_header(seq_num, ack_num, flags)
        self.assertEqual(packed_data, b'\x00\x01\x00\x01\x00\x01')

    def test_header_unpacking(self):
        """Test that headers are unpacked correctly."""
        packed_data = b'\x00\x01\x00\x01\x00\x01'
        seq_num, ack_num, flags = unpack_header(packed_data)
        self.assertEqual(seq_num, 1)
        self.assertEqual(ack_num, 1)
        self.assertEqual(flags, 0x01)


if __name__ == '__main__':
    unittest.main()
