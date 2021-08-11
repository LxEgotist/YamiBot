# -*- coding: utf-8 -*-
# __init__.py
# @author LxEgotist
# @description 
# @created 2020-11-09T17:16:26.580Z+08:00
# @last-modified 2020-12-12T02:41:50.355Z+08:00
#




""" 每日早安插件
"""
from nonebot import logger, on_metaevent, scheduler
from nonebot.typing import Bot, Event
from pathlib import Path
from utils.helpers import get_first_bot
from .config import config
from .data import get_first_connect_message, get_moring_message
from utils.getSentence import getSentence
import json,os
from datetime import datetime
def check_first_connect(bot: Bot, event: Event, state: dict) -> bool:
	if event.sub_type == 'connect':
		return True
	return False


morning_metaevent = on_metaevent(rule=check_first_connect, block=True)
@morning_metaevent.handle()
async def _(bot: Bot, event: Event, state: dict):
	""" 启动时发送问好信息 """
	hello_str = get_first_connect_message()
	for group_id in config.group_id:
		await bot.send_msg(
			message_type='group', group_id=group_id, message=hello_str
		)
	logger.info('发送首次启动的问好信息')


@scheduler.scheduled_job(
	'cron',
	hour=config.morning_hour,
	minute=config.morning_minute,
	second=config.morning_second,
	id='morning'
)
async def _():
	""" 早安
	"""
	s=''
	for group_id in config.group_id:
		hello_str = await get_moring_message()
		await get_first_bot().send_msg(
			message_type='group',
			group_id=group_id,
			message=hello_str+s,
		)
	pth=Path(".")/"LxBot"/"data"
	with open(os.path.join(pth,"nmsl.json"),"w") as f:
		json.dump({"test":0},f)
	with open(os.path.join(pth,"detpr.json"),"w") as f:
		json.dump({"test":0},f)
	logger.info('发送早安信息')