#!/usr/bin/env python3

from remoteDockersMgrSsh import *


#
# Server stats
# MemTotal:       10110016 kB
# MemFree:          342696 kB
# MemAvailable:    1925276 kB : dispo pour de nouvelles apps
# ...
# meminfo = dict((i.split()[0].rstrip(':'),int(i.split()[1])) for i in open('/proc/meminfo').readlines())
# mem_kib = meminfo['MemTotal']
#

def remote_get_mem_all(server):
    return run_cmd(server, [
        'cat /proc/meminfo',
    ])


def remote_get_mem(server):
    mem = remote_get_mem_all(server)
    mem = mem.splitlines()
    # MemTotal:        1649648 kB
    mem_total = mem[0][9:-2].strip()
    # MemAvailable:    1400744 kB
    mem_available = mem[2][13:-2].strip()
    return mem[0] + "\n" + mem[2], mem_total, mem_available


def remote_get_df(server):
    return run_cmd(server, [
        'df | grep sd',
    ])
