#!/usr/bin/env python
# -*- coding: utf-8 -*- master.py
# -*- coding: utf-8 -*- @author LxEgotist
# -*- coding: utf-8 -*- @description 
# -*- coding: utf-8 -*- @created 2020-11-09T19:19:10.770Z+08:00
# -*- coding: utf-8 -*- @last-modified 2020-11-09T19:21:34.613Z+08:00
#

import json
from pathlib import Path

def getMaster()->list:
	with open(Path('.')/'LxBot'/'data'/'master.json','r') as f:
		js=json.load(f)
	return js['list']
