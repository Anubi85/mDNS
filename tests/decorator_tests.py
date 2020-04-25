import unittest
from anubi.mdns import DnsRRecord, register_subclass, DnsType

class DecoratorTests(unittest.TestCase):

    def tearDown(self):
        if DnsType.TXT in DnsRRecord._DnsRRecord__subclass_registry:
            del DnsRRecord._DnsRRecord__subclass_registry[DnsType.TXT]
    def test_register_subclass_decorator_success(self):
        try:
            @register_subclass(DnsType.TXT)
            class TestClass(DnsRRecord):
                pass
        except RuntimeError as ex:
            if str(ex) == 'Decorated class must inherit from {0}'.format(DnsRRecord.__name__):
                self.fail() 
        self.assertTrue(DnsType.TXT in DnsRRecord._DnsRRecord__subclass_registry)
        self.assertEqual(DnsRRecord._DnsRRecord__subclass_registry[DnsType.TXT], TestClass)
    def test_register_subclass_decorator_failure(self):
        with self.assertRaises(RuntimeError) as context:
            @register_subclass(DnsType.TXT)
            class TestClass:
                pass
        self.assertEqual(str(context.exception), 'Decorated class must inherit from {0}'.format(DnsRRecord.__name__))
        self.assertFalse(DnsType.TXT in DnsRRecord._DnsRRecord__subclass_registry)
        with self.assertRaises(KeyError):
            _ = DnsRRecord._DnsRRecord__subclass_registry[DnsType.TXT]