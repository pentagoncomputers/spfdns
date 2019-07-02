'''
Created on 1 Jul 2019

@author: dermot@pentagoncomputers.com
@copyright: Pentagon Computers Ltd, 2019.
'''

from __future__ import print_function

from IPy import IP

from dnslib import RR, QTYPE, RCODE
from dnslib.dns import parse_time, A
from dnslib.label import DNSLabel
from dnslib.server import BaseResolver
import re
import spf
from textwrap import wrap


def str_to_ip_addr(rev_ip_str):
    '''
    Turn a reversed ip string into an ip address.

    :param ip_str:
    :return IP|False    False on failure.
    '''
    # Both ipv4 and ipv6 addresses should be dot-notation (the rfc says so).  We do a crude match
    # here to check if it's sane.
    if re.match('^(\d{1,3}\.){4}$', rev_ip_str + '.'):
        # ipv4
        # We can split on dots and reverse.
        ip_str = '.'.join(reversed(rev_ip_str.split('.')))
    elif re.match('^([0-9a-f]\.){32}$', rev_ip_str + '.'):
        # ipv6
        no_seps = ''.join(reversed(rev_ip_str.split('.')))
        ip_str = ':'.join(wrap(no_seps, 4)) # sneaky hack to get it in blocks of 4
    else:
        return False

    try:
        return IP(ip_str)
    except TypeError:
        print('{} does not appear to an ip address'.format(ip_str))

    return False



class SPFResolver(BaseResolver):
    def __init__(self, domains, ttl='300s'):
        self.domains = []
        for o in domains:
            self.domains.append(DNSLabel(o.lower()))
        self.ttl = parse_time(ttl)
        self.routes = {}

    def resolve(self,request,handler):  # @UnusedVariable
        reply = request.reply()
        qtype = QTYPE[request.q.qtype]
        qname = request.q.qname
        qname_str = str(qname).lower()

        # qname_str will be <ip_address_dot_notation_reversed>._spf.mta.domain.com
        # for spf macro like exists:${ir}._spf._mta.domain.com

        for o in self.domains:
            dom_lower = str(o).lower()
            if qname_str.endswith(dom_lower):

                # we only respond to 'A' requests.
                if qtype == 'A':

                    # ip_addr_part is expected to be reversed dot-notation (even for ipv6)
                    ip_addr_part = qname_str[:-(1+len(dom_lower))]
                    if ip_addr_part:
                        try:
                            ip = str_to_ip_addr(ip_addr_part)

                            if ip:
                                print(ip)

                                if spf.is_ok(ip, dom_lower):
                                    reply.add_answer(RR(qname, QTYPE.A, ttl=self.ttl, rdata=A('127.0.0.1')))
                                    return reply
                                else:
                                    print('IP {} is not in domain {}'.format(ip_addr_part, dom_lower))
                            else:
                                print('{} not a dotted-decimal ip address'.format(ip_addr_part))
                        except ValueError:
                            print('{} does not appear to an ip address'.format(ip_addr_part))


        reply.header.rcode = RCODE.NXDOMAIN
        return reply
