#!/usr/bin/env python3

import yaml
import ipaddress
import os
import re

config = {}


def config():
    global config
    return config


def config_load():
    global config
    config = None
    config_temp = {}
    try:
        with open("config.yaml", 'r') as stream:
            try:
                config_temp = yaml.safe_load(stream)
            except yaml.YAMLError as exc:
                print(f"YAML parsing error: {exc}")
                return None

        config_valid, config_message = check_config(config_temp)
        if not config_valid:
            print(f"Configuration error:\n{config_message}")
        else:
            config = config_temp
            print(f"Configuration loaded successfully")
        return config
    except FileNotFoundError:
        print("Config file 'config.yaml' not found.")
        return None
    except PermissionError:
        print("Permission denied when trying to read 'config.yaml'.")
        return None
    except Exception as e:
        print(f'Unexpected error reading config file: {e}')
        return None

def check_config(conf):
    if conf is None:
        return False, "Configuration not loaded"

    errors = []

    # Main category checks
    if not isinstance(conf.get('debugmode'), bool):
        errors.append("debugmode must be a boolean")

    if not isinstance(conf.get('checkserverlogin'), bool):
        errors.append("checkserverlogin must be a boolean")

    if not isinstance(conf.get('checkservermem'), bool):
        errors.append("checkservermem must be a boolean")

    if not isinstance(conf.get('httpserverhost'), str):
        errors.append("httpserverhost must be a string")

    if not isinstance(conf.get('httpserverport'), int) or not 1 <= conf.get('httpserverport') <= 65535:
        errors.append("httpserverport must be a valid port number (1-65535)")

    if not isinstance(conf.get('secret'), str) or len(conf.get('secret', '')) < 8:
        errors.append("secret must be a string with at least 8 characters")

    if not isinstance(conf.get('servers'), list):
        errors.append("servers must be a list")
    else:
        # Subcategory server checks
        for idx, server in enumerate(conf.get('servers', [])):
            server_errors = []

            if not isinstance(server.get('name'), str) or not server.get('name'):
                server_errors.append("name must be a non-empty string")

            try:
                ipaddress.ip_address(server.get('host', ''))
            except ValueError:
                server_errors.append("host must be a valid IP address")

            if not isinstance(server.get('port'), int) or not 1 <= server.get('port') <= 65535:
                server_errors.append("port must be a valid port number (1-65535)")

            if not isinstance(server.get('user'), str) or not server.get('user'):
                server_errors.append("user must be a non-empty string")

            if server.get('password') and not isinstance(server.get('password'), str):
                server_errors.append("password must be a string or empty")

            if server.get('privatekeyfile'):
                if not isinstance(server.get('privatekeyfile'), str) or not os.path.exists(server.get('privatekeyfile')):
                    server_errors.append("privatekeyfile must be a valid path to an existing file")

            if not isinstance(server.get('host_public'), str) or not re.match(r'^[a-zA-Z0-9.-]+$', server.get('host_public', '')):
                server_errors.append("host_public must be a valid FQDN")

            if not isinstance(server.get('host_public_baseport'), int) or not 1 <= server.get('host_public_baseport') <= 65535:
                server_errors.append("host_public_baseport must be a valid port number (1-65535)")

            if not isinstance(server.get('maxclient'), int) or server.get('maxclient') < 1:
                server_errors.append("maxclient must be a positive integer")

            if not isinstance(server.get('enabled'), bool):
                server_errors.append("enabled must be a boolean")

            if server_errors:
                errors.append(f"Errors in server {idx + 1} ({server.get('name', 'unnamed')}):")
                errors.extend(f"  - {error}" for error in server_errors)

    if errors:
        return False, "\n".join(errors)
    else:
        return True, "Configuration is valid"


def config_get_servers():
    global config
    servers = []
    if None != config:
        for server in config['servers']:
            servers.append(server['name'])
    return servers


def config_get_server(name):
    global config
    servers = []
    if None != config:
        for server in config['servers']:
            if name == server['name']:
                return server
    return None
