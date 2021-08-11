import re,os,json
from pathlib import Path
from nonebot.plugin import on_command,on_message
from nonebot.permission import SUPERUSER
from nonebot.adapters.cqhttp import Bot, Event
from nonebot.rule import to_me,Rule
from utils.rule import check_cosplay_user


cosmsg=on_message(rule=Rule(check_cosplay_user))
@cosmsg.handle()
async def _(bot: Bot, event: Event, state: dict) -> None:
	await cosmsg.finish(event.raw_message)
	
	
cos=on_command('cos',rule=Rule(to_me()),permission=SUPERUSER)
@cos.handle()
async def _(bot: Bot, event: Event, state: dict) -> None:
	work_place = Path('.') / 'LxBot' / 'data' 
	file=work_place/'cosplay_user.json'
	msg0=event.raw_message
	msg = str(event.message).strip().split(' ')

	if msg[0]=='del':
		if os.path.exists(file):
			os.remove(file)
			await bot.set_group_card(group_id=event.group_id,user_id=1393937441,card="暗酱")
			await cos.finish('我变回暗酱咯(๑＞ڡ＜)☆ ')
	else:
		pattern=re.compile('cos \[CQ:at,qq=(\d+?)\]')
		user_id=re.search(pattern,msg0).group(1)
		card=await bot.get_group_member_info(group_id=event.group_id,user_id=int(user_id))
		card=card["card"]
		await bot.set_group_card(group_id=event.group_id,user_id=1393937441,card=card)
		with open(file,'w') as f:
			json.dump({"user":user_id},f)
		await cos.finish(f'我现在是[CQ:at,qq={user_id}]啦')
	pass