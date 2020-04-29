Module Contents
==================

The module exports following elements.

Enums
-----

Following enumerations provides all valid values for some DNS packet and record fields.

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

Following classes can be used to manipulate DNS packets and records.

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

``DnsRRecordAAAA``
^^^^^^^^^^^^^^^^^^

.. autoclass:: anubi.mdns.DnsRRecordAAAA
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

Following classes implements utility functionality for the packet.
Most of the time the user do not need to use this classes, they are usefull only for some advanced uses of the module.

``Index``
^^^^^^^^^

.. autoclass:: anubi.mdns.Index
    :members:

Decorators
----------

Following decorators provides easy ways for the user to extend the module functionalities.

``register_subclass``
^^^^^^^^^^^^^^^^^^^^^

.. autofunction:: anubi.mdns.register_subclass

.. toctree::