# RemoteDockersMgr

Web API to Manage docker instances on remote hosts

## On API Server

### Setup

```bash
cp config.yaml.ori config.yaml
```

For SSH connexion, please provide the password:
    password: xxxxxxx
Or the private key path:
   privatekeyfile: mycreds/id_rsa.priv

Note: The password is prioritary over the private key file, if both are provided, the password will be used. For security reasons, it is recommended to use the private key file.

### How to add authentication with a secret

- Add string in `secret` of `config.yaml` file
- Convert the string to base64
- Add `?secret=base64string` to the URL to access the API (do not forget to replace `base64string` by the base64 string)

```bash
curl "http://localhost:14000/serverlist?secret=QWJjZGVmZ2hpamsxMiQ="
```

> ["ChallServer01", "ChallServer02"]

### Start

```bash
pip install -r requirements.txt
./remoteDockersMgr.py
```

### List servers  

```bash
curl http://localhost:14000/serverlist
```

> ["ChallServer01", "ChallServer02"]

### Docker run

```bash
curl "http://localhost:14000/dockerrun?server=ChallServer01&image=nginx:1.25&name=mynginx3&port=80&label=UID%3DUSERID_345642456"
```

> ada236a60961765a0bc7d8527de4cec31fa6e70f3b57bf98a2453d14ffb71d17

### Docker ps

```bash
curl -s http://localhost:14000/dockerps?server=ChallServer01 | jq .
```

### Docker Stop and Destroy

```bash
curl "http://localhost:14000/dockerdestroy?server=ChallServer01&id=79a836407792ad8af976ebed2dca769de9ec7acd48d55d972aa928aa526c1161"
```

> 79a836407792ad8af976ebed2dca769de9ec7acd48d55d972aa928aa526c1161

## On Remote Server (who accessed by SSH)

Installer docker, et faire en sorte que les logs n'écrasent pas le disque

```bash
cat /etc/docker/daemon.json
```
  
```json
{
  "log-driver": "json-file",
  "log-opts": {
    "max-size": "10m",
    "max-file": "3"
  },
  "dns": ["8.8.8.8"]
}
```

## On all servers

Use the same Timezone on all servers

```bash
timedatectl set-timezone Europe/Paris ## Replace Europe/Paris by your timezone
```

Set the time from the internet

```bash
timedatectl set-ntp true
```
