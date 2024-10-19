#!/usr/bin/env python3

import json

from remoteDockersMgrSsh import *


def remote_docker_ps_all(server):
    dockers = []
    # print("remote_docker_ps_all "+server['name'])
    ret = run_cmd(server, [
        "docker ps --all --no-trunc --format='{{json .}}'",
    ])
    # print(ret)
    for line in ret.splitlines():
        # print(line)
        try:
            js = json.loads(line)
            # print("{0}  {1}   {2}".format(js['Image'], js['State'], js['Status']))
            dockers.append(js)
        except:
            pass
    return dockers


def remote_docker_run(server, image, containername="", dockerporttoexpose=0, label=""):
    # print("remote_docker_start [", image, containername, dockerporttoexpose, "]")
    memlimit = '--memory="512m"'
    cpulimit = '--cpus="0.2"'  # 20% of a cpu
    cpushare = '--cpu-shares="1024"'  # default is 1024, set to 2048 to get 2 x more cpu than other containers
    argcontainername = ""
    if containername != "":
        argcontainername = f"--name={containername}"
    argportmapping = ""
    if dockerporttoexpose != "":
        argportmapping = f"-p{dockerporttoexpose}"
    arglabel = ""
    if label != "":
        arglabel = f"-l {label}"
    cmd = f"docker run -d --rm {arglabel} {memlimit} {cpulimit} {cpushare} {argcontainername} {argportmapping} {image} "
    # print("["+cmd+"]")
    ret = run_cmd(server, [cmd])
    ret = ret.strip()
    # print(ret)
    return ret


def remote_docker_kill(server, id):
    dockers = []
    ret = run_cmd(server, [
        f"docker rm -f {id}",  # so brutal :)
    ])
    ret = ret.strip()
    return ret
