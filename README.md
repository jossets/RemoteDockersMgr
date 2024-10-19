# RemoteDockersMgr



Web API to Manage docker instances on remote hosts



## Setup

````
cp config.yaml.ori config.yaml
````

Pour la connection ssh, préciser le mot de passe
    password: xxxxxxx
ou le chemin du fichier contenant le certificat privé
   privatekeyfile: mycreds/id_rsa.priv


## Start 

````
pip install -r requirements.txt
./remoteDockersMgr.py
````


## List servers  

````
$ curl http://localhost:14000/serverlist
["ChallServer01", "ChallServer02"]
````


## Docker run

````
$ curl "http://localhost:14000/dockerrun?server=ChallServer01&image=nginx:1.25&name=mynginx3&port=80&label=UID%3DUSERID_345642456"
"ada236a60961765a0bc7d8527de4cec31fa6e70f3b57bf98a2453d14ffb71d17"
````

## Docker ps

````
curl -s http://localhost:14000/dockerps?server=ChallServer01 | jq .
````


## Docker Stop and Destroy

````
$ curl "http://localhost:14000/dockerdestroy?server=ChallServer01&id=79a836407792ad8af976ebed2dca769de9ec7acd48d55d972aa928aa526c1161"
"79a836407792ad8af976ebed2dca769de9ec7acd48d55d972aa928aa526c1161"
````


# Sur les serveurs distant


Installer docker, et faire en sorte que les logs n'écrasent pas le disque
```
cat /etc/docker/daemon.json
{
  "log-driver": "json-file",
  "log-opts": {
    "max-size": "10m",
    "max-file": "3"
  },
  "dns": ["8.8.8.8"]
}
```

Configurer la même Timezone sur tous les serveurs distants
Configurer l'heure à partir d'internet