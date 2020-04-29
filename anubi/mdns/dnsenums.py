from enum import IntEnum

class OpCode(IntEnum):
    '''
    DNS packet OpCodes.
    '''
    #: Query
    QUERY = 0
    #: Inverse Query (Obsolete)
    IQUERY = 1
    #: Status
    STATUS = 2
    #: Notify
    NOTIFY = 4
    #: Update
    UPDATE = 5
    #: DNS Stateful Operations
    DSO = 6

class RCode(IntEnum):
    '''
    DNS packet RCODEs.
    '''
    #: No error
    NOERROR = 0
    #: Format error
    FORMERR = 1
    #: Server failure
    SERVFAIL = 2
    #: Non-Existent domain
    NXDOMAIN = 3
    #: Not implemented
    NOTIMP = 4
    #: Query refused
    REFUSED = 5
    #: Name exist when it should not
    YXDOMAIN = 6
    #: RR Set exist when it should not
    YXRRSET = 7
    #: RR Set that should exist does not
    NXRRSET = 8
    #: Server not authoritative for zone/Not authorized
    NOTAUTH = 9
    #: Name not contained in zone
    NOTZONE = 10
    #: DSO-TYPE not implemented
    DSOTYPENI = 11
    #: Bad OPT version
    BADVERS = 16
    #: TSIG signature failure
    BADSIG = 16
    #: Key not recognized
    BADKEY = 17
    #: Signature out of time window
    BADTIME = 18
    #: Bad TKEY mode
    BADMODE = 19
    #: Duplicate key name
    BADNAME = 20
    #: Algorithm not supported
    BADALG = 21
    #: Bad truncation
    BADTRUNC = 22
    #: Bad/Missing server cookie
    BADCOOKIE = 23

class DnsType(IntEnum):
    '''
    DNS record types.
    '''
    #: Host address (IPv4)
    A = 1
    #: Authoritative name server
    NS = 2
    #: Mail destination (Obsolete, use :attr:`MX`)
    MD = 3
    #: Mail forwarder (Obsolete, use :attr:`MX`)
    MF = 4
    #: Canonical name for alias
    CNAME = 5
    #: Mark starts of a zone of authority
    SOA = 6
    #: Mailbox domain name (Experimental)
    MB = 7
    #: Mail group member (Experimental)
    MG = 8
    #: Mail rename domain name (Experimental)
    MR = 9
    #: Null (Experimental)
    NULL = 10
    #: Well known service description
    WKS = 11
    #: Domain name pointer
    PTR = 12
    #: Host information
    HINFO = 13
    #: Mailbox or mail list information
    MINFO = 14
    #: Mail exchange
    MX = 15
    #: Text string
    TXT = 16
    #: Responsible person
    RP = 17
    #: AFS database location
    AFSDB = 18
    #: X.25 PSDN address
    X25 = 19
    #: ISDN address
    ISDN = 20
    #: Route through
    RT = 21
    #: NSAP address (NSAP stype :attr:`A` record)
    NSAP = 22
    #: Domain name pointer, NSAP style
    NSAP_PTR = 23
    #: Security signature
    SIG = 24
    #: Security key
    KEY = 25
    #: X.400 mail mapping information
    PX = 26
    #: Geographical position
    GPOS = 27
    #: Host address (IPv6)
    AAAA = 28
    #: Location information
    LOC = 29
    #: Next domain (Obsolete)
    NXT = 30
    #: Endpoint identifier
    EID = 31
    #: Nimrod locator
    NIMLOC = 32
    #: Server selection
    SRV = 33
    #: ATM address
    ATMA = 34
    #: Naming authority pointer
    NAPTR = 35
    #: Key exchanger
    KX = 36
    #: CERT
    CERT = 37
    #: Host address (IPv6 - Obsolete, use :attr:`AAAA`)
    A6 = 38
    #: DNAME
    DNAME = 39
    #: SINK
    SINK = 40
    #: OPT
    OPT = 41
    #: APL
    APL = 42
    #: Delegation singer
    DS = 43
    #: SSH key fingerprint
    SSHFP = 44
    #: IPSECKEY
    IPSECKEY = 45
    #: RRSIG
    RRSIG = 46
    #: NSEC
    NSEC = 47
    #: DNSKEY
    DNSKEY = 48
    #: DHCID
    DHCID = 49
    #: NSEC3
    NSEC3 = 50
    #: NSEC3PARAM
    NSEC3PARAM = 51
    #: TLSA
    TLSA = 52
    #: S/MIME cer association
    SIMMEA = 53
    #: Host identity protocol
    HIP = 55
    #: NINFO
    NINFO = 56
    #: RKEY
    RKEY = 57
    #: Trust anchor link
    TALINK = 58
    #: Child DS
    CDS = 59
    #: DNSKEY(s) the child wants reflected in DS
    CDNSKEY = 60
    #: OpenPGP key
    OPENPGPKEY = 61
    #: Child-To-Parent syncronization
    CSYNC = 62
    #: Message digest for DNS zone
    ZONEMD = 63
    #: SPF
    SPF = 99
    #: UINFO (IANA reservedd)
    UINFO = 100
    #: UID (IANA reservedd)
    UID = 101
    #: GID (IANA reservedd)
    GID = 102
    #: UNSPEC (IANA reservedd)
    UNSPEC = 103
    #: NID
    NID = 104
    #: L32
    L32 = 105
    #: L64
    L64 = 106
    #: LP
    LP = 107
    #: EUI-48 address
    EUI48 = 108
    #: EUI-64 address
    EUI64 = 109
    #: Transaction key
    TKEY = 249
    #: Transaction signature
    TSIG = 250
    #: Incremental transfer
    IXFR = 251
    #: Transfer of an entire zone
    AXFR = 252
    #: Mailbox related resource record (:attr:`MB`, :attr:`MG` or :attr:`MR`)
    MAILB = 253
    #: Mail agent (Obsolete, see :attr:`MX`)
    MAILA = 254
    #: Any
    ANY = 255
    #: URI
    URI = 256
    #: Certification authority restriction
    CAA = 257
    #: Application visibility and control
    AVC = 258
    #: Digital object architecture
    DOA = 259
    #: Automatic multicast tunnelling relay
    AMTRELAY = 260
    #: DNSSEC trust authorities
    TA = 32769
    #: DNSSEC lookaside validation (Obsolete)
    DLV = 32769
    
    @classmethod
    def contains_value(cls, value):
        '''
        :param value: The value to be tested.
        :type value: int

        Test if the given value correspond to any of the enum values.
        '''
        return value in cls.__members__.values()
    @classmethod
    def is_obsolete(cls, value):
        '''
        :param value: The value to be tested.
        :type value: int

        Test if the given value correspond to a value marked ad obsolete.
        '''
        return value in [
            DnsType.MD, 
            DnsType.MF, 
            DnsType.NXT, 
            DnsType.A6, 
            DnsType.MAILA, 
            DnsType.DLV
            ]

class DnsClass(IntEnum):
    '''
    DNS class types.
    '''
    #: Internet
    IN = 1
    #: CSNET (Obsolete)
    CS = 2
    #: Chaos
    CH = 3
    #: Hesoid
    HS = 4
    #: None
    NONE = 254
    #: Any
    ANY = 255
    
    @classmethod
    def contains_value(cls, value):
        '''
        :param value: The value to be tested.
        :type value: int

        Test if the given value correspond to any of the enum values.
        '''
        return value in cls.__members__.values()