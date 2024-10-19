#!/usr/bin/env python3
 
import yaml

config={}

def config():
    global config 
    return config


def config_load():
    global config
    config=None
    with open("config.yaml", 'r') as stream:
        try:
            config = (yaml.safe_load(stream))
            #print(config)
        except yaml.YAMLError as exc:
            print(exc)
    #print(config)
    return config

def config_get_servers():
    global config
    servers=[]
    if None!=config:
        for server in config['servers']:
            servers.append(server['name'])
    return servers


def config_get_server(name):
    global config
    servers=[]
    if None!=config:
        for server in config['servers']:
            if name == server['name']:
                return server
    return None