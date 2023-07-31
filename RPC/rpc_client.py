#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@Project ：tools 
@File    ：rpc_client.py
@Author  ：yqbao
@Date    ：2022/10/10 16:34 
"""
import pickle
import time
from multiprocessing.connection import Client


class RPCProxy:
    def __init__(self, connection):
        self._connection = connection

    def __getattr__(self, name):
        def do_rpc(*args, **kwargs):
            try:
                self._connection.send(pickle.dumps((name, args, kwargs)))
                result = pickle.loads(self._connection.recv())
                if isinstance(result, Exception):
                    raise result
                return result
            except ConnectionResetError:
                pass

        return do_rpc


def open_client():
    """
    只读远程客户端
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
    proxy = None
    try:
        c = Client(('192.167.6.167', 27000), authkey=b'peekaboo')
        proxy = RPCProxy(c)
        proxy.create_client()
        proxy.connect(OPC_SERVER)
        proxy.read(GROUP_NAME, TAG_LIST, 1)
        while True:
            # 请求组
            opc_data = proxy.read(GROUP_NAME, TAG_LIST, 1)
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
    except ConnectionRefusedError:
        print("由于目标计算机积极拒绝，无法连接")
    except ConnectionResetError:
        print("远程主机强迫关闭了一个现有的连接")
    except TypeError:
        print("远程服务已断开")
    finally:
        # 释放资源
        try:
            proxy.remove()
            proxy.close()
        except AttributeError:
            pass


if __name__ == '__main__':
    open_client()
