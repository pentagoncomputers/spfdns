'''
Created on 1 Jul 2019

@author: dermot@pentagoncomputers.com
@copyright: Pentagon Computers Ltd, 2019.
'''
import argparse
import time

from dnslib.server import DNSLogger, DNSHandler, DNSServer
import spf
from spfresolver import SPFResolver


def run_server():

    p = argparse.ArgumentParser(description="SPF DNS Resolver")
    p.add_argument("--port","-p",type=int,default=53,
                        metavar="<port>",
                        help="Server port (default:53)")
    p.add_argument("--address","-a",default="",
                        metavar="<address>",
                        help="Listen address (default:all)")
    p.add_argument("--udplen","-u",type=int,default=0,
                    metavar="<udplen>",
                    help="Max UDP packet length (default:0)")
    p.add_argument("--tcp",action='store_true',default=False,
                        help="TCP server (default: UDP only)")
    p.add_argument("--log",default="request,reply,truncated,error",
                    help="Log hooks to enable (default: +request,+reply,+truncated,+error,-recv,-send,-data)")
    p.add_argument("--log-prefix",action='store_true',default=False,
                    help="Log prefix (timestamp/handler/resolver) (default: False)")
    args = p.parse_args()

    domains = spf.get_domains()

    resolver = SPFResolver(domains)
    logger = DNSLogger(args.log,args.log_prefix)

    print("Starting SPF Resolver ({}:{}) [{}] on domains: {}".format(
                        args.address or "*",
                        args.port,
                        "UDP/TCP" if args.tcp else "UDP",
                        domains))

    if args.udplen:
        DNSHandler.udplen = args.udplen

    udp_server = DNSServer(resolver,
                           port=args.port,
                           address=args.address,
                           logger=logger)
    udp_server.start_thread()

    if args.tcp:
        tcp_server = DNSServer(resolver,
                               port=args.port,
                               address=args.address,
                               tcp=True,
                               logger=logger)
        tcp_server.start_thread()

    while udp_server.isAlive():
        time.sleep(1)


if __name__ == '__main__':
    run_server()