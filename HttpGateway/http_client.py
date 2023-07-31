#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@ Project     : gateway 
@ File        : rmi_client.py
@ Author      : yqbao
@ Version     : V1.0.0
@ Description : 
"""
import atexit
import json
import os
import time

import requests

OPC_SERVER = 'Kepware.KEPServerEX.V6'
GROUP_NAME = 'group0'
TAG_LIST = [
    u'channel_1.Test_1.K1',
    u'channel_1.Test_7.K7',
    u'channel_2.Test_1.Random1'
]

if "PYRO_HTTPGATEWAY_KEY" in os.environ:
    gateway_key = os.environ["PYRO_HTTPGATEWAY_KEY"]
else:
    gateway_key = ''

HOST = "http://192.167.6.192:7767"
headers = {'x-pyro-gateway-key': gateway_key}


def pyro():
    try:
        url = f"{HOST}/pyro/"
        response = request(method="get", url=url, header=headers)
        with open('pyro.html', 'w', encoding='utf-8') as f:
            f.write(response.text)
    except requests.exceptions.ConnectionError:
        print("[WinError 10061] 由于目标计算机积极拒绝，无法连接。")
    except Exception as e:
        print(e)


def creat_client():
    try:
        url = f"{HOST}/pyro/remote.opcda.client/creat_client"
        response = request(method="get", url=url, header=headers)
        print(response.text)
    except requests.exceptions.ConnectionError:
        print("[WinError 10061] 由于目标计算机积极拒绝，无法连接。")
    except Exception as e:
        print(e)


def connect():
    url = f"{HOST}/pyro/remote.opcda.client/connect?opc_server={OPC_SERVER}"
    response = request(method="get", url=url, header=headers)
    print(response.text)


def read():
    url = "{}/pyro/remote.opcda.client/read".format(HOST)
    data = {"tags": TAG_LIST, "group": GROUP_NAME, "timeout": 5000, "sync": False}
    response = request(method="post", url=url, data=data, header=headers)
    # print(response.text)
    resolve(response)


def reads():
    url = "{}/pyro/remote.opcda.client/read".format(HOST)
    data = {"tags": TAG_LIST, "timeout": 5000, "sync": False}
    response = request(method="post", url=url, data=data, header=headers)
    # print(response.text)
    resolve(response)


def info():
    url = f"{HOST}/pyro/remote.opcda.client/info"
    response = request(method="get", url=url, header=headers)
    print(response.text)


def ping():
    url = f"{HOST}/pyro/remote.opcda.client/ping"
    response = request(method="get", url=url, header=headers)
    print(response.text)


def groups():
    url = f"{HOST}/pyro/remote.opcda.client/groups"
    response = request(method="get", url=url, header=headers)
    print(response.text)


def servers():
    url = f"{HOST}/pyro/remote.opcda.client/servers"
    response = request(method="get", url=url, header=headers)
    print(response.text)


def lists():
    url = f"{HOST}/pyro/remote.opcda.client/lists"
    response = request(method="get", url=url, header=headers)
    print(response.text)


def remove(group):
    url = f"{HOST}/pyro/remote.opcda.client/remove?groups={group}"
    response = request(method="get", url=url, header=headers)
    print(response.text)


@atexit.register
def end():
    print("end")


def close():
    url = f"{HOST}/pyro/remote.opcda.client/close"
    data = {"del_object": False}
    response = request(method="POST", url=url, data=data, header=headers)
    print(response.text)


def request(method: str, url, header, data: dict = None, timeout=300):
    if method.upper() == "GET":
        response = requests.request(method='GET', url=url, headers=header, timeout=timeout)
    else:
        response = requests.request(method='POST', url=url, data=data, headers=header, timeout=timeout)
    return response


def resolve(opc_data):
    try:
        opc_data = str(opc_data.content, encoding="utf-8")
        opc_data = json.loads(opc_data)
        send_values = {}
        for item in list(opc_data):
            name, value, quality, time_ = item
            if quality == 'Good':
                send_values[name] = value
            else:
                print('Error:  {}'.format(item))
            send_values['time'] = time_
        print(send_values)
        with open('values.txt', 'a+', encoding='utf-8') as f:
            f.write(json.dumps(send_values) + '\n')
    except Exception as e:
        print(e.args)


if __name__ == '__main__':
    try:
        close()  # 避免客户端异常退出后，远程客户端未关闭，故在启动前，先关闭可能存在的OPC连接
    except Exception as e:
        print(e)
    finally:
        pyro()  # 查看远程注册的方法，返回一个html
        creat_client()  # 创建远程客户端
        connect()  # 连接OPC服务
        servers()  # 查看已有服务列表
        read()  # 读取OPC数据，返回(tag,time,value)
        info()  # 查看opc服务信息
        ping()  # 检查是否连接opc
        groups()  # 查看读取时划分的组
        lists()  # 查看OPC服务全部节点
        i = 1
        while i < 10:
            reads()
            time.sleep(1)
            i += 1
        remove(GROUP_NAME)  # 删除划分的组，需要先停止读取，否则报错
        close()  # 关闭OPC连接
        ping()
