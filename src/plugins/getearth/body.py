#!/usr/bin/env python
import getearth
import requests,json,os
from datetime import datetime
SCALE=getearth.SCALE
l1,str_date=getearth.getEarth(flag=1,date='2020-11-03 02:30:00')
date=datetime.strptime(str_date, '%Y-%m-%d %H:%M:%S')
pth='{}d'.format(SCALE)
files_name=date.strftime('%Y%m%d%H%M%S')
proxy = {"https": "socks5://127.0.0.1:10808"} #proxies
if not os.path.exists(pth):
	os.mkdir(pth)
if not os.path.exists(os.path.join(pth,files_name)):
	os.mkdir(os.path.join(pth,files_name))
for (fname,url) in l1:
	if not os.path.exists(os.path.join(pth,files_name,fname)):
		fname=os.path.join(pth,files_name,fname)
		print('开始下载：',url,'as:  ',fname)
		b = requests.get(url, stream=True,proxies=proxy)
		if b.status_code ==200:
			with open(fname, 'wb') as f:
				for chunk in b:
					f.write(chunk)
	else:
		print('已下载')
		pass
getearth.synthesis(SCALE=SCALE,date=str_date)