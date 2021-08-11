# -*- coding: utf-8 -*-
# test.py
# @author LxEgotist
# @description 
# @created 2020-11-09T17:16:26.263Z+08:00
# @last-modified 2020-11-22T16:55:07.396Z+08:00
#

from nonebot.permission import SUPERUSER
from nonebot.adapters.cqhttp import Bot, Event
from nonebot.plugin import on_command
import time,os
from nonebot.rule import to_me,Rule
from pathlib import Path
from datetime import datetime
from utils.meme import ImgText
#rule=Rule(to_me())
test = on_command('test',permission=SUPERUSER)
@test.handle()
async def _(bot: Bot, event: Event, state: dict) -> None:
	'''
	/meme 类型 内容
	'''
	tmp_path=Path('LxBot')/'data'/'data_Temp'/'img'
	data_path=Path('LxBot')/'data'/'meme'
	msg = str(event.message).strip().split(' ')
	_type,text=msg[0],msg[1]
	img=ImgText(data_path/'img'/f'{_type}',text,str(data_path/'font'/f'{_type}.ttf'))
	img_path=img.draw_text(tmp_path)
	print(img_path)
	await test.finish(f'[CQ:image,file={os.path.abspath(img_path)}]')

	pass