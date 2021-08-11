#!/usr/bin/env python
# -*- coding: utf-8 -*- data.py
# -*- coding: utf-8 -*- @author LxEgotist
# -*- coding: utf-8 -*- @description 
# -*- coding: utf-8 -*- @created 2020-11-09T17:16:26.571Z+08:00
# -*- coding: utf-8 -*- @last-modified 2020-11-09T18:08:42.562Z+08:00
#




from datetime import datetime

import httpx,random,json,sys
from pathlib import Path
from utils.helpers import render_expression
data_pth=Path('.')/'LxBot'/'data'

def get_first_connect_message():
	""" 根据当前时间返回对应消息 """
	hour = datetime.now().hour
	if hour < 6:
		return '好困呐'
	if hour > 18:
		return '晚上好呀！'
	if hour > 13:
		return '下午好呀！'
	if hour > 11:
		return '中午好呀！'
	return '哦嗨哟！'

with open(data_pth/"sentence.json",'r',encoding='utf-8') as f:
	EXPR_MORNING=set(json.load(f)['morning'])
EXPR_MORNING=[x+'\n{message}' for x in list(EXPR_MORNING)]


async def get_moring_message() -> str:
	""" 获得早上问好
	日期不同，不同的问候语
	通过 [免费节假日 API](http://timor.tech/api/holiday/)
	"""
	try:
		# 获得不同的问候语
		async with httpx.AsyncClient() as client:
			r = await client.get('http://timor.tech/api/holiday/tts')
			rjson = r.json()
	except:
		rjson = {'code': -1}

	if rjson['code'] == 0:
		message = rjson['tts']
	else:
		message = '好像没法获得节假日信息了，嘤嘤嘤'

	return render_expression(EXPR_MORNING, message=message)

if __name__=='__main__':
	print(EXPR_MORNING)