# -*- coding: utf-8 -*-
# File       : rmi_client.py
# Time       : 2022/07/25 9:42
# Author     ：
# Version    : V1.0.0
# Description: # 仅支持32位的python
import time
from OpenOPC_Py38.src import OpenOPC

from read.read_data import FormattingExcel

message = ''


def client():
    """
    只读本地客户端
    注意：仅支持32位的python
    :return:
    """
    GROUP_NAME = 'group0'
    OPC_SERVER = 'Kepware.KEPServerEX.V6'
    TAG_LIST = [
        u'channel_1.Test_1.K1',
        u'channel_1.Test_7.K7',
        u'channel_2.Test_1.Random1'
    ]

    opc = OpenOPC.Client()
    opc.connect(OPC_SERVER)
    opc.read(tags=TAG_LIST, group=GROUP_NAME)
    resolve(opc, TAG_LIST)


def open_write():
    """
    只写远程客户端
    注意：仅支持32位的python
    :return:
    """
    OPC_GATE_HOST = '192.168.1.200'
    OPC_GATE_PORT = 7766
    OPC_SERVER = 'Kepware.KEPServerEX.V6'

    path = "read/document/批量写opc数据.xlsx"
    name = "Sheet1"
    ex = FormattingExcel(path, name)
    TAG_LIST = ex.read()

    opc = OpenOPC.open_client(OPC_GATE_HOST, OPC_GATE_PORT)
    opc.connect(OPC_SERVER)
    opc.write(TAG_LIST)


def open_client():
    """
    只读远程客户端
    注意：仅支持32位的python
    :return:
    """
    OPC_GATE_HOST = '192.167.6.192'
    OPC_GATE_PORT = 7766

    OPC_SERVER = 'Kepware.KEPServerEX.V6'
    GROUP_NAME = 'group0'
    TAG_LIST = [
        u'channel_1.Test_1.K1',
        u'channel_1.Test_7.K7',
        u'channel_2.Test_1.Random1'
    ]

    opc = OpenOPC.open_client(OPC_GATE_HOST, OPC_GATE_PORT)
    opc.connect(OPC_SERVER)
    opc.read(tags=TAG_LIST, group=GROUP_NAME, timeout=5000, sync=True)
    resolve(opc, TAG_LIST)


def resolve(opc, tag_list):
    try:
        while True:
            # 请求组
            print(opc.properties(tags=tag_list))
            opc_data = opc.read(tags=tag_list, timeout=5000, sync=True)
            send_values = {}
            for item in opc_data:
                name, value, quality, time_ = item
                if quality == 'Good':
                    send_values[name] = value
                else:
                    print('Error:  {}'.format(item))
                send_values['time'] = time_
            print(send_values)

            time.sleep(1)
    finally:
        # 释放资源
        opc.remove(opc.groups())
        opc.close()


if __name__ == '__main__':
    # client()
    # open_write()
    open_client()
