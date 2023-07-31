# -*- coding: utf-8 -*-
# File       : read_data.py
# Time       : 2022/08/03 11:01
# Author     ：
# Version    : V1.0.0
# Description:
import pandas as pd


class FormattingExcel(object):

    def __init__(self, file_path, sheet_name):
        self.file_path = file_path
        self.sheet_name = sheet_name

    def read(self):
        """
        读取excel文件
        Returns:
            格式[(),()]
        """
        df = pd.read_excel(self.file_path, sheet_name=self.sheet_name)
        rows = len(df.values)
        base = []
        for x in range(0, rows):
            base_data = [df.values[x][0], df.values[x][1]]
            base.append(tuple(base_data))
        return base


if __name__ == '__main__':
    path = "document/批量写opc数据.xlsx"
    name = "Sheet1"
    ex = FormattingExcel(path, name)
    ex.read()
