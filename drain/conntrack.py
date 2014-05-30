#!/usr/bin/env python

import os.path
import re
import time
from subprocess import Popen

import interfaces

if not os.path.exists('/proc/net/nf_conntrack'):
    raise ImportError

def established(port):
    count = 0
    ifaces = interfaces.all()

    for conn in open('/proc/net/nf_conntrack'):
        m = re.search('ESTABLISHED src=([0-9\.]+) dst=([0-9\.]+) sport=([0-9]+) dport=([0-9]+)', conn)

        if m:
            saddr, daddr, sport, dport = m.groups()

            if daddr in ifaces and dport == port:
                count += 1

    return count


def monitor(port):
    draining = True

    while draining:
        draining = established(port)
        yield draining
        time.sleep(1) 

# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
