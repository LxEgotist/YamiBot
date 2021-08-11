# -*- coding: utf-8 -*-
# lolicon.py
# @author LxEgotist
# @description 
# @created 2020-11-09T19:12:52.718Z+08:00
# @last-modified 2021-05-20T15:12:22.817Z+08:00
#

from nonebot.plugin import on_command,on_regex
from nonebot.permission import SUPERUSER
from nonebot.adapters.cqhttp import Bot, Event
import requests,json,random,time
from utils.master import getMaster
from utils.getSentence import getSentence
import time,re
from pathlib import Path
from datetime import datetime
from utils.utils_img import compress_image, aio_download_pics
setus = on_regex(
	r"来[点丶张份副个幅][涩色瑟][图圖]|[涩色瑟][图圖]来|[涩色瑟][图圖][gkd|GKD|搞快点]|[gkd|GKD|搞快点][涩色瑟][图圖]|[涩色瑟][图圖][gkd|GKD|搞快点]|[涩色瑟][图圖]|.+?[张连]{0,1}[涩色瑟][图圖].+?[张连]{0,1}")


@setus.handle()  # type: ignore
async def _setu(bot: Bot, event: Event, state: dict) -> None:
	'''
	group = str(event.group_id)
	user  = str(event.user_id)
	if check(event.raw_message):
		await setus.finish("太.....太多了啦~会坏掉的啊啊啊啊~最...最多只能一个啦ヽ(*。>Д<)o゜")
	timeformat="%Y-%m-%d %H:%M:%S"
	now =datetime.now()
	with open(Path('.')/"LxBot"/'data'/'lolicon.json','r') as f:
		js=json.load(f)
		if group in js.keys():
			last=js[group]
		else:
			js[group]=now.strftime(timeformat)
			last=now.strftime(timeformat)
	with open(Path('.')/"LxBot"/'data'/'lolicon.json','w') as f:
		js[group]=now.strftime(timeformat)
		json.dump(js,f)
	second=(now-datetime.strptime(last,timeformat)).seconds
	if 0<second and second < 30:
		await setus.finish(f"啊啊啊~太...太快啦~暗酱受不了啦~QwQ~\n上次手冲时间{last}\n请休息30秒再冲哦")
	flag=random.randint(0,1)
	flag=0
	params = {"apikey": "796636435fa923ef36f2f4", "r18": flag , "num": "1"}
	data = {}
	res = random.randint(1, 5)
	try:
		data = json.loads(requests.get('https://api.lolicon.app/setu/', params).text)
	except Exception:
		await setus.finish("请求数据失败，也可能为接口调用次数达上限")
	msg0 = "您要的涩图:\n"
	msg0 += f'Title: {data["data"][0]["title"]}\n'
	msg0 += f'Pid: {data["data"][0]["pid"]}\n'
	if 1 <= res < 5:
		await setus.send(msg0)
		a = await bot.send_group_msg(group_id=event.group_id,message=f'[CQ:image,file=file:///{compress_image(await aio_download_pics(data["data"][0]["url"]))}]')
		if flag:
			time.sleep(1)
			await bot.delete_msg(message_id=a['message_id'],self_id=event.self_id)
			await setus.finish("略略略我撤回了,被人看到暗酱会消失的QWQ")
	elif res == 5:
		msg0="谢谢你帮master找涩图,我已经转发给他了\nο(=•ω＜=)ρ⌒☆"
		if flag:
			msg0+="\n顺便你刚刚抽中了一张r18涩图哦"
		await bot.send(event, msg0)
		for sup in getMaster():
			await bot.send_private_msg(
				user_id=sup,
				message=
				f'主人，从群{group}的{user}发来的涩图！热乎着！\nTitle: {data["data"][0]["title"]}\nPid: {data["data"][0]["pid"]}\n[CQ:image,file=file:///{compress_image(await aio_download_pics(data["data"][0]["url"]))}]'
			)
def check(msg:str)-> bool:
	pattern=re.compile(r'[\d二三四五六七八九十百千]{1,10}[张连]{0,1}[涩色瑟][图圖]|[涩色瑟][图圖][\d二三四五六七八九十百千]{1,10}[张连]{0,1}')
	if re.findall(pattern,msg):
		return True
	else:
		return False
	'''


	await setus.finish("不准色图!")