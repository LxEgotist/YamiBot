#!/usr/bin/env python
# -*- coding: utf-8 -*- getSentence.py
# -*- coding: utf-8 -*- @author LxEgotist
# -*- coding: utf-8 -*- @description 
# -*- coding: utf-8 -*- @created 2020-11-09T18:11:34.138Z+08:00
# -*- coding: utf-8 -*- @last-modified 2020-11-09T18:18:27.061Z+08:00
#
from pathlib import Path
import json,random
data_pth=Path('.')/'LxBot'/'data'
def getSentence(type:str)->str:
	with open(data_pth/'sentence.json','r') as f:
		js=json.load(f)
	return random.choice(js)