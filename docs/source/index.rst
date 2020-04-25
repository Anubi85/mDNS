.. anubi.mdns documentation master file, created by
   sphinx-quickstart on Sun Apr 19 15:05:10 2020.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to anubi.mdns's documentation!
======================================

This module provides a simple DNS server that respond to muticast queries.

To use it simply :code:`import anubi.mdns` and create a mDNS instance, add records to it and start it.

The server respond only on IPv4 address and support following record types:

* A: IPv4 address

.. toctree::
   :maxdepth: 2
   :caption: Contents:

Module Contents
==================

The module exports following elements.

Enums
-----

``OpCode``
^^^^^^^^^^

.. autoclass:: anubi.mdns.OpCode
   :members:
   :member-order: bysource

``RCode``
^^^^^^^^^

.. autoclass:: anubi.mdns.RCode
   :members:
   :member-order: bysource

``DnsType``
^^^^^^^^^^^

.. autoclass:: anubi.mdns.DnsType
   :members:
   :undoc-members:
   :member-order: bysource

``DnsClass``
^^^^^^^^^^^^

.. autoclass:: anubi.mdns.DnsClass
   :members:
   :undoc-members:
   :member-order: bysource

   

DNS Classes
-----------

``mDNS``
^^^^^^^^

.. autoclass:: anubi.mdns.mDNS
    :members:
    :exclude-members: run

``DnsPacket``
^^^^^^^^^^^^^

.. autoclass:: anubi.mdns.DnsPacket
    :members:

``DnsQRecord``
^^^^^^^^^^^^^^

.. autoclass:: anubi.mdns.DnsQRecord
    :members:
    :inherited-members:

``DnsRRecord``
^^^^^^^^^^^^^^

.. autoclass:: anubi.mdns.DnsRRecord
    :members:
    :inherited-members:

``DnsRRecordA``
^^^^^^^^^^^^^^^

.. autoclass:: anubi.mdns.DnsRRecordA
    :members:
    :inherited-members:

``DnsRRecordNotImplemented``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. note::
    This class does not actually decode/encode the raw data, just copy those data from/to the given ``bytearray``.
        

.. autoclass:: anubi.mdns.DnsRRecordNotImplemented
    :members:
    :inherited-members:

Utility Classes
---------------

``Index``
^^^^^^^^^

.. autoclass:: anubi.mdns.Index
    :members:

Decorators
----------

``register_subclass``
^^^^^^^^^^^^^^^^^^^^^

.. autofunction:: anubi.mdns.register_subclass
