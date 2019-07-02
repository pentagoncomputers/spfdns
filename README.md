
SPF DNS Resolver
----------------

Resolver for SPF exists queries, e.g. exists:%{ir}.spf.yourdomain.com.
POC only.

Requires:
 * [dnslib](https://bitbucket.org/paulc/dnslib/),
 * [IPy](https://github.com/autocracy/python-ipy),
 * [mysql-connector](https://pypi.org/project/mysql-connector-python/),
 * [six](https://pypi.org/project/six/)

Tested on Python3.6, but probably runs ok on any python 3.

Copyright [Pentagon Computers Ltd](https://www.pentagoncomputers.com), 2019.