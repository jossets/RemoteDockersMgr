import json
import datetime 
from remoteDockersMgrSsh import *
from remoteDockersMgrConfig import *

#
#{"Command":"\"/docker-entrypoint.sh nginx -g 'daemon off;'\"",
# "CreatedAt":"2024-10-19 19:36:59 +0200 CEST",
# "ID":"79a836407792ad8af976ebed2dca769de9ec7acd48d55d972aa928aa526c1161",
# "Image":"nginx:1.25",
# "Labels":"USERID_345642456=,maintainer=NGINX Docker Maintainers \u003cdocker-maint@nginx.com\u003e",
# "LocalVolumes":"0",
# "Mounts":"",
# "Names":"mynginx3",
# "Networks":"bridge",
# "Ports":"0.0.0.0:32774-\u003e80/tcp, :::32774-\u003e80/tcp",
# "RunningFor":"43 seconds ago",
# "Size":"1.09kB (virtual 187MB)",
# "State":"running",
# "Status":"Up 42 seconds"}
def remote_docker_ps_all(server):
    dockers = []
    #print("remote_docker_ps_all "+server['name'])
    ret = run_cmd(server, [
        "docker ps --all --no-trunc --format='{{json .}}'",
        ]) 
    #print(ret)
    for line in ret.splitlines():
        #print(line)
        try:
            js = json.loads(line)
            #print("{0}  {1}   {2}".format(js['Image'], js['State'], js['Status']))
            dockers.append(js)
        except:
            pass
    return dockers




def remote_docker_run(server, image, containername="", dockerporttoexpose=0, label="", leasetime=0):
    #print("remote_docker_start [", image, containername, dockerporttoexpose, "]")
    memlimit='--memory="512m"'  
    cpulimit='--cpus="0.2"'     # 20% of a cpu
    cpushare='--cpu-shares="1024"' # default is 1024, set to 2048 to get 2 x more cpu than other containers
    argcontainername=""
    if containername!="":
        argcontainername= f"--name={containername}"
    argportmapping=""
    if dockerporttoexpose!="":
        argportmapping=f"-p{dockerporttoexpose}"
    arglabel=""
    if label!="":
        arglabel=f"-l {label}"
    leasetimeend=""
    if 0!=leasetime:
        endtime = ((datetime.datetime.now()+datetime.timedelta(seconds=leasetime)).strftime("%Y-%m-%d %H:%M:%S"))
        leasetimeend=f"-l LEASETIMEEND='{endtime}'"
    cmd = f"docker run -d --rm {arglabel} {leasetimeend} {memlimit} {cpulimit} {cpushare} {argcontainername} {argportmapping} {image} "
    #print("["+cmd+"]")    
    ret = run_cmd(server, [ cmd ]) 
    ret=ret.strip()
    #print(ret)
    return ret


def remote_docker_kill(server, id):
    dockers = []
    ret = run_cmd(server, [
        f"docker rm -f {id}",   # so brutal :)
        ]) 
    ret=ret.strip()    
    return ret