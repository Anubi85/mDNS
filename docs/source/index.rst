.. anubi.mdns documentation master file, created by
   sphinx-quickstart on Sun Apr 19 15:05:10 2020.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

.. toctree::
    :hidden:
    
    module_contents

Welcome to anubi.mdns's documentation!
======================================

.. image:: https://img.shields.io/pypi/v/anubi.mdns
    :target: https://pypi.org/project/anubi.mdns/
.. image:: https://img.shields.io/pypi/pyversions/anubi.mdns
.. image:: https://img.shields.io/github/license/anubi85/mDNS

This module provides a simple DNS server that respond to muticast queries.

To use it simply :code:`import anubi.mdns` and create a mDNS instance, add records to it and start it.

The server respond only on IPv4 address and support following record types:

    +-------------+--------------+
    | Record Type | Description  |
    +=============+==============+
    | A           | IPv4 address |
    +-------------+--------------+
    | AAAA        | IPv6 address |
    +-------------+--------------+
   