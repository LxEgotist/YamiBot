import sys
import nonebot,os
from .getearth import getEarth
import requests,json,os
from datetime import datetime
from nonebot import on_command
from nonebot.rule import to_me
from nonebot.adapters.cqhttp import Bot, Event
from PIL import ImageFile,Image
ImageFile.LOAD_TRUNCATED_IMAGES = True
msg='[CQ:image,file=%s]'
origin_pth='/root/plugins/image'
earth = on_command("getearth", priority=1)
proxy={"https":"https://127.0.0.1:7890","http":"http://127.0.0.1:7890"}
@earth.handle()
async def handle_earth(bot: Bot, event: Event, state: dict):
	try:
		await earth.send('该调用耗时巨tm久，别瞎j8一直调用')
	except:
		pass
#	try:
	args = str(event.message).strip().split()
	if args:
		SCALE=int(args[0])
		if int(args[0])==3:
			SCALE=4
		if int(args[0])>3:
			SCALE=1
	else:
		SCALE=1
#	except:
#		await earth.send('nmsl')
	l1,str_date=getEarth(SCALE=SCALE)
	date=datetime.strptime(str_date, '%Y-%m-%d %H:%M:%S')
	msg0="UTC {}\nSIZE:{}*{}".format(date.strftime('%Y-%m-%d %H:%M:%S'),SCALE*550,SCALE*550)
	files_name=date.strftime('%Y%m%d%H%M%S')
	pth='{}d'.format(SCALE)
	if not os.path.exists(os.path.join(origin_pth,pth)):
		os.mkdir(os.path.join(origin_pth,pth))
	if not os.path.exists(os.path.join(origin_pth,pth,files_name)):
		os.mkdir(os.path.join(origin_pth,pth,files_name))
	for (fname,url) in l1:
		if not os.path.exists(os.path.join(origin_pth,pth,files_name,fname)):
			fname=os.path.join(origin_pth,pth,files_name,fname)
			print('开始下载：',url,'as:  ',fname)
			try:
				b = requests.get(url,proxies=proxy,timeout=20)
			except requests.exceptions.ProxyError:
				await earth.finish("代理错误")
			if b.status_code ==200:
				with open(fname, 'wb') as f:
					f.write(b.content)
					print('下载完成',fname)
			else:
				print(b.status_code)
		else:
			print('已下载',fname)
			pass
	#合成图片
	filename_format='{}_{}_{}.png'
	pth='{}d'.format(SCALE)
	files_name=date.strftime('%Y%m%d%H%M%S')
	png = Image.new('RGB', (550 * SCALE, 550 * SCALE))
	for x in range(SCALE):
		for y in range(SCALE):
			fname=os.path.join(origin_pth,pth,files_name,filename_format.format(date.strftime("%H%M%S"), x, y))
			try:
				img = Image.open(fname)
				png.paste(img, (550 * x, 550 * y, 550 * (x + 1), 550 * (y + 1)))
			except FileNotFoundError:
				await earth.send(fname+"缺失")
	png.save(os.path.join(origin_pth,pth,files_name,'earth.png'),'PNG')
	earth_pth=os.path.join(pth,files_name,'earth.png')
	message=msg % earth_pth
	await earth.send(msg0)
	await earth.finish(message)
