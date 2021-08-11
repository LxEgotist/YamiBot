#!/usr/bin/env python
# -*- coding: utf-8 -*- __init__.py
# -*- coding: utf-8 -*- @author LxEgotist
# -*- coding: utf-8 -*- @description 
# -*- coding: utf-8 -*- @created 2020-11-09T18:55:49.558Z+08:00
# -*- coding: utf-8 -*- @last-modified 2020-11-09T18:55:59.367Z+08:00
#

import yaml
from pathlib import Path


def load_yaml(file: Path) -> dict:
    '''
    读取yaml文件
    :return: dict
    '''
    with open(file, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)
    return data