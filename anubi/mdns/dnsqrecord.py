from ._dnsrecord import DnsRecord

class DnsQRecord(DnsRecord):
    #properties
    @property
    def prefer_unicast(self):
        '''
        Flag that indicates if unicast reply are preferred (True) or not (False).
        '''
        return (self._class & 0x8000) != 0
    @prefer_unicast.setter
    def prefer_unicast(self, value):
        if value:
            self._class |= 0x8000
        else:
            self._class &= 0x7FFF
    #methods
    @classmethod
    def decode(cls, data, idx):
        '''
        :param data: Array of bytes that has to be decoded.
        :type data: bytearray
        :param idx: The index from where the record data begins in the `data` array.
        :type idx: :class:`Index`

        Decode the given data starting from the given index into a :class:`DnsQRecord` instance.
        '''
        return DnsQRecord(*super()._decode(data, idx))
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