#!/usr/bin/env python
# -*- coding: utf-8 -*- nmsl.py
# -*- coding: utf-8 -*- @author LxEgotist
# -*- coding: utf-8 -*- @description 
# -*- coding: utf-8 -*- @created 2020-11-09T17:16:26.005Z+08:00
# -*- coding: utf-8 -*- @last-modified 2020-11-09T18:41:54.965Z+08:00
#


import nonebot,requests,random,json
from nonebot import on_command
from nonebot.rule import to_me
from nonebot.adapters.cqhttp import Bot, Event
from pathlib import Path
url="https://nmsl.shadiao.app/api.php?level=min&lang=zh_cn"

nmsl=on_command("nmsl")
@nmsl.handle()
async def _(bot: Bot, event: Event, state: dict) -> None:
	user_id=str(event.user_id)
	data_pth=Path(".")/Path(".")/"LxBot"/"data"/"nmsl.json"
	with open(data_pth,'r') as f:
		js=json.load(f)
	if user_id in js.keys():
		js[user_id]+=1
	else:
		js[user_id]=1
	with open(data_pth,'w') as f:
		json.dump(js,f)
	if js[user_id]==3:
		await nmsl.finish("不是？？你这么想被嘴臭的嘛？？你他妈的是抖M吧！")
	elif js[user_id]==6:
		await nmsl.finish("给我适可而止啊喂!")
	elif js[user_id]>10:
		await nmsl.finish("懒得理你 爬")
	else:
		msg0=requests.get(url=url,timeout=5).text
		await nmsl.finish(msg0)