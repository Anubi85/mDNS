import unittest
from anubi.mdns import DnsPacket, DnsType, DnsClass, OpCode, RCode

class DecodeTests(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        #decode known packets
        cls._q_packet_1 = DnsPacket.decode(b'\x00\x00\x05\x00\x00\x03\x00\x00\x00\x00\x00\x00\x04test\x05local\x00\x00\x01\x00\x01\x08_service\xc0\x0c\x00\xff\x00\x01\x04test\x04_tcp\xc0\x11\x00\x10\x00\x01')
        cls._q_packet_2 = DnsPacket.decode(b'\x97\x80\x00\x00\x00\x02\x00\x00\x00\x00\x00\x00\x04test\x05local\x00\x00\x01\x80\x01\x08_service\x04test\x05local\x00\x00\xff\x80\xff')
        cls._a_packet_1 = DnsPacket.decode(b'\x00\x00\x86\x00\x00\x00\x00\x01\x00\x00\x00\x01\x04test\x05local\x00\x00\x01\x00\x01\x00\x00\x00x\x00\x04\x7f\x00\x00\x01\xc0\x0c\x00\x1c\x80\x01\x00\x00\x00x\x00\x10\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01')
        cls._a_packet_2 = DnsPacket.decode(b'\x97\x80\xa0\x85\x00\x02\x00\x03\x00\x01\x00\x02\x04test\x05local\x00\x00\x01\x00\x01\x08_service\xc0\x0c\x00\xff\x00\xff\x04test\x04_tcp\xc0\x11\x00\x10\x00\x02\x00\x00\x00x\x00\x08test1234\xc0\x0c\x00\x01\x00\x01\x00\x00\x00<\x00\x04\x7f\x00\x00\x02\xc0\x0c\x00\x01\x00\x01\x00\x00\x00\xf0\x00\x04\x7f\x00\x00\x03\xc0\x0c\x00\x02\x00\x01\x00\x00\x03\xe8\x00\x12test1.test2.local.\xc0\x0c\x00\x1c\x00\x01\x00\x00\x00x\x00\x10\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x04\xc0\x1c\x00!\x00\x01\x00\x00\x11\x94\x00\x12\x00\x00\x00\x00\x00\x15\t_service1\xc0\x0c')

    def test_id(self):
        self.assertEqual(DecodeTests._q_packet_1.id, 0)
        self.assertEqual(DecodeTests._q_packet_2.id, 38784)
        self.assertEqual(DecodeTests._a_packet_1.id, 0)
        self.assertEqual(DecodeTests._a_packet_2.id, 38784)
    def test_query_bit(self):
        self.assertTrue(DecodeTests._q_packet_1.QR)
        self.assertTrue(DecodeTests._q_packet_2.QR)
        self.assertFalse(DecodeTests._a_packet_1.QR)
        self.assertFalse(DecodeTests._a_packet_2.QR)
    def test_op_code(self):
        self.assertEqual(DecodeTests._q_packet_1.OpCode, 0)
        self.assertEqual(DecodeTests._q_packet_2.OpCode, 0)
        self.assertEqual(DecodeTests._a_packet_1.OpCode, 0)
        self.assertEqual(DecodeTests._a_packet_2.OpCode, OpCode.NOTIFY)
    def test_authoritative_answer_bit(self):
        self.assertTrue(DecodeTests._q_packet_1.AA)
        self.assertFalse(DecodeTests._q_packet_2.AA)
        self.assertTrue(DecodeTests._a_packet_1.AA)
        self.assertFalse(DecodeTests._a_packet_2.AA)
    def test_truncated_bit(self):
        self.assertFalse(DecodeTests._q_packet_1.TC)
        self.assertFalse(DecodeTests._q_packet_2.TC)
        self.assertTrue(DecodeTests._a_packet_1.TC)
        self.assertFalse(DecodeTests._a_packet_2.TC)
    def test_recursion_desired_bit(self):
        self.assertTrue(DecodeTests._q_packet_1.RD)
        self.assertFalse(DecodeTests._q_packet_2.RD)
        self.assertFalse(DecodeTests._a_packet_1.RD)
        self.assertFalse(DecodeTests._a_packet_2.RD)
    def test_recursion_avaialble_bit(self):
        self.assertFalse(DecodeTests._q_packet_1.RA)
        self.assertFalse(DecodeTests._q_packet_2.RA)
        self.assertFalse(DecodeTests._a_packet_1.RA)
        self.assertTrue(DecodeTests._a_packet_2.RA)
    def test_authenticated_data_bit(self):
        self.assertFalse(DecodeTests._q_packet_1.AD)
        self.assertFalse(DecodeTests._q_packet_2.AD)
        self.assertFalse(DecodeTests._a_packet_1.AD)
        self.assertFalse(DecodeTests._a_packet_2.AD)
    def test_checking_disabled_bit(self):
        self.assertFalse(DecodeTests._q_packet_1.CD)
        self.assertFalse(DecodeTests._q_packet_1.CD)
        self.assertFalse(DecodeTests._a_packet_1.CD)
        self.assertFalse(DecodeTests._a_packet_2.CD)
    def test_rcode(self):
        self.assertEqual(DecodeTests._q_packet_1.RCODE, 0)
        self.assertEqual(DecodeTests._q_packet_2.RCODE, 0)
        self.assertEqual(DecodeTests._a_packet_1.RCODE, 0)
        self.assertEqual(DecodeTests._a_packet_2.RCODE, RCode.REFUSED)
    def test_question_records_count(self):
        self.assertEqual(len(DecodeTests._q_packet_1.question_records), 3)
        self.assertEqual(len(DecodeTests._q_packet_2.question_records), 2)
        self.assertEqual(len(DecodeTests._a_packet_1.question_records), 0)
        self.assertEqual(len(DecodeTests._a_packet_2.question_records), 2)
    def test_answer_records_count(self):
        self.assertEqual(len(DecodeTests._q_packet_1.answer_records), 0)
        self.assertEqual(len(DecodeTests._q_packet_2.answer_records), 0)
        self.assertEqual(len(DecodeTests._a_packet_1.answer_records), 1)
        self.assertEqual(len(DecodeTests._a_packet_2.answer_records), 3)
    def test_authority_records_count(self):
        self.assertEqual(len(DecodeTests._q_packet_1.authority_records), 0)
        self.assertEqual(len(DecodeTests._q_packet_2.authority_records), 0)
        self.assertEqual(len(DecodeTests._a_packet_1.authority_records), 0)
        self.assertEqual(len(DecodeTests._a_packet_2.authority_records), 1)
    def test_additional_records_count(self):
        self.assertEqual(len(DecodeTests._q_packet_1.additional_records), 0)
        self.assertEqual(len(DecodeTests._q_packet_2.additional_records), 0)
        self.assertEqual(len(DecodeTests._a_packet_1.additional_records), 1)
        self.assertEqual(len(DecodeTests._a_packet_2.additional_records), 2)
    def test_resource_record_A(self):
        self.assertEqual(sum(1 for r in DecodeTests._a_packet_1.answer_records if r.record_type == DnsType.A), 1)
        self.assertEqual(DecodeTests._a_packet_1.answer_records[0].record_type, DnsType.A)
        self.assertEqual(DecodeTests._a_packet_1.answer_records[0].record_class, DnsClass.IN)
        self.assertEqual(DecodeTests._a_packet_1.answer_records[0].ttl, 120)
        self.assertEqual(DecodeTests._a_packet_1.answer_records[0].address, '127.0.0.1')
        self.assertEqual(sum(1 for r in DecodeTests._a_packet_2.answer_records if r.record_type == DnsType.A), 2)
        self.assertEqual(DecodeTests._a_packet_2.answer_records[1].record_type, DnsType.A)
        self.assertEqual(DecodeTests._a_packet_2.answer_records[1].record_class, DnsClass.IN)
        self.assertEqual(DecodeTests._a_packet_2.answer_records[1].ttl, 60)
        self.assertEqual(DecodeTests._a_packet_2.answer_records[1].address, '127.0.0.2')
        self.assertEqual(DecodeTests._a_packet_2.answer_records[2].record_type, DnsType.A)
        self.assertEqual(DecodeTests._a_packet_2.answer_records[2].record_class, DnsClass.IN)
        self.assertEqual(DecodeTests._a_packet_2.answer_records[2].ttl, 240)
        self.assertEqual(DecodeTests._a_packet_2.answer_records[2].address, '127.0.0.3')
    def test_resource_record_AAAA(self):
        self.assertEqual(sum(1 for r in DecodeTests._a_packet_1.additional_records if r.record_type == DnsType.AAAA), 1)
        self.assertEqual(DecodeTests._a_packet_1.additional_records[0].record_type, DnsType.AAAA)
        self.assertEqual(DecodeTests._a_packet_1.additional_records[0].record_class, DnsClass.IN)
        self.assertEqual(DecodeTests._a_packet_1.additional_records[0].ttl, 120)
        self.assertEqual(DecodeTests._a_packet_1.additional_records[0].address, '::1')
        self.assertEqual(sum(1 for r in DecodeTests._a_packet_2.additional_records if r.record_type == DnsType.AAAA), 1)
        self.assertEqual(DecodeTests._a_packet_2.additional_records[0].record_type, DnsType.AAAA)
        self.assertEqual(DecodeTests._a_packet_2.additional_records[0].record_class, DnsClass.IN)
        self.assertEqual(DecodeTests._a_packet_2.additional_records[0].ttl, 120)
        self.assertEqual(DecodeTests._a_packet_2.additional_records[0].address, '1::4')
    def test_record_names(self):
        self.assertEqual(DecodeTests._q_packet_1.question_records[0].name, 'test.local.')
        self.assertEqual(DecodeTests._q_packet_1.question_records[1].name, '_service.test.local.')
        self.assertEqual(DecodeTests._q_packet_1.question_records[2].name, 'test._tcp.local.')
        self.assertEqual(DecodeTests._q_packet_2.question_records[0].name, 'test.local.')
        self.assertEqual(DecodeTests._q_packet_2.question_records[1].name, '_service.test.local.')
        self.assertEqual(DecodeTests._a_packet_1.answer_records[0].name, 'test.local.')
        self.assertEqual(DecodeTests._a_packet_1.additional_records[0].name, 'test.local.')
        self.assertEqual(DecodeTests._a_packet_2.question_records[0].name, 'test.local.')
        self.assertEqual(DecodeTests._a_packet_2.question_records[1].name, '_service.test.local.')
        self.assertEqual(DecodeTests._a_packet_2.answer_records[0].name, 'test._tcp.local.')
        self.assertEqual(DecodeTests._a_packet_2.answer_records[1].name, 'test.local.')
        self.assertEqual(DecodeTests._a_packet_2.answer_records[2].name, 'test.local.')
        self.assertEqual(DecodeTests._a_packet_2.authority_records[0].name, 'test.local.')
        self.assertEqual(DecodeTests._a_packet_2.additional_records[0].name, 'test.local.')
        self.assertEqual(DecodeTests._a_packet_2.additional_records[1].name, '_service.test.local.')
    def test_record_types(self):
        self.assertEqual(DecodeTests._q_packet_1.question_records[0].record_type, DnsType.A)
        self.assertEqual(DecodeTests._q_packet_1.question_records[1].record_type, DnsType.ANY)
        self.assertEqual(DecodeTests._q_packet_1.question_records[2].record_type, DnsType.TXT)
        self.assertEqual(DecodeTests._q_packet_2.question_records[0].record_type, DnsType.A)
        self.assertEqual(DecodeTests._q_packet_2.question_records[1].record_type, DnsType.ANY)
        self.assertEqual(DecodeTests._a_packet_1.answer_records[0].record_type, DnsType.A)
        self.assertEqual(DecodeTests._a_packet_1.additional_records[0].record_type, DnsType.AAAA)
        self.assertEqual(DecodeTests._a_packet_2.question_records[0].record_type, DnsType.A)
        self.assertEqual(DecodeTests._a_packet_2.question_records[1].record_type, DnsType.ANY)
        self.assertEqual(DecodeTests._a_packet_2.answer_records[0].record_type, DnsType.TXT)
        self.assertEqual(DecodeTests._a_packet_2.answer_records[1].record_type, DnsType.A)
        self.assertEqual(DecodeTests._a_packet_2.answer_records[2].record_type, DnsType.A)
        self.assertEqual(DecodeTests._a_packet_2.authority_records[0].record_type, DnsType.NS)
        self.assertEqual(DecodeTests._a_packet_2.additional_records[0].record_type, DnsType.AAAA)
        self.assertEqual(DecodeTests._a_packet_2.additional_records[1].record_type, DnsType.SRV)
    def test_record_classes(self):
        self.assertEqual(DecodeTests._q_packet_1.question_records[0].record_class, DnsClass.IN)
        self.assertEqual(DecodeTests._q_packet_1.question_records[1].record_class, DnsClass.IN)
        self.assertEqual(DecodeTests._q_packet_1.question_records[2].record_class, DnsClass.IN)
        self.assertEqual(DecodeTests._q_packet_2.question_records[0].record_class, DnsClass.IN)
        self.assertEqual(DecodeTests._q_packet_2.question_records[1].record_class, DnsClass.ANY)
        self.assertEqual(DecodeTests._a_packet_1.answer_records[0].record_class, DnsClass.IN)
        self.assertEqual(DecodeTests._a_packet_1.additional_records[0].record_class, DnsClass.IN)
        self.assertEqual(DecodeTests._a_packet_2.question_records[0].record_class, DnsClass.IN)
        self.assertEqual(DecodeTests._a_packet_2.question_records[1].record_class, DnsClass.ANY)
        self.assertEqual(DecodeTests._a_packet_2.answer_records[0].record_class, DnsClass.CS)
        self.assertEqual(DecodeTests._a_packet_2.answer_records[1].record_class, DnsClass.IN)
        self.assertEqual(DecodeTests._a_packet_2.answer_records[2].record_class, DnsClass.IN)
        self.assertEqual(DecodeTests._a_packet_2.authority_records[0].record_class, DnsClass.IN)
        self.assertEqual(DecodeTests._a_packet_2.additional_records[0].record_class, DnsClass.IN)
        self.assertEqual(DecodeTests._a_packet_2.additional_records[1].record_class, DnsClass.IN)
    def test_prefer_unicast_bit(self):
        self.assertFalse(any(map(lambda r: r.prefer_unicast, DecodeTests._q_packet_1.question_records)))
        self.assertTrue(all(map(lambda r: r.prefer_unicast, DecodeTests._q_packet_2.question_records)))
        self.assertFalse(any(map(lambda r: r.prefer_unicast, DecodeTests._a_packet_2.question_records)))
    def test_flush_cache_bit(self):
        self.assertFalse(DecodeTests._a_packet_1.answer_records[0].flush_cache)
        self.assertTrue(DecodeTests._a_packet_1.additional_records[0].flush_cache)
        self.assertFalse(any(map(lambda r: r.flush_cache ,DecodeTests._a_packet_2.answer_records)))
        self.assertFalse(any(map(lambda r: r.flush_cache ,DecodeTests._a_packet_2.authority_records)))
        self.assertFalse(any(map(lambda r: r.flush_cache ,DecodeTests._a_packet_2.additional_records)))