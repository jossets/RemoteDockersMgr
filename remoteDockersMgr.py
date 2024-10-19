#!/usr/bin/env python3

import time
import select
from subprocess import call
import os
import sys
import threading
import ssl 

import json
from urllib.parse import urlparse, parse_qs
import random 
import string


from remoteDockersMgrConfig import *
from remoteDockersMgrHttp import *
from remoteDockersMgrDocker import *
from remoteDockersMgrSsh import *
from remoteDockersMgrBash import *
from remoteDockersMgrWatchdog import *


def main():
    print("== Remote Dockers Manager ==", flush=True)
    print("|")
    print("| Read config file")
    config_load()  
    
    #print(config())  
    if None==config():
        print("Error reading config file")
        exit(1)
    tracecx = config()['debugmode']

    if config()['checkserverlogin']:
        print("| Check server login", flush=True)
        for server in  config()['servers']:
            ret =run_cmd(server, [ 'id' ])
            # to do handle pb
            print(ret)

    if config()['checkservermem']:   
        print("| Check server mem", flush=True)
        for server in  config()['servers']:
            if server['enabled']:
                mem, mem_total, mem_available = remote_get_mem(server)
                server['mem'] = mem
                server['mem_total'] = mem_total
                server['mem_available'] = mem_available
                print(mem+"\n", flush=True)

                dockers = remote_docker_ps_all(server)
                for docker in dockers:
                    print("{0}  {1}   {2}".format(docker['Image'], docker['State'], docker['Status']))
                server['status']='ready'
                print("Status: Ready\n", flush=True)

    
    #
    # VM watchdog 
    if config()['enablewatchdog']:  
        th = threading.Thread(target=VMWatchdogThread) 
        th.daemon = True
        th.start()


    print("|\n| Run HTTP server and serve", flush=True) 
    HTTP_serve_forever(config()['httpserverhost'], config()['httpserverport'])
    exit(0)



if __name__== "__main__":
    main()
    
