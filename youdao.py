#! /usr/bin/python3
# -*- coding:utf-8 -*-

import sys
import uuid
import requests
import hashlib
import time

YOUDAO_URL = 'http://openapi.youdao.com/api'
APP_KEY = '2ba19d7e3ed057cf'
APP_SECRET = '8z6MGtGsyVoervF5Fk3yET4xsNOqgjet'


def query_content():
    content = ""
    arr = sys.argv[1:]
    for arg in arr:
        content = content+" "+arg
    if(content == ""):
        print("Usage:python3 %s <The words or sentences you want to query>" % sys.argv[0])
        sys.exit()
    return content


def encrypt(signStr):   # sha256加密
    hash_algorithm = hashlib.sha256()
    hash_algorithm.update(signStr.encode('utf-8'))
    return hash_algorithm.hexdigest()


def truncate(q):
    if q is None:
        return None
    size = len(q)
    return q if size <= 20 else q[0:10] + str(size) + q[size - 10:size]


def do_request(data):
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    return requests.post(YOUDAO_URL, data=data, headers=headers)


def print_formatted(content):
    print("\033[1;33m"+content.get('query').lstrip()+"\033[0m")
    basic = content.get('basic')
    web = content.get('web')
    if(basic):
        if(basic.get('us-phonetic')):
            print("\033[1;33m"+"美["+basic.get('us-phonetic')+"]"+"\033[0m",end="")
            if(basic.get('uk-phonetic')):
                print("\033[1;33m"+"    英["+basic.get('uk-phonetic')+"]"+"\033[0m",end="")
            print()
        elif(basic.get('uk-phonetic')):
            print("\033[1;33m"+"英["+basic.get('uk-phonetic')+"]"+"\033[0m")
        for e in basic.get('explains'):
            print("\033[1;36m"+e+"\033[0m")
        if(basic.get('wfs')):
            print("\033[1;35m"+"[",end="")
            for wf in basic.get('wfs'):
                w = wf.get('wf')
                print(w.get('name')+" "+w.get('value')+" ",end="")
            print("]"+"\033[0m")
    else:
        for translate in content.get('translation'):
            print("\033[1;36m"+translate+"\033[0m")

    if(web):
        print("\033[1;34m"+"网络释义"+"\033[0m")
        for item in web:
            print("\033[1;33m"+item.get('key')+" "+"\033[0m",end="")
            for i,val in enumerate(item.get('value')):
                if(i != len(item.get('value'))-1):
                    print("\033[1;36m"+val+","+"\033[0m",end="")
                else:
                    print("\033[1;36m"+val+"\033[0m")


def connect():
    q = query_content()
    data = {}
    data['from'] = 'auto'
    data['to'] = 'auto'
    data['signType'] = 'v3'
    curtime = str(int(time.time()))
    data['curtime'] = curtime
    salt = str(uuid.uuid1())
    signStr = APP_KEY + truncate(q) + salt + curtime + APP_SECRET
    sign = encrypt(signStr)
    data['appKey'] = APP_KEY
    data['q'] = q
    data['salt'] = salt
    data['sign'] = sign

    response = do_request(data)
    if(response.status_code == 200):
        content = response.json()
        print_formatted(content)
    else:
        print("request error!!!")


if __name__ == '__main__':
    connect()
