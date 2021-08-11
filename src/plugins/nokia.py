from nonebot import on_command
from nonebot.typing import Bot, Event
import os
from pathlib import Path
from utils.nokia import generate_image
nokia = on_command('nokia')
@nokia.handle()
async def _(bot: Bot, event: Event, state: dict):
	msg=str(event.message)
	tmp_img=Path('.')/'LxBot'/'data'/'data_Temp'/'img'
	img_path=generate_image(msg,tmp_img)
	await nokia.finish(f'[CQ:image,file=file:///{img_path}]')