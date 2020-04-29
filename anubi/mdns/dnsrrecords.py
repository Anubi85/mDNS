from ._utility import Index, read_short, read_int, write_short, write_int
from ._dnsrecord import DnsRecord
from .dnsenums import DnsType, DnsClass
from socket import inet_pton, inet_ntop, AF_INET, AF_INET6

class DnsRRecord(DnsRecord):
    #subclass registry
    __subclass_registry = {}
    def __new__(cls, *args, **kwargs):
        if cls is DnsRRecord:
            raise Exception('Cannot instantiate abstract class {0}'.format(cls.__name__))
        else:
            return super().__new__(cls)
    def __init__(self, name, type_, class_, ttl):
        '''
        :param name: The record domain name.
        :type name: str
        :param type_: The record :class:`DnsType`.
        :type type_: int
        :param class_: The record :class:`DnsClass`.
        :type class_: int
        :param ttl: The record TTL in milliseconds.
        :type ttl: int

        Represent a DNS record and allows to maipulate its properties.
        This class is a base class for specialized record types and connot be instantiated.
        '''
        super().__init__(name, type_, class_)
        self._ttl = ttl
    #properties
    @property
    def ttl(self):
        '''
        The record TTL in milliseconds.
        '''
        return self._ttl
    @ttl.setter
    def ttl(self, value):
        self._ttl = value
    @property
    def flush_cache(self):
        '''
        A flag that indicates if the client that receive this record has to flush its cached copies (True) or not (False).
        '''
        return (self._class & 0x8000) != 0
    @flush_cache.setter
    def flush_cache(self, value):
        if value:
            self._class |= 0x8000
        else:
            self._class &= 0x7FFF
    #methods
    @staticmethod
    def register_subclass(record_type, subclass):
        if issubclass(subclass, DnsRRecord):
            DnsRRecord.__subclass_registry[record_type] = subclass
        else:
            raise RuntimeError('Decorated class must inherit from {0}'.format(DnsRRecord.__name__))
    @staticmethod
    def _get_record_type(data, idx):
        type_ = 0
        while True:
            step = data[idx]
            if step == 0:
                type_ = read_short(data, idx + 1)
                break
            elif step & 0xC0 != 0:
                idx.advance(2)
                type_ = read_short(data, idx)
                break
            else:
                idx.advance(step + 1)
        return type_
    @classmethod
    def decode(cls, data, idx):
        '''
        :param data: Array of bytes that has to be decoded.
        :type data: bytearray
        :param idx: The index from where the record data begins in the `data` array.
        :type idx: :class:`Index`

        Decode the given data starting from the given index into a proper :class:`DnsRRecord` subclass instance.
        '''
        if cls == DnsRRecord:
            type_ = DnsRRecord._get_record_type(data, Index(idx))
            if type_ in DnsRRecord.__subclass_registry:
                instance = DnsRRecord.__subclass_registry[type_].decode(data, idx)
            else:
                instance = DnsRRecordNotImplemented.decode(data, idx)
            return instance
        else:
            name, type_, class_ = super()._decode(data, idx)
            ttl = read_int(data, idx)
            data_size = read_short(data, idx)
            return name, type_, class_, ttl, data_size
    def encode(self, data, name_compression_dictionary):
        '''
        :param data: The `bytearray` to which the instance data will be appended.
        :type data: bytearray
        :param name_compression_dictionary: a dictionary used to perform name compression. Keys are the domain names, values are the indexes in the `data` array where the domain name begin.
        :type name_compression_dictionary: dict[str, int]

        Encode the intance to a `bytearray` compressing domain names according with the given `name_compression_dictionary`.
        The resulting `bytearray` will be attached to the given `data` parameter.
        If `name_compression_dictionary` is `None` no name compression will be applied.
        '''
        super()._encode(data, name_compression_dictionary)
        write_int(self.ttl, data)
    def answer_to(self, question):
        '''
        :param question: The :class:`DnsQRecord` instance for which the current instance has to be tested.
        :type question: :class:`DnsQRecord`
        :return: `True` if the instance answer to the given question, `False` otherwse.
        :rtype: bool

        Check if the record is a reply for the given question. A record answer to a question if all following criterias are satisfied:

        * The record and question domain names are the same.
        * The record and question types are the same OR the question type is :attr:`DnsType.ANY` OR the record type is :attr:`DnsType.CNAME`.
        * The record and question classes are the same OR the question class is :attr:`DnsClass.ANY`.
        '''
        #a record answer to a question only if they have:
        # - the same name
        # - the same type or question type is ANY or resource record type is CNAME
        # - the same class or the question class is ANY
        if not isinstance(question, DnsRecord):
            return False
        else:
            return (self.name == question.name and
                    (self.record_type == question.record_type or
                        question.record_type == DnsType.ANY or
                        self.record_type == DnsType.CNAME) and
                    (self.record_class == question.record_class or question.record_class == DnsClass.ANY))

#decorator for register DnsRRecord subclasses
def register_subclass(record_type):
    '''
    :param record_type: The :class:`DnsType` that the decorated class implements.
    :type record_type: :class:`DnsType`

    This decorator can only be applied to class that derives from :class:`DnsRRecord`.
    If applied to a class that does not satisfy the constrain a :exc:`RuntimeError` exception will be raised.
    Scope of this decorator is to register the class ad secoder for the given `record_type`.
    '''
    def worker(subclass):
        DnsRRecord.register_subclass(record_type, subclass)
        return subclass
    return worker

@register_subclass(DnsType.A)
class DnsRRecordA(DnsRRecord):
    def __init__(self, name, ttl, address):
        '''
        :param name: The record domain name.
        :type name: str
        :param ttl: The record TTL in milliseconds.
        :type ttl: int
        :param address: The record IP address (IPv4).
        :type address: str

        Represent a DNS Record of type A and allows to manipulate its properties.
        '''
        super().__init__(name, DnsType.A.value, DnsClass.IN.value, ttl)
        self._address = address
    #equality operator
    def __eq__(self, other):
        return (isinstance(other, DnsRRecordA) and
                super().__eq__(other) and
                self._address == other.address)
    #properties
    @property
    def address(self):
        '''
        The record IPv4 address.
        '''
        return self._address
    @address.setter
    def address(self, value):
        self._address = value
    #methods
    @classmethod
    def decode(cls, data, idx):
        name, _, class_, ttl, data_size = super().decode(data, idx)
        instance = DnsRRecordA(name, ttl, inet_ntop(AF_INET, data[idx: idx + data_size]))
        #preserve cache flush bit
        instance._class = class_
        idx.advance(data_size)
        return instance
    def encode(self, data, name_compression_dictionary):
        super().encode(data, name_compression_dictionary)
        raw_ip = inet_pton(AF_INET, self._address)
        write_short(len(raw_ip), data)
        data.extend(raw_ip)

@register_subclass(DnsType.AAAA)
class DnsRRecordAAAA(DnsRRecord):
    def __init__(self, name, ttl, address):
        '''
        :param name: The record domain name.
        :type name: str
        :param ttl: The record TTL in milliseconds.
        :type ttl: int
        :param address: The record IP address (IPv6).
        :type address: str

        Represent a DNS Record of type AAAA and allows to manipulate its properties.
        '''
        super().__init__(name, DnsType.AAAA.value, DnsClass.IN.value, ttl)
        self._address = address
    #equality operator
    def __eq__(self, other):
        return (isinstance(other, DnsRRecordAAAA) and
                super().__eq__(other) and
                self._address == other.address)
    #properties
    @property
    def address(self):
        '''
        The record IPv6 address.
        '''
        return self._address
    @address.setter
    def address(self, value):
        self._address = value
    #methods
    @classmethod
    def decode(cls, data, idx):
        name, _, class_, ttl, data_size = super().decode(data, idx)
        instance = DnsRRecordAAAA(name, ttl, inet_ntop(AF_INET6, data[idx: idx + data_size]))
        #preserve cache flush bit
        instance._class = class_
        idx.advance(data_size)
        return instance
    def encode(self, data, name_compression_dictionary):
        super().encode(data, name_compression_dictionary)
        raw_ip = inet_pton(AF_INET6, self._address)
        write_short(len(raw_ip), data)
        data.extend(raw_ip)

class DnsRRecordNotImplemented(DnsRRecord):
    def __init__(self, name, type_, class_, ttl, data_size, data):
        '''
        :param name: The record domain name.
        :type name: str
        :param type_: The record :class:`DnsType`.
        :type type_: int
        :param class_: The record :class:`DnsClass`.
        :type class_: int
        :param ttl: The record TTL in milliseconds.
        :type ttl: int
        :param data_size: The record data size in bytes.
        :type data_size: int
        :param data: The record raw data.
        :type data: bytearray

        Represent a DNS record and allows to maipulate its properties.
        This class is a base class for specialized record types and connot be instantiated.
        '''
        super().__init__(name, type_, class_, ttl)
        self._data_size = data_size
        self._data = data
    #equality operator
    def __eq__(self, other):
        return (isinstance(other, DnsRRecordNotImplemented) and
                super().__eq__(other) and
                self.data_size == other.data_size and
                self.data == other.data)
    #properties
    @property
    def data_size(self):
        '''
        The size of the record data section in bytes.
        '''
        return self._data_size
    @data_size.setter
    def data_size(self, value):
        self._data_size = value
    @property
    def data(self):
        '''
        The record data section (raw bytes representation).
        '''
        return self._data
    @data.setter
    def data(self, value):
        self._data = value        
    @property
    def is_unknown(self):
        '''
        A flag that indicates if the record represented by the instance is of a known :class:`DnsType` and :class:`DnsClass` (True) or not (False).
        '''
        return not (DnsType.contains_value(self.record_type) and DnsClass.contains_value(self.record_class))
    @property
    def is_obsolete(self):
        '''
        A flag that indicates if the record represented by the instance is of an obsolete :class`DnsType` (True) or not (False).
        '''
        return not self.is_unknown() and DnsType.is_obsolete(self.record_type)
    #methods
    @classmethod
    def decode(cls, data, idx):
        name, type_, class_, ttl, data_size = super().decode(data, idx)
        instance = DnsRRecordNotImplemented(name, type_, class_, ttl, data_size, data[idx: idx + data_size])
        idx.advance(data_size)
        return instance
    def encode(self, data, name_compression_dictionary):
        super().encode(data, name_compression_dictionary)
        write_short(self.data_size, data)
        data.extend(self.data)