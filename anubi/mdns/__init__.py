'''
This module provides a simple DNS server that respond to muticast queries.

To use it simply 'import mdns' and create a mDNS instance,
add records to it and start it.

The server respond only on IPv4 address and support following record types:
- A:    IPv4 address
- AAAA: IPv6 address
'''

__version__ = '0.1.0a'
__author__ = 'Andrea Parisotto'

from .mdns import mDNS
from .dnsenums import DnsClass, DnsType, OpCode, RCode
from .dnsqrecord import DnsQRecord
from .dnsrrecords import DnsRRecord, DnsRRecordA, DnsRRecordAAAA, DnsRRecordNotImplemented, register_subclass
from .dnspacket import DnsPacket
from ._utility import Index
import logging

logging.getLogger(__name__).addHandler(logging.NullHandler())