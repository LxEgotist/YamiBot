#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
'''
Descripttion: 
version: 
Author: LxEgotist
Date: 2020-11-06 23:34:50
LastEditors: LxEgotist
LastEditTime: 2020-11-08 22:45:54
'''

import nonebot,requests,random,json
from nonebot import on_command
from nonebot.rule import to_me
from nonebot.adapters.cqhttp import Bot, Event
from pathlib import Path
url="http://api.heerdev.top/nemusic/random"

detpr=on_command("detpr")
@detpr.handle()
async def _(bot: Bot, event: Event, state: dict) -> None:
	user_id=str(event.user_id)
	data_pth=Path(".")/Path(".")/"LxBot"/"data"/"detpr.json"
	with open(data_pth,'r') as f:
		js=json.load(f)
	if user_id in js.keys():
		js[user_id]+=1
	else:
		js[user_id]=1
	with open(data_pth,'w') as f:
		json.dump(js,f)
	if js[user_id]==3:
		await detpr.finish("是想让我安~慰~你一下嘛~？")
	elif js[user_id]==6:
		await detpr.finish("如果心里感到难受就快去滚睡觉嗷！")
	elif js[user_id]>10:
		await detpr.finish("那我建议直接埋了嗷")
	else:
		try:
			js=json.loads(requests.get(url=url,timeout=5).text)
			msg0=js["text"]
			await detpr.finish(msg0)
		except requests.exceptions.ConnectTimeout as e:
			msg0 = str(e.args)
			await detpr.finish(msg0)
		except requests.exceptions.ReadTimeout as e:
			msg0 = str(e.args)
			await detpr.finish(msg0)