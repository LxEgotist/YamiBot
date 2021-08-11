from nonebot import on_command
from nonebot.typing import Bot, Event
import os

help = on_command('help', aliases={'帮助'}, block=True)
@help.handle()
async def _(bot: Bot, event: Event, state: dict):
	await help.finish(f'[CQ:image,file={os.path.abspath("help.png")}]\n有一切问题请使用/report上报')
	
report = on_command('report', block=True)
@report.handle()
async def _(bot: Bot, event: Event, state: dict):
	msg = str(event.message)
	await bot.send_private_msg(user_id=838167348,message=f'{event.user_id} from {event.group_id}')
	await bot.send_private_msg(user_id=838167348,message=msg)

