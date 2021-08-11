'''
Descripttion: 
version: 
Author: LxEgotist
Date: 2020-11-06 13:05:55
LastEditors: LxEgotist
LastEditTime: 2020-11-06 13:15:40
'''
import json
from pathlib import Path
from typing import Optional

def whiteList(user: Optional[str] = None, group: Optional[str] = None) -> bool:
    """
    :说明:

      判断某一 用户/群 是否处于封禁名单中。

    :参数:

      * ``user: Optional[str] = None``: 用户QQ号
      * ``group: Optional[str] = None``: 用户所在群号
      * !!!二者必须传入一个，否则一律返回 False !!!

    :返回:
      
      是：False | 否：True
    
    :用法:

    .. code-block:: python
      
        whiteList(user=123456789, group=123456789)

    """
    file_user = Path('.') / 'utils' / 'utils_whiteList' / 'whiteList_user.json'
    file_group = Path('.') / 'utils' / 'utils_whiteList' / 'whiteList_group.json'

    with open(file_user, 'r') as f:
        data_user = json.load(f)
    with open(file_group, 'r') as f:
        data_group = json.load(f)    
    if user:
        if user in data_user['list']:
            flag = True
        else:
            flag = False
        if user in data_user['tmp']:
            flag = True
            data_user["tmp"].remove(user)
            with open(file_user, 'w') as f:
                json.dump(data_user,f)
        return flag

    elif group:
        if group in data_group['list']:
            return True
        else:
            return False
    else:
        return False