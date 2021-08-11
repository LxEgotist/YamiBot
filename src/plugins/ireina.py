'''
Descripttion: 
version: 
Author: LxEgotist
Date: 2020-11-06 10:57:46
LastEditors: LxEgotist
LastEditTime: 2020-11-06 11:35:02
'''
import os
import json,sys
import random
from pathlib import Path
from nonebot.plugin import on_command
from nonebot.permission import SUPERUSER
from nonebot.adapters.cqhttp import Bot, Event
sys.path.append('/root/LxBot')
from utils.utils_error import errorRepo
from utils.utils_whiteList import whiteList
from utils.utils_banList import banList

ireina = on_command("ireina")
@ireina.handle()
async def _(bot: Bot, event: Event, state: dict) -> None:
	msg = str(event.message).strip().split(' ')
	user=str(event.user_id)
	group=str(event.group_id)

	if not banList(user,group):
		files_name= Path(".") / "ireina"
		if msg:
			if msg[0]=='meme':
				files_name=Path(".") / "ireina" / "meme"
		img_pth = os.path.abspath(Path(".") / files_name / random.choice(os.listdir(files_name)))
		print(img_pth)
		await ireina.finish(f"[CQ:image,file={img_pth}]")