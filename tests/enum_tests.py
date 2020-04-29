import unittest
from anubi.mdns import DnsClass, DnsType

class EnumTests(unittest.TestCase):

    def test_dns_class_contains(self):
        self.assertTrue(DnsClass.contains_value(DnsClass.IN))
        self.assertFalse(DnsClass.contains_value(0))

    def test_dns_type_contains(self):
        self.assertTrue(DnsType.contains_value(DnsType.A))
        self.assertFalse(DnsType.contains_value(0))

    def test_dns_type_obsolete(self):
        self.assertFalse(DnsType.is_obsolete(DnsType.AAAA))
        self.assertTrue(DnsType.is_obsolete(DnsType.A6))