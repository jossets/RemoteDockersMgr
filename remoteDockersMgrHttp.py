#!/usr/bin/env python3

import base64
import traceback
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

from remoteDockersMgrConfig import *
from remoteDockersMgrDocker import *


def clean_uid(uid):
    return ''.join(filter(lambda c: c in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVXYZ1234567890-_", uid))


def clean_string(text):
    return ''.join(i for i in text if i.isprintable())


def clean_param(uid):
    return ''.join(filter(lambda c: c in "ABCDEFGHIJKLMNOPQRSTUVWXYabcdefghijklmnopqrstuvwxyz1234567890_-", uid))


def clean_image(image):
    return ''.join(filter(lambda c: c in "ABCDEFGHIJKLMNOPQRSTUVWXYabcdefghijklmnopqrstuvwxyz1234567890_-:/.", image))


def clean_base64(image):
    return ''.join(filter(lambda c: c in "ABCDEFGHIJKLMNOPQRSTUVWXYabcdefghijklmnopqrstuvwxyz1234567890+=/", image))


def clean_dockerid(id):
    return ''.join(filter(lambda c: c in "ABCDEFabcdef1234567890", id))


class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    # Default response
    def do_GET_default(self):
        self.send_response(200)
        self.end_headers()
        str = "<html>Remote Dockers Mgr: Ready</html>"
        self.wfile.write(str.encode(encoding='utf_8'))

    # Error response
    def do_GET_error(self, msg):
        self.send_response(403)
        self.end_headers()
        str = "<html>" + msg + "</html>"
        self.wfile.write(str.encode(encoding='utf_8'))

    # Parse parameters
    def param_get(self, param):
        query_components = parse_qs(urlparse(self.path).query)
        # print(query_components)
        paramvalue = ""
        if param in query_components:
            paramvalue = query_components[param][0]
            # print(paramvalue)
            # print("found "+param+"="+paramvalue)
        return paramvalue

    def param_get_image(self, param):
        imageraw = self.param_get('image')
        image = clean_image(imageraw)
        return image

    def checkSecret(self):
        # print("Check secret")
        if (config()['secret'] == "") or (config()['secret']) == None:
            return True
        secretraw = self.param_get('secret')
        secretbase64 = clean_base64(secretraw)
        secret = base64.b64decode(secretbase64)
        return secret == config()['secret']

    def do_GET_serverlist(self):
        status = config_get_servers()
        json_str = json.dumps(status)
        # print("do_GET_serverlist: ["+json_str+"]")
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json_str.encode(encoding='utf_8'))

    def do_GET_dockerps(self):
        serverraw = self.param_get('server')
        server = clean_string(serverraw)
        # print(server)
        # print("do_GET_dockerps: ["+server+"]")
        serverentry = config_get_server(server)
        if (not (server in config_get_servers())) or (serverentry == None):
            self.do_GET_error("Bad server name")
            return

        ret = remote_docker_ps_all(serverentry)
        # print(ret)
        json_str = json.dumps(ret)
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json_str.encode(encoding='utf_8'))

    def do_GET_dockerrun(self):
        serverraw = self.param_get('server')
        server = clean_string(serverraw)
        serverentry = config_get_server(server)
        if (not (server in config_get_servers())) or (serverentry == None):
            self.do_GET_error("Bad server name")
            return

        imageraw = self.param_get('image')
        image = clean_image(imageraw)
        # print(image)

        nameraw = self.param_get('name')
        name = clean_image(nameraw)
        # print(name)

        portraw = self.param_get('port')
        port = clean_image(portraw)

        labelraw = self.param_get('label')
        label = clean_image(labelraw)

        ret = remote_docker_run(serverentry, image, name, port, label)

        json_str = json.dumps(ret)
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json_str.encode(encoding='utf_8'))

    def do_GET_dockerdestroy(self):
        serverraw = self.param_get('server')
        server = clean_string(serverraw)
        serverentry = config_get_server(server)
        if (not (server in config_get_servers())) or (serverentry == None):
            self.do_GET_error("Bad server name")
            return

        idraw = self.param_get('id')
        id = clean_dockerid(idraw)

        ret = remote_docker_kill(serverentry, id)
        json_str = json.dumps(ret)
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json_str.encode(encoding='utf_8'))

    def do_GET(self):
        try:
            print("[+] HTTP GET %s" % clean_string(self.path), flush=True)
            if not self.checkSecret():
                self.do_GET_error("Bad shared secret")
                return

            if self.path.startswith("/serverlist"):
                self.do_GET_serverlist()
            elif self.path.startswith("/dockerps"):
                self.do_GET_dockerps()
            elif self.path.startswith("/dockerrun"):
                self.do_GET_dockerrun()
            elif self.path.startswith("/dockerdestroy"):
                self.do_GET_dockerdestroy()
            else:
                self.do_GET_default()
        except Exception as e:
            print(e, flush=True)
            print(traceback.format_exc(), flush=True)


def HTTP_serve_forever(host, port):
    httpd = HTTPServer((host, port), SimpleHTTPRequestHandler)
    httpd.serve_forever()
