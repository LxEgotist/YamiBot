'''
Descripttion: 
version: 
Author: LxEgotist
Date: 2020-11-06 14:03:45
LastEditors: LxEgotist
LastEditTime: 2020-11-06 14:09:37
'''
from nonebot.plugin import on_command,on_message
from nonebot.permission import SUPERUSER
from nonebot.adapters.cqhttp import Bot, Event
from pathlib import Path
import json,os,time
from datetime import datetime
work_place = Path('.') / 'LxBot' / 'data' 

async def check_wordcloud_group(bot: Bot, event: Event, state: dict) -> bool:
	with open(os.path.join(work_place,'wordcloud',"wordcloud_group.json"),'r') as f:
		js=json.load(f)
	if str(event.group_id) in js['list']:
		return True
	else:
		return False
	
async def check_cosplay_user(bot: Bot, event: Event, state: dict) -> bool:
	file=os.path.join(work_place,"cosplay_user.json")
	if not os.path.exists(file):
		with open(file,'w') as f:
			json.dump({"user":""},f)
		js={"user":""}
	else:
		with open(file,'r') as f:
			js=json.load(f)
	if str(event.user_id)==js["user"]:
		return True
	else:
		return False