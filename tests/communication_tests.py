import unittest
from anubi.mdns import mDNS, DnsRRecordA, DnsRRecordAAAA, DnsPacket, DnsQRecord, DnsType, DnsClass
import socket

class CommunicationTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls._mdns = mDNS()
        #replace the class socket with a new one connected to localhost
        cls.__mdns_address = ('127.0.0.1', mDNS._mDNS__MDNS_ADDRESS[1])
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        #set socket options
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        if hasattr(socket, 'SO_REUSEPORT'):
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
        sock.bind(cls.__mdns_address)
        cls._mdns._mDNS__sock.close()
        cls._mdns._mDNS__sock = sock
        cls._mdns._mDNS__reply_sender._DnsReplySender__sock = sock
        cls._mdns.add_record(DnsRRecordA('test.local.', 120, '127.0.0.1'))
        cls._mdns.add_record(DnsRRecordAAAA('test.local.', 120, '::1'))
        cls._mdns.start()
    @classmethod
    def tearDownClass(cls):
        cls._mdns.stop()
        cls._mdns.join()

    def setUp(self):
        self.__sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    def tearDown(self):
        self.__sock.close()

    def test_IPv4_address_query_1(self):
        query = DnsPacket(True)
        question = DnsQRecord('test.local.', DnsType.A, DnsClass.IN)
        #we cannot use multicast on localhost, so force unicast reply
        question.prefer_unicast = True
        query.question_records.append(question)
        self.__sock.sendto(query.encode(), self.__mdns_address)
        data = self.__sock.recv(8192)
        reply = DnsPacket.decode(data)
        self.assertEqual(query.question_records[0], reply.question_records[0])
        #answer record
        self.assertEqual(reply.answer_records[0].name, 'test.local.')
        self.assertEqual(reply.answer_records[0].record_type, DnsType.A)
        self.assertEqual(reply.answer_records[0].record_class, DnsClass.IN)
        self.assertEqual(reply.answer_records[0].ttl, 120)
        self.assertEqual(reply.answer_records[0].address, '127.0.0.1')
        #additional record
        self.assertEqual(reply.additional_records[0].name, 'test.local.')
        self.assertEqual(reply.additional_records[0].record_type, DnsType.AAAA)
        self.assertEqual(reply.additional_records[0].record_class, DnsClass.IN)
        self.assertEqual(reply.additional_records[0].ttl, 120)
        self.assertEqual(reply.additional_records[0].address, '::1')

    def test_IPv4_address_query_2(self):
        query = DnsPacket(True)
        question = DnsQRecord('test.local.', DnsType.ANY, DnsClass.ANY)
        #we cannot use multicast on localhost, so force unicast reply
        question.prefer_unicast = True
        query.question_records.append(question)
        self.__sock.sendto(query.encode(), self.__mdns_address)
        data = self.__sock.recv(8192)
        reply = DnsPacket.decode(data)
        self.assertEqual(query.question_records[0], reply.question_records[0])
        #answer records
        self.assertEqual(len(reply.answer_records), 2)
        self.assertEqual(reply.answer_records[0].name, 'test.local.')
        self.assertEqual(reply.answer_records[0].record_type, DnsType.A)
        self.assertEqual(reply.answer_records[0].record_class, DnsClass.IN)
        self.assertEqual(reply.answer_records[0].ttl, 120)
        self.assertEqual(reply.answer_records[0].address, '127.0.0.1')
        self.assertEqual(reply.answer_records[1].name, 'test.local.')
        self.assertEqual(reply.answer_records[1].record_type, DnsType.AAAA)
        self.assertEqual(reply.answer_records[1].record_class, DnsClass.IN)
        self.assertEqual(reply.answer_records[1].ttl, 120)
        self.assertEqual(reply.answer_records[1].address, '::1')
    
    def test_IPv6_address_query_1(self):
        query = DnsPacket(True)
        question = DnsQRecord('test.local.', DnsType.AAAA, DnsClass.IN)
        #we cannot use multicast on localhost, so force unicast reply
        question.prefer_unicast = True
        query.question_records.append(question)
        self.__sock.sendto(query.encode(), self.__mdns_address)
        data = self.__sock.recv(8192)
        reply = DnsPacket.decode(data)
        self.assertEqual(query.question_records[0], reply.question_records[0])
        #answer record
        self.assertEqual(reply.answer_records[0].name, 'test.local.')
        self.assertEqual(reply.answer_records[0].record_type, DnsType.AAAA)
        self.assertEqual(reply.answer_records[0].record_class, DnsClass.IN)
        self.assertEqual(reply.answer_records[0].ttl, 120)
        self.assertEqual(reply.answer_records[0].address, '::1')
        #additional record
        self.assertEqual(reply.additional_records[0].name, 'test.local.')
        self.assertEqual(reply.additional_records[0].record_type, DnsType.A)
        self.assertEqual(reply.additional_records[0].record_class, DnsClass.IN)
        self.assertEqual(reply.additional_records[0].ttl, 120)
        self.assertEqual(reply.additional_records[0].address, '127.0.0.1')

    def test_IPv6_address_query_2(self):
        query = DnsPacket(True)
        question = DnsQRecord('test.local.', DnsType.ANY, DnsClass.ANY)
        #we cannot use multicast on localhost, so force unicast reply
        question.prefer_unicast = True
        query.question_records.append(question)
        self.__sock.sendto(query.encode(), self.__mdns_address)
        data = self.__sock.recv(8192)
        reply = DnsPacket.decode(data)
        self.assertEqual(query.question_records[0], reply.question_records[0])
        #answer records
        self.assertEqual(len(reply.answer_records), 2)
        self.assertEqual(reply.answer_records[0].name, 'test.local.')
        self.assertEqual(reply.answer_records[0].record_type, DnsType.A)
        self.assertEqual(reply.answer_records[0].record_class, DnsClass.IN)
        self.assertEqual(reply.answer_records[0].ttl, 120)
        self.assertEqual(reply.answer_records[0].address, '127.0.0.1')
        self.assertEqual(reply.answer_records[1].name, 'test.local.')
        self.assertEqual(reply.answer_records[1].record_type, DnsType.AAAA)
        self.assertEqual(reply.answer_records[1].record_class, DnsClass.IN)
        self.assertEqual(reply.answer_records[1].ttl, 120)
        self.assertEqual(reply.answer_records[1].address, '::1')