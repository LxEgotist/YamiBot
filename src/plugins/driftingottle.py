# -*- coding: utf-8 -*-
# driftingottle.py
# @author LxEgotist
# @description 
# @created 2020-11-23T20:06:59.489Z+08:00
# @last-modified 2020-11-25T22:12:35.926Z+08:00
#

import sys,os,json,random,requests
from pathlib import Path
from nonebot import on_command
from nonebot.rule import to_me
from nonebot.adapters.cqhttp import Bot, Event
import uuid
from nonebot.permission import SUPERUSER,GROUP_ADMIN,GROUP_OWNER
from aip import AipContentCensor
APP_ID ='Ki2zfTOLUKo2px62ckYUFRZV'
API_KEY='Ki2zfTOLUKo2px62ckYUFRZV'
APP_ID='23030360'
SECRET_KEY='dG4NdsWCS1ET3KZN2XzEtLDRAUkSKv93'
client = AipContentCensor(APP_ID, API_KEY, SECRET_KEY)
DRIFTING_BOTTLE_PATH = Path('.') / 'LxBot' / 'data' / 'drifting_bottle.json'
driftingBottle = on_command('发送片段')
@driftingBottle.handle()
async def _(bot: Bot, event: Event, state: dict) -> None:
	args = str(event.message).strip()

	if args:
		state['args'] = args
@driftingBottle.got('args', prompt='请输入你想沉入暗酱意识海的内容吧')
async def _(bot: Bot, event: Event, state: dict) -> None:
	args = state['args']
	user = event.user_id
	group = event.group_id
	result=client.textCensorUserDefined(args)
	if result["conclusion"]=='不合规':
		await driftingBottle.finish(result['data'][0]["msg"])
	if not DRIFTING_BOTTLE_PATH.is_file():
		with open(DRIFTING_BOTTLE_PATH, 'w') as f:
			f.write(json.dumps({}))

	with open(DRIFTING_BOTTLE_PATH, 'r') as f:
		data = json.load(f)
	num=str(uuid.uuid1()).split('-')[0]
	while num in data:
		num=str(uuid.uuid1()).split('-')[0]
	data[num] = [user, group, args]

	with open(DRIFTING_BOTTLE_PATH, 'w') as f:
		f.write(json.dumps(data))

	await driftingBottle.finish(f'已读取片段进暗酱的意识海啦,这段片段的编号是{num}')

getDriftingBottle = on_command('读取片段')
@getDriftingBottle.handle()
async def _(bot: Bot, event: Event, state: dict) -> None:
	if not DRIFTING_BOTTLE_PATH.is_file():
		with open(DRIFTING_BOTTLE_PATH, 'w') as f:
			f.write(json.dumps({}))

	with open(DRIFTING_BOTTLE_PATH, 'r') as f:
		data = json.load(f)

	l = [x for x in data]
	if not l:
		await getDriftingBottle.finish('暂无片段可读取~')

	num = random.choice(l)
	bottle = data[num]
	msg = bottle[2]

	msg0 = f'[CQ:at,qq={event.user_id}]\n'
	msg0 += f'片段[{num}]内容如下：\n'
	msg0 += msg+'\n'
	msg0 += f"by {bottle[0]} from {bottle[1]}"
	await getDriftingBottle.finish(msg0)

delDriftingBottle = on_command('删除片段',permission=SUPERUSER)
@delDriftingBottle.handle()
async def _(bot: Bot, event: Event, state: dict) -> None:
	args =str(event.message).strip().split(' ')
	if not args:
		msg0 = '*For master\n'
		msg0 += '- delall\n'
		msg0 += '- del [编号]\n'
		msg0 += 'eg: 删除片段 del [编号]'

		await delDriftingBottle.finish(msg0)

	if not DRIFTING_BOTTLE_PATH.is_file():
		with open(DRIFTING_BOTTLE_PATH, 'w') as f:
			f.write(json.dumps({}))

		await delDriftingBottle.finish('成功删除....空气(/▽＼)')

	with open(DRIFTING_BOTTLE_PATH, 'r') as f:
		data = json.load(f)
	#print(args[0])
	if args[0] == 'delall':
		os.remove(os.path.abspath(DRIFTING_BOTTLE_PATH))

	elif args[0] == 'del':
		try:
			#print(f'删除{args[1]}了哦')
			del data[args[1]]
			#print(data)
		except:
			await delDriftingBottle.finish('清除失败了...')

	with open(DRIFTING_BOTTLE_PATH, 'w') as f:
		f.write(json.dumps(data))
		f.close()

	result = args[1] if args[0] == 'del' else "ALL"
	await delDriftingBottle.finish(
		f'已删除片段[{result}]，目前还剩余[{len(data)}]条~')

checkDriftingBottle = on_command('统计片段',permission=SUPERUSER)
@checkDriftingBottle.handle()
async def _(bot: Bot, event: Event, state: dict) -> None:
	if not DRIFTING_BOTTLE_PATH.is_file():
		with open(DRIFTING_BOTTLE_PATH, 'w') as f:
			f.write(json.dumps({}))

		await checkDriftingBottle.finish('暗酱脑袋空空的\n(￣▽￣)"')

	with open(DRIFTING_BOTTLE_PATH, 'r') as f:
		data = json.load(f)
	if len(data)==0:
		await checkDriftingBottle.finish('暗酱脑袋空空的\n(￣▽￣)"')
	await checkDriftingBottle.finish(f'共有{len(data)}条片段')