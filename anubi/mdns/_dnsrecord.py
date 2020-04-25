from ._utility import read_name, write_name, read_short, write_short

class DnsRecord:
    def __new__(cls, *args, **kwargs):
        if cls is DnsRecord:
            raise Exception('Cannot instantiate abstract class {0}'.format(cls.__name__))
        else:
            return super().__new__(cls)
    def __init__(self, name, type_, class_):
        '''
        :param name: The record domain name.
        :type name: str
        :param type_: The record :class:`DnsType`.
        :type type_: int
        :param class_: The record :class:`DnsClass`.
        :type class_: int

        Represent a DNS record and allows to maipulate its properties.
        '''
        self._name = name
        self._type = type_
        self._class = class_
    #properties
    @property
    def name(self):
        '''
        The record domain name.
        '''
        return self._name
    @name.setter
    def name(self, value):
        self._name = value
    @property
    def record_type(self):
        '''
        The record :class:`DnsType`.
        '''
        return self._type
    @record_type.setter
    def record_type(self, value):
        self._type = value & 0xFFFF
    @property
    def record_class(self):
        '''
        The record :class:`DnsClass`.
        '''
        return self._class & 0x7FFF
    @record_class.setter
    def record_class(self, value):
        self._class &= 0x8000
        self._class |= (value & 0x7FFF)
    #equality operator
    def __eq__(self, other):
        if not isinstance(other, DnsRecord):
            return False
        elif (self.name == other.name and 
              self.record_type == other.record_type and 
              self.record_class == other.record_class):
            return True
        else:
            return False
    #methods
    @classmethod
    def _decode(cls, data, idx):
        name = read_name(data, idx)
        type_ = read_short(data, idx)
        class_ = read_short(data, idx)
        return name, type_, class_
    def _encode(self, data, name_compression_dictionary):
        write_name(self.name, data, name_compression_dictionary)
        write_short(self._type, data)
        write_short(self._class, data)
