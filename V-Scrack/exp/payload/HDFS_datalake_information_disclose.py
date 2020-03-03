# coding:utf-8

import os
import sys
import json
#from lxml import etree(Python3.5以上不支持该种引用方法)

from lxml import html
etree = html.etree

from io import StringIO
import multiprocessing
from urllib.parse import urlparse
import requests
import urllib.parse,urllib.request,urllib.parse
import ssl

ssl._create_default_https_context = ssl._create_unverified_context

API = "/webhdfs/v1"
option = "LISTSTATUS"

PORT = 50070
HTTP = "http"
HTTPS = "https"
ROOT_PATH = "/"
DEPTH = "-1"

class File_HDFS():
    def __init__(self, filetype, permission, owner, group, pathSuffix, modificationTime, path,host):
        self.filetype = filetype
        self.perm = permission
        self.owner = owner
        self.group = group
        self.pathSuffix = pathSuffix
        self.lastModif = modificationTime
        self.path = path
        self.host = host
        self.children = []

    def is_directory(self):
        return True if self.filetype == "DIRECTORY" else False

    def print_HDFS(self):
        # t = "d" if self.is_directory() else "-"
        print(self.perm + "  " + self.owner + ":" + self.group + "  " + str(
            self.lastModif) + "  " + self.pathSuffix + "  " + self.path)

    def get_url(self):
        return "http://" + self.host + ":" + str(PORT) + API + self.path + "?op=" + option + "&user.name=" + self.owner

    def print_HDFS_csv(self):
        return ";".join([str(self.lastModif), self.filetype, self.perm, self.owner, self.group, self.pathSuffix,
                         self.get_url()]) + "\n"

    def add_child(self, child):
        self.children.append(child)

f = lambda x: [int(i) for i in bin(x)[2:].zfill(3)]
g = lambda tuplet_list: tuplet_list[0] if tuplet_list[1] else '-'
h = lambda l1, l2: [t for t in zip(l1, l2)]

def perm_to_str(num):
    s = ['r', 'w', 'x']
    num = [int(i) for i in str(num)]

    if all(map(lambda x: x < 8, num)) and len(num) == 3:
        return "".join(map(lambda x: "".join(map(g, h(s, f(x)))), num))
    else:
        return "--ERROR--"

def parse_hdfs_json(json_string, path):
    data_json = json.loads(json_string)
    files_HDFS = []
    for f in data_json['FileStatuses']['FileStatus']:
        tmp_path = path + f["pathSuffix"] + \
            ("/" if f["type"] == "DIRECTORY" else "")
        permission = perm_to_str(int(f["permission"]))
        files_HDFS.append(
            File_HDFS(f["type"], permission, f["owner"], f["group"], f["pathSuffix"], f["modificationTime"], tmp_path,HOST))

    return files_HDFS

def parse_hdfs_xml(xml_string):
    tree = etree.parse(StringIO(xml_string))
    files_HDFS = []
    for e in tree.xpath("/listing")[0].getchildren():
        f = {
            "permission": None,
            "owner": None,
            "group": None,
            "pathSuffix": None,
            "modified": None,
            "path": None
        }
        if e.tag == "directory" or e.tag == "file":
            f["filetype"] = e.tag

            for attribut in e.keys():
                f[attribut] = e.get(attribut)

            f["pathSuffix"] = f["path"].split("/")[-1]
            files_HDFS.append(
                File_HDFS(f["filetype"], f["permission"], f["owner"], f["group"], f["pathSuffix"], f["modified"],
                          f["path"],HOST))
    return files_HDFS

def request_namenode(path, user):
    op = "op=LISTSTATUS"
    URL = "http://" + HOST + ":" + \
        str(PORT) + API + path + "?" + op + "&user.name=" + user
    response = requests.get(URL, verify=False,timeout=3)
    data = None
    if response.ok:
        data = response.text
    return data

def request_namenode_multi(file_HDFS):
    return request_namenode(file_HDFS.path, file_HDFS.owner)

def request_namenode_multi2(file_HDFS, q):
    return request_namenode(file_HDFS.path, file_HDFS.owner)


def hdfs_listpaths(user, host, path, use_recursion, output):
    rec = "yes" if use_recursion else "no"
    URL = "http://" + host + ":" + \
        str(PORT) + "/listPaths" + path + "?recursive=" + rec

    try:
        response = requests.get(URL,verify=False,timeout=3)
        if response.ok:
            files_HDFS = parse_hdfs_xml(response.content)
            if output:
                with open(output, 'w') as f:
                    for e in files_HDFS:
                        f.write(e.print_HDFS_csv())
                f.close()
            else:
                for e in files_HDFS:
                    e.print_HDFS()
    except:
        return False
    return True

def hdfs_ls(path, user, output):
    json_string = request_namenode(path, user)
    t = []
    if json_string:
        files_HDFS = parse_hdfs_json(json_string, path)
        jobs = []
        for e in files_HDFS:
            if e.is_directory():
                p = multiprocessing.Process(target=hdfs_ls, args=(e.path, e.owner, output))
                for child in hdfs_ls(e.path, e.owner, output):
                    e.add_child(child)
    else:
        files_HDFS = ''

    return files_HDFS

def init_ls(path, user, port, depth):
    json_string = request_namenode(path, user)
    files_HDFS = parse_hdfs_json(json_string, path)
    if depth:
        hdfs_ls_multi(files_HDFS, depth - 1)
    return files_HDFS

def hdfs_ls_multi(files_HDFS, depth):
    p = multiprocessing.Pool(10)
    json_strings = p.map(request_namenode_multi, files_HDFS)
    p.close()
    p.join()
    for parent, json_string in zip(files_HDFS, json_strings):
        tt = parse_hdfs_json(json_string, parent.path)
        if depth:
            output = hdfs_ls_multi([e for e in tt if e.is_directory()], depth - 1)
        parent.children = tt

def print_arbo(file_HDFS):
    if file_HDFS.children != []:
        print(file_HDFS.path + " : ")
        for child in file_HDFS.children:
            child.print_HDFS()
        for child in file_HDFS.children:
            print_arbo(child)

def print_list(files_HDFS):
    for e in files_HDFS:
        e.print_HDFS()
    for e in files_HDFS:
        print_arbo(e)

service_names = {
    "whdfs": "WebHDFS",
    "httpfs": "HttpFS"
}

service_ports = {
    "whdfs": 50070,
    "httpfs": 14000
}

def build_URL(protocol, host, port, rp_path, root_path, api_path, option):
    if rp_path:
        return "%s://%s:%s%s%s%s?op=%s" % (protocol, host, port, rp_path, api_path, root_path, option)
    else:
        return "%s://%s:%s%s%s?op=%s" % (protocol, host, port, api_path, root_path, option)

def test_service(method, port):
    try:
        URL = build_URL(PROTOCOL, HOST, port, RP_PATH, "/", API, option)
        # print URL
        response = requests.get(URL,verify=False,timeout= 3)
        if response.ok:
            return True
        else:
            return False
    except:
        return False

def test_all_services():
    found_services = {}
    counter = 0

    for service in service_names:
        if test_service(service, service_ports[service]):
            found_services.update({service: True})
            counter += 1
        else:
            found_services.update({service: False})
    return found_services, counter

def test_vul(host):
    global HOST, PORT, PROTOCOL, URL, RP_PATH, ROOT_PATH
    PORT = 50070
    PROTOCOL = HTTP
    ROOT_PATH = "/"
    RP_PATH = ""
    DEPTH = -1
    HOST = host

    services, counter = test_all_services()
    if counter:
        if "whdfs" in services:
            PORT = service_ports["whdfs"]
            result = hdfs_listpaths("user", host, ROOT_PATH, False, "/")
            if not result:
                files_HDFS = init_ls(
                    ROOT_PATH, "hdfs", service_ports["whdfs"], DEPTH)
                return files_HDFS
        else:
            PORT = service_ports["httpfs"]
            files_HDFS = init_ls(
                ROOT_PATH, "hdfs", service_ports["whdfs"], DEPTH)
            return files_HDFS

    return None

def verify(protocol,ip,port):
    oldurl = protocol+'://'+ip+':'+str(port)
    print('testing if HDFS datalake information disclose vul')
    result = {}
    depth = "-1"
    ROOT_PATH = "/"
    pr = urlparse(oldurl)
    host=ip

    try:
        files_HDFS = test_vul(host)
        v_url = files_HDFS[0].get_url() if files_HDFS else oldurl
        if files_HDFS:
            result['ShellInfo'] = {}
            result['ShellInfo']['URL'] = v_url
        if result:
            msg = 'There is HDFS datalake information disclose vul on url: ' + v_url + '  .'
            number = 'v90'
            print(msg)
            return True, oldurl, number, msg
    except Exception as e:
        msg = str(e)
        number = 'v0'
        return False, oldurl, number, msg
    msg = 'There is no HDFS datalake information disclose vul'
    number = 'v0'
    return False, oldurl, number, msg

