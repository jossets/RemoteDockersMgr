import time
from datetime import date
from datetime import datetime

from remoteDockersMgrConfig import *
from remoteDockersMgrSsh import *
from remoteDockersMgrDocker import *

# "Labels":"USERID_345642456=,maintainer=NGINX Docker Maintainers \u003cdocker-maint@nginx.com\u003e",
def get_label(labels, label):
    arraylabels = labels.split(',')
    for entry in arraylabels:
        if entry.startswith(label+"="):
            return entry[len(label)+1:]
    return ""

def VMWatchdogAction():
    print("\n[+] Watchdog starting", flush=True)
    print("    Local time: "+ time.strftime('%Y-%m-%d %H:%M:%S'))
    for server in  config()['servers']:
        if server["enabled"]:
            print("    [ Server: "+server['name']+" ]", flush=True)
            dockers = remote_docker_ps_all(server)
            for docker in dockers:
                # "CreatedAt":"2024-10-19 19:36:59 +0200 CEST"
                createdatraw = docker['CreatedAt']
                # "CreatedAt":"2024-10-19 19:36:59",
                createdatraw = createdatraw[0:19]
                #print(createdatraw)
                createdat = time.strptime(createdatraw, "%Y-%m-%d %H:%M:%S")
                #print(createdat)
                now = time.localtime()
                # duration in second
                duration = time.mktime(now) - time.mktime(createdat)
                #print(duration)
                #                 
                if "Labels" in docker:
                    #print(docker['Labels'])
                    leasetimeendraw = get_label(docker['Labels'], "LEASETIMEEND")
                    if ""!=leasetimeendraw:
                        leasetimeend = time.strptime(leasetimeendraw, "%Y-%m-%d %H:%M:%S")
                        #print(leasetimeend)                    
                        if now>leasetimeend:
                            print("    - Destroy instance: "+docker['ID'])
                            remote_docker_kill(server, docker['ID'])
# 

    print("[-] Watchdog ending", flush=True)


def VMWatchdogThread():
    time.sleep(2)
    while True:
        VMWatchdogAction()
        time.sleep(180)

