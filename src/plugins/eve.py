from nonebot import on_command
from nonebot.typing import Bot, Event
import os
from pathlib import Path
from utils.eve import get_data
import xmltodict,json,requests
from utils.utils_img import compress_image, aio_download_pics
eve = on_command('eve')
@eve.handle()
async def _(bot: Bot, event: Event, state: dict):
	help_doc='/eve 物品名 星域名(可选) 查询价格\n/minerals查询吉他市场基础矿物的收购最高价\nquicklook 订单查询(未实装)'
	msg = str(event.message).strip().split(' ')
	if msg == ['']:
		await eve.finish(help_doc)
	elif len(msg) == 1:
		data=get_data(msg[0])
	elif len(msg) == 2:
		data=get_data(msg[0],msg[1])
	if data[0] == -1:
		await eve.finish("未知星域")
	elif data[0] == -2:
		await eve.finish("未查询到物品")
	buy=data[0]['buy']
	sell=data[0]['sell']
	if data[2]=="":
		data[2]="all"
	await eve.send(f"正在查询星域{data[2]}中的{data[1]}")
	msg0=f"需求量:{buy['volume']}\n"
	msg0+=f"最高价:{buy['max']} 最低价:{buy['min']}\n"
	msg0+=f"出售总量:{sell['volume']}\n"
	msg0+=f"最高价:{sell['max']} 最低价:{sell['min']}\n"
	await eve.finish(msg0)
#--------矿物价格
minerals= on_command('minerals')
@minerals.handle()
async def _(bot: Bot, event: Event, state: dict):
	try:
		text=requests.get('https://www.ceve-market.org/api/evemon').text
		data=xmltodict.parse(text,encoding='utf-8')["minerals"]["mineral"]
	except:
		await minerals.finish('发生了奇怪的错误,请用/report向管理汇报')
	msg0='以下是基础矿物吉他收购价格\n'
	for d in data:
		msg0+="{0:10}\t{1:<10}\n".format(d['name'].strip(),d['price'].strip(),'　')
	await minerals.finish(msg0)
#--------订单信息
quicklook=on_command('quicklook')
@quicklook.handle()
async def _(bot: Bot, event: Event, state: dict):
	msg = str(event.message).strip().split(' ')
	if msg == ['']:
		await quicklook.finish('/quicklook sell/buy 物品名 星域名来查询订单信息')
	pass
#-------安全地图
safemap=on_command('safemap')
async def _(bot: Bot, event: Event, state: dict):
	safemap_url='https://www.ceve-market.org/dumps/safemap/last.png'
	await safemap.finish('[CQ:image,file=file:///{compress_image(await aio_download_pics(safemap_url))}]')	
	
