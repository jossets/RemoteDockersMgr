#
# Ssh command

import paramiko
from scp import SCPClient
import sys
import time
import threading 
from remoteDockersMgrConfig import *

tracecx=0

def connect_server(server):
    if (tracecx): print("Connecting...%s " % server['name'], flush=True)
    i = 0
    retry_time = 2
    while True:
        try:
            if (tracecx): print("Trying to connect to %s:%s (%i/%i)" % (server['host'], server['port'], i, retry_time))
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            if (server['password']):
                if (tracecx): print("Using password XXXX.", flush=True)    
                ssh.connect(server['host'], port=server['port'], username=server['user'], password=server['password'])
            elif (server['privatekeyfile']):
                if (tracecx): print("Using private key file: %s" % server['privatekeyfile'], flush=True)  
                k = paramiko.RSAKey.from_private_key_file(server['privatekeyfile'] )
                #k = paramiko.DSSKey.from_private_key_file(server['privatekeyfile'] )
                ssh.connect(server['host'], port=server['port'], username=server['user'], pkey=k) 
            else:
                print("No password stagegy set. Leave", flush=True)    
                return        
            break
        except paramiko.AuthenticationException:
            print("Authentication failed when connecting to %s" % server['host'], flush=True)
            sys.exit(1)
        except Exception as e:
            print("Could not SSH to %s, retry in 2s: %s" % (server['host'], str(e)), flush=True)
            i += 1
            time.sleep(2)
        
        # If we could not connect within time limit
        if i >= retry_time:
            print("Could not connect to %s. Giving up" % server['host'], flush=True)
            exit(1)
    if (tracecx): print("Connected to %s" % server['host'], flush=True)
    return ssh


def run_cmd(server, cmd_list, trace=False):
    ssh = connect_server(server)
    for command in cmd_list:
        # print command
        if trace:
            print ("> " + command, flush=True)
        # execute commands
        stdin, stdout, stderr = ssh.exec_command(command)
        
        opt = stdout.readlines()
        opt = "".join(opt)
        opterr = stderr.readlines()
        opterr = "".join(opterr)
        if trace:
            print(opt+opterr, flush=True)

    # Close SSH connection
    ssh.close()
    ret=""
    if opt and opterr:
        ret = opt +"\n"+ opterr
    elif opt:
        ret=opt
    else:
        ret=opterr        
    return ret