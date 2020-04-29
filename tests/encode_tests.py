import unittest
from anubi.mdns import DnsPacket, DnsQRecord, DnsType, DnsClass, DnsRRecordA, DnsRRecordAAAA, DnsRRecordNotImplemented, OpCode, RCode

class EncodeTests(unittest.TestCase):  

    def test_query_1(self):
        #prepare the packet
        q_packet = DnsPacket(True)        
        q_packet.id = 0
        q_packet.AA = True
        q_packet.RD = True
        q_packet.question_records.append(DnsQRecord('test.local.', DnsType.A, DnsClass.IN))
        q_packet.question_records.append(DnsQRecord('_service.test.local.', DnsType.ANY, DnsClass.IN))
        q_packet.question_records.append(DnsQRecord('test._tcp.local.', DnsType.TXT, DnsClass.IN))
        #test encoding
        self.assertEqual(q_packet.encode(), b'\x00\x00\x05\x00\x00\x03\x00\x00\x00\x00\x00\x00\x04test\x05local\x00\x00\x01\x00\x01\x08_service\xc0\x0c\x00\xff\x00\x01\x04test\x04_tcp\xc0\x11\x00\x10\x00\x01')
    def test_query_2(self):
        #prepare the packet
        q_packet = DnsPacket(True)
        q_packet.id = 38784
        q = DnsQRecord('test.local.', DnsType.A, DnsClass.IN)
        q.prefer_unicast = True
        q_packet.question_records.append(q)
        q = DnsQRecord('_service.test.local.', DnsType.ANY, DnsClass.ANY)
        q.prefer_unicast = True
        q_packet.question_records.append(q)
        #test encoding
        self.assertEqual(q_packet.encode(False), b'\x97\x80\x00\x00\x00\x02\x00\x00\x00\x00\x00\x00\x04test\x05local\x00\x00\x01\x80\x01\x08_service\x04test\x05local\x00\x00\xff\x80\xff')
    def test_answer_1(self):
        #prepare the packet
        a_packet = DnsPacket(False)
        a_packet.id = 0
        a_packet.AA = True
        a_packet.TC = True
        a_packet.answer_records.append(DnsRRecordA('test.local.', 120, '127.0.0.1'))
        r = DnsRRecordAAAA('test.local.', 120, '::1')
        r.flush_cache = True
        a_packet.additional_records.append(r)
        #test encoding
        self.assertEqual(a_packet.encode(), b'\x00\x00\x86\x00\x00\x00\x00\x01\x00\x00\x00\x01\x04test\x05local\x00\x00\x01\x00\x01\x00\x00\x00x\x00\x04\x7f\x00\x00\x01\xc0\x0c\x00\x1c\x80\x01\x00\x00\x00x\x00\x10\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01')
    def test_answer_2(self):
        #prepare the packet
        a_packet = DnsPacket(False)
        a_packet.id = 38784
        a_packet.RA = True
        a_packet.OpCode = OpCode.NOTIFY
        a_packet.RCODE = RCode.REFUSED
        a_packet.question_records.append(DnsQRecord('test.local.', DnsType.A, DnsClass.IN))
        a_packet.question_records.append(DnsQRecord('_service.test.local.', DnsType.ANY, DnsClass.ANY))
        a_packet.answer_records.append(DnsRRecordNotImplemented('test._tcp.local.', DnsType.TXT, DnsClass.CS, 120, 8 , b'test1234'))
        a_packet.answer_records.append(DnsRRecordA('test.local.', 60, '127.0.0.2'))
        a_packet.answer_records.append(DnsRRecordA('test.local.', 240, '127.0.0.3'))
        a_packet.authority_records.append(DnsRRecordNotImplemented('test.local.', DnsType.NS, DnsClass.IN, 1000, 18 , b'test1.test2.local.'))
        a_packet.additional_records.append(DnsRRecordAAAA('test.local.', 120, '1::4'))
        a_packet.additional_records.append(DnsRRecordNotImplemented('_service.test.local.', DnsType.SRV, DnsClass.IN, 4500, 18, b'\x00\x00\x00\x00\x00\x15\x09_service1\xc0\x0c'))
        #test encoding
        self.assertEqual(a_packet.encode(), b'\x97\x80\xa0\x85\x00\x02\x00\x03\x00\x01\x00\x02\x04test\x05local\x00\x00\x01\x00\x01\x08_service\xc0\x0c\x00\xff\x00\xff\x04test\x04_tcp\xc0\x11\x00\x10\x00\x02\x00\x00\x00x\x00\x08test1234\xc0\x0c\x00\x01\x00\x01\x00\x00\x00<\x00\x04\x7f\x00\x00\x02\xc0\x0c\x00\x01\x00\x01\x00\x00\x00\xf0\x00\x04\x7f\x00\x00\x03\xc0\x0c\x00\x02\x00\x01\x00\x00\x03\xe8\x00\x12test1.test2.local.\xc0\x0c\x00\x1c\x00\x01\x00\x00\x00x\x00\x10\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x04\xc0\x1c\x00!\x00\x01\x00\x00\x11\x94\x00\x12\x00\x00\x00\x00\x00\x15\t_service1\xc0\x0c')