
from ._utility import Index, read_short, write_short
from .dnsqrecord import DnsQRecord
from .dnsrrecords import DnsRRecord, DnsRRecordNotImplemented, DnsRRecordA
from .dnsenums import DnsType, DnsClass
import logging

logger = logging.getLogger(__name__)

class DnsPacket:
    __QR_MASK = 0x8000
    __OPCODE_MASK = 0x7800
    __AA_MASK = 0x0400
    __TC_MASK = 0x0200
    __RD_MASK = 0x0100
    __RA_MASK = 0x0080
    __Z_MASK = 0x0040
    __AD_MASK = 0x0020
    __CD_MASK = 0x0010
    __RCODE_MASK = 0x000F
    def __init__(self, is_query):
        '''
        :param is_query: A flag that specify if the packes is a query packet or not.
        :type is_query: bool

        Represent a DNS packet and exposes API to control packet content.
        '''
        self._id = 0
        self.__flags = 0
        self.QR = is_query
        self._question_records = []
        self._answer_records = []
        self._authority_records = []
        self._additional_records = []
    #methods
    @classmethod
    def decode(cls, data):
        '''
        :param data: Array of bytes that has to be decoded.
        :type data: bytearray
        :return: A new instance of :class:`DnsPacket` built from given data.

        Decodes the given data into a :class:`DnsPacket` instance.
        '''
        instance = cls(False)
        idx = Index()
        instance._id = read_short(data, idx)
        instance.__flags = read_short(data, idx)
        #zero flag is ignored and must be alwais be zero
        instance.__flags &= ~cls.__Z_MASK
        question_count = read_short(data, idx)
        answer_count = read_short(data, idx)
        authority_count = read_short(data, idx)
        additional_conunt = read_short(data, idx)
        for i in range(question_count):
            try:
                instance.question_records.append(DnsQRecord.decode(data, idx))
            except Exception as ex:
                logger.warning('Fail to decode question record %d with error %s', i, str(ex))
        for i in range(answer_count):
            try:
                instance.answer_records.append(DnsRRecord.decode(data, idx))
            except Exception as ex:
                logger.warning('Fail to decode answer record %d with error %s', i, str(ex))
        for i in range(authority_count):
            try:
                instance.authority_records.append(DnsRRecord.decode(data, idx))
            except Exception as ex:
                logger.warning('Fail to decode authority record %d with error %s', i, str(ex))
        for i in range(additional_conunt):
            try:
                instance.additional_records.append(DnsRRecord.decode(data, idx))
            except Exception as ex:
                logger.warning('Fail to decode additional record %d with error %s', i, str(ex))
        return instance
    def encode(self, compress_names=True):
        '''
        :param compress_names: A flag that indicates if the domain names in the packed has to be compressed or not. Default to True
        :type compress_names: bool
        :return: A `bytearray` that represent the :class:`DnsPacket` instance.

        Encode the intance to a `bytearray` compressing domain names according with the given flag.
        '''
        raw_data = bytearray()
        if compress_names:
            name_compression_dictionary = {}
        else:
            name_compression_dictionary = None
        write_short(self._id, raw_data)
        write_short(self.__flags, raw_data)
        write_short(len(self.question_records), raw_data)
        write_short(len(self.answer_records), raw_data)
        write_short(len(self.authority_records), raw_data)
        write_short(len(self.additional_records), raw_data)
        for question_record in self.question_records:
            try:
                question_record.encode(raw_data, name_compression_dictionary)
            except Exception as ex:
                logger.warning('Fail to encode question record %s with error %s', question_record, str(ex))
        for answer_record in self.answer_records:
            try:
                answer_record.encode(raw_data, name_compression_dictionary)
            except Exception as ex:
                logger.warning('Fail to encode answer record %s with error %s', answer_record, str(ex))
        for authority_record in self.authority_records:
            try:
                authority_record.encode(raw_data, name_compression_dictionary)
            except Exception as ex:
                logger.warning('Fail to encode authority record %s with error %s', authority_record, str(ex))
        for additional_record in self.additional_records:
            try:
                additional_record.encode(raw_data, name_compression_dictionary)
            except Exception as ex:
                logger.warning('Fail to encode additional record %s with error %s', additional_record, str(ex))
        return bytes(raw_data)
    #utility methods
    def __get_flags_bit(self, bitmask):
        return self.__flags & bitmask != 0
    def __set_flags_bit(self, bitmask, value):
        if value:
            self.__flags |= bitmask
        else:
            self.__flags &= ~bitmask
    #properties
    @property
    def id(self):
        '''
        The query identifier of the packet.
        '''
        return self._id
    @id.setter
    def id(self, value):
        self._id = value
    @property
    def QR(self):
        '''
        Flag that indicates if the packet represent a query (True) or not (False).
        '''
        return not self.__get_flags_bit(self.__QR_MASK)
    @QR.setter
    def QR(self, value):
        self.__set_flags_bit(self.__QR_MASK, not value)
    @property
    def OpCode(self):
        '''
        The packet :class:`OpCode`.
        '''
        return ((self.__flags & self.__OPCODE_MASK) >> 11) & 0x0F
    @OpCode.setter
    def OpCode(self, value):
        self.__flags &= ~self.__OPCODE_MASK
        op_code = ((value.value) & 0x0F) << 11
        self.__flags |= op_code
    @property
    def AA(self):
        '''
        Flags that indicates if the packet is an authoritative answer (True) or not (False).
        '''
        return self.__get_flags_bit(self.__AA_MASK )
    @AA.setter
    def AA(self, value):
        self.__set_flags_bit(self.__AA_MASK, value)
    @property
    def TC(self):
        '''
        Flags that indicates if the packet is truncated (True) or not (False).
        '''
        return self.__get_flags_bit(self.__TC_MASK)
    @TC.setter
    def TC(self, value):
        self.__set_flags_bit(self.__TC_MASK, value)
    @property
    def RD(self):
        '''
        Flags that indicates if the name resolution recursion for the query is desired (True) or not (False).
        '''
        return self.__get_flags_bit(self.__RD_MASK)
    @RD.setter
    def RD(self, value):
        self.__set_flags_bit(self.__RD_MASK, value)
    @property
    def RA(self):
        '''
        Flags that indicates if the name resolution recursion is available (True) or not (False) on the server that send the reply.
        '''
        return self.__get_flags_bit(self.__RA_MASK)
    @RA.setter
    def RA(self, value):
        self.__set_flags_bit(self.__RA_MASK, value)
    @property
    def AD(self):
        '''
        Flags that indicates if the data in answer and authority sections has been authenticated (True) or not (False).
        '''
        return self.__get_flags_bit(self.__AD_MASK)
    @AD.setter
    def AD(self, value):
        self.__set_flags_bit(self.__AD_MASK, value)
    @property
    def CD(self):
        '''
        Flags that indicates if server that reply to the quesry has to authenticate the data in answer and authority sections (True) or not (False).
        '''
        return self.__get_flags_bit(self.__CD_MASK)
    @CD.setter
    def CD(self, value):
        self.__set_flags_bit(self.__CD_MASK, value)
    @property
    def RCODE(self):
        '''
        The packet :class:`RCode` (response code).
        '''
        return self.__flags & self.__RCODE_MASK
    @RCODE.setter
    def RCODE(self, value):
        self.__flags &= ~self.__RCODE_MASK
        self.__flags |= (value.value & 0x0F)
    @property
    def question_records(self):
        '''
        The list of question records in the packet.
        '''
        return self._question_records
    @property
    def answer_records(self):
        '''
        The list of answer records in the packet.
        '''
        return self._answer_records
    @property
    def authority_records(self):
        '''
        The list of authority records in the packet.
        '''
        return self._authority_records
    @property
    def additional_records(self):
        '''
        The list of additional records in the packet.
        '''
        return self._additional_records