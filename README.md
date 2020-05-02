# anubi.mdns

[![PyPI](https://img.shields.io/pypi/v/anubi.mdns)](https://pypi.org/project/anubi.mdns/)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/anubi.mdns)
![GitHub](https://img.shields.io/github/license/anubi85/mDNS)
[![Documentation Status](https://readthedocs.org/projects/anubimdns/badge/?version=latest)](https://anubimdns.readthedocs.io/en/latest/?badge=latest)

This module is a pure python implementation of a mDNS responder. It provides DNS functionalities into a small network that uses the mDNS protocol.

## Python compatibility
The module is compatible with:
* Python 3.7
* Python 3.8

It may be compatible also with previous versions of python but it has never been tested. If you test it with a python version not listed above please notify me so I can update the documentation.

## Versioning
The version number follow the following pattern: MAJOR.MINOR.PATCH.TAG.
* MAJOR version increment on backword incompatible changes
* MINOR version increment on addition of new features
* PATCH version incement on bug fixing and minor changes
* TAG indicates project state (currently alpha)


## Status
The project is currently in its alpha state. It used only by me in a small home environement.
Right now the mDNS responder listen only on IPv4 mDNS addrress and support only type A resource records.

## How to use anubi.mdns
Here 's an example of starting a mDNS responder that resolve some host names.
```python
import signal
import anubi.mdns as mdns

# Create the responder instance
responder = mdns.mDNS()

# Create a SIGINT handler
def sigint_handler(sig_num, stack):
    #just to be sure
    if sig_num == signal.SIGINT:
        #stop the responder on SIGINT signal
        responder.stop()
        print('mDSN responder stopped')

# Register the signal handler
signal.signal(signal.SIGINT, sigint_handler)
# Create records for DNS
responder.add_record(DnsRRecordA('test.local.', 120, '127.0.0.1'))
# Start the responder
responder.start()
# Instruct the user how to stop the application
print('mDSN responder started.\nPress CTRL + C to stop it.')
#  Wait untill the responder terminates
responder.join()
```

## Changelog
### 0.1.0a
- Complete support for AAAA DNS records.
- Add support for additional records.
  Now the additional records section contains AAAA records (if any) for A query and A records (if any) for AAAA query.
### 0.0.4a
- Add support for AAAA DNS records.
### 0.0.3a
- Update python requirements for pypi.
### 0.0.2a
- Update project description and supported python versions for pypi.
### 0.0.1a
- First release.

## License
MIT, see [here](https://github.com/Anubi85/mDNS/blob/master/LICENSE.md) for details.

