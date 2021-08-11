'''
Descripttion: 
version: 
Author: LxEgotist
Date: 2020-11-06 12:49:07
LastEditors: LxEgotist
LastEditTime: 2020-11-06 14:05:40
'''
from nonebot import get_bots
from nonebot.typing import Bot, Event
import random
def refuse(user_id,at=False) -> str:
	msg0=''
	if at:
		msg0=f"[CQ:at,qq={user_id}]"
	msg0 += random.choice([
		"宁不配嗷",
		"建议向[CQ:at,qq=838167348]问问宁配不配嗷",
		"权限不足",
		"要不要求求我给你权限呐",
		"肥肠抱歉,宁不配呐",
	]
	)
	return msg0
