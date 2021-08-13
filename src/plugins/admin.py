import json
from pathlib import Path
from utils.utils_error import errorRepo
from utils.utils_whiteList import whiteList
from utils.utils_banList import banList
from nonebot.plugin import on_command,on_request,on_regex
from nonebot.adapters.cqhttp import Bot, Event
from nonebot.permission import SUPERUSER,GROUP_ADMIN,GROUP_OWNER
master = ["838167348"]
whiteListcheck = on_command('whiteList-check', permission=SUPERUSER)
@whiteListcheck.handle() # type: ignore
async def _(bot: Bot, event: Event, state: dict) -> None:
	msg = str(event.message).strip().split(' ')
	if msg[0]=='user':
		if whiteList(user=msg[1]):
			await whiteListcheck.finish('True')
		else:
			await whiteListcheck.finish('False')
	if msg[0]=='group':
		if whiteList(group=msg[1]):
			await whiteListcheck.finish('True')
		else:
			await whiteListcheck.finish('False')

setWhiteList = on_command('whiteList-set', permission=SUPERUSER)
@setWhiteList.handle() # type: ignore
async def _(bot: Bot, event: Event, state: dict) -> None:
	msg = str(event.message).strip().split(' ')
	if len(msg)<2:
		await setWhiteList.finish('你在输什么j8')
	else:
		
		mo=msg[0]
		number=msg[1]
		file=Path('.') / 'utils' /'utils_whiteList' / f'whiteList_{mo}.json'
		#print(file)
		j=json.load(open(file,'r'))
		j['list'].append(number)
		j['list']=list(set(j['list']))
		with open(file,'w') as f:
			json.dump(j,f)
		await setWhiteList.finish(f'{mo}:{number}加入白名单')

settmpWhiteList = on_command('whiteList-once', permission=SUPERUSER)
@settmpWhiteList.handle() # type: ignore
async def _(bot: Bot, event: Event, state: dict) -> None:
	msg = str(event.message).strip().split(' ')
	if len(msg)<2:
		await settmpWhiteList.finish('你在输什么j8')
	elif msg[0]=='user':
		mo=msg[0]
		if msg[1]!='all':
			number=msg[1]
		else:
			m=[]
			l=await bot.get_group_member_list()
			for i in l:
				m.append(i['user_id'])
		file=Path('.') / 'utils' /'utils_whiteList' / f'whiteList_{mo}.json'
		#print(file)
		j=json.load(open(file,'r'))
		if msg[1]=='all':
			j['tmp']+=m
			await settmpWhiteList.finish(f'群{event.group_id}的每个lsp现在都有一次ghs的机会了呢')
		else:
			j['tmp'].append(number)
			await settmpWhiteList.finish(f'[CQ:at,qq={number}]加入白名单,只有一次挥霍的机会哦')
		j['tmp']=list(set(j['tmp']))
		
		with open(file,'w') as f:
			json.dump(j,f)


delWhiteList = on_command('whiteList-del', permission=SUPERUSER)
@delWhiteList.handle() # type: ignore
async def _(bot: Bot, event: Event, state: dict) -> None:
	msg = str(event.message).strip().split(' ')
	if len(msg)<2:
		await delWhiteList.finish('你在输什么j8')
	else:
		mo=msg[0]
		number=msg[1]
		file=Path('.') / 'utils' /'utils_whiteList' / f'whiteList_{mo}.json'
		#print(file)
		j=json.load(open(file,'r'))
		j['list'].remove(number)
		j['list']=list(set(j['list']))
		with open(file,'w') as f:
			json.dump(j,f)
		await delWhiteList.finish(f'{mo}:{number}移出白名单')
		#await delWhiteList.finish(f'{mo}:{number}移出白名单失败')

banListcheck = on_command('banList-check', permission=SUPERUSER)
@banListcheck.handle() # type: ignore
async def _(bot: Bot, event: Event, state: dict) -> None:
	msg = str(event.message).strip().split(' ')
	if msg[0]=='user':
		if banList(user=msg[1]):
			await banListcheck.finish('True')
		else:
			await banListcheck.finish('False')
	if msg[0]=='group':
		if banList(group=msg[1]):
			await banListcheck.finish('True')
		else:
			await banListcheck.finish('False')

setWhiteList = on_command('banList-set', permission=SUPERUSER)
@setWhiteList.handle() # type: ignore
async def _(bot: Bot, event: Event, state: dict) -> None:
	msg = str(event.message).strip().split(' ')
	if len(msg)<2:
		await setWhiteList.finish('你在输什么j8')
	else:
		mo=msg[0]
		number=msg[1]
		file=Path('.') / 'utils' /'utils_banList' / f'banList_{mo}.json'
		#print(file)
		j=json.load(open(file,'r'))
		j['list'].append(number)
		j['list']=list(set(j['list']))
		with open(file,'w') as f:
			json.dump(j,f)
		await setWhiteList.finish(f'{mo}:{number}加入黑名单')


delWhiteList = on_command('banList-del', permission=SUPERUSER)
@delWhiteList.handle() # type: ignore
async def _(bot: Bot, event: Event, state: dict) -> None:
	msg = str(event.message).strip().split(' ')
	if len(msg)<2:
		await delWhiteList.finish('你在输什么j8')
	else:
		mo=msg[0]
		number=msg[1]
		file=Path('.') / 'utils' /'utils_banList' / f'banList_{mo}.json'
		#print(file)
		j=json.load(open(file,'r'))
		j['list'].remove(number)
		j['list']=list(set(j['list']))
		with open(file,'w') as f:
			json.dump(j,f)
		await delWhiteList.finish(f'{mo}:{number}移出黑名单')
		#await delWhiteList.finish(f'{mo}:{number}移出黑名单失败')


banLists = on_regex(
	r"/((b|B)an(l|L)ist|(b|B)lack(l|L)ist|(w|W)hite(l|L)ist)-help")
@banLists.handle()  # type: ignore
async def _(bot: Bot, event: Event, state: dict) -> None:
	msg = "-==WhiteList==-\n"
	msg += " - /whiteList-check [mo] [number]\n"
	msg += " - /whiteList-set [mo] [number]\n"
	msg += " - /whiteList-once [mo] [number]\n"
	msg += " - /whiteList-del [mo] [number]"
	await banLists.finish(msg)
	msg = "-==BanList==-\n"
	msg += " - /banList-check [mo] [number]\n"
	msg += " - /banList-set [mo] [number]\n"
	msg += " - /banList-del [mo] [number]"
	await banLists.finish(msg)
	msg = "  [mo] :	user/group\n"
	msg += "  [number] :	user ID/group ID"
	await banLists.finish(msg)


morningSet = on_command("morning",permission=(SUPERUSER | GROUP_OWNER | GROUP_ADMIN))
@morningSet.handle()
async def _(bot: Bot, event: Event, state: dict) -> None:
	group_id=str(event.group_id)
	data_pth=Path('.')/'LxBot'/'data'
	msg = str(event.message).strip().split(' ')
	if msg[0] in ['add','del','set']:
		if msg[0] in ['add','set']:
			with open(data_pth/"morning.json",'r') as f:
				js=json.load(f)
				if js.keys():
					print(len(js.keys()))
					pass
				else:
					print(js.keys())
					js["list"]=[]
			print(js)
			js["list"].append(group_id)
			js["list"]=list(set(js["list"]))
			with open(data_pth/"morning.json",'w') as f:
				json.dump(js,f)
			await morningSet.finish("每日叫床服务已开启o(*////▽////*)q")
		if msg[0] in ['del']:
			with open(data_pth/"morning.json",'r') as f:
				js=json.load(f)
				if js.keys():
					if group_id in js["list"]:
						js["list"].remove(group_id)
						js["list"]=list(set(js["list"]))
					else:
						await morningSet.finish('未开启叫床服务＞﹏＜')
			with open(data_pth/"morning.json",'w') as f:
				json.dump(js,f)
			await morningSet.finish("嘤嘤嘤QWQ")
		if msg[0] == "check":
			with open(data_pth/"morning.json",'r') as f:
				js=json.load(f)
				if js.keys():
					if group_id in js["list"]:
						await morningSet.finish("每日叫床服务已开启o(*////▽////*)q")
				await morningSet.finish('未开启叫床服务＞﹏＜')

#处理加群/好友(只设置了前者)请求
selfEvent = on_request()
@selfEvent.handle()  # type: ignore
async def _(bot: Bot, event: Event, state: dict) -> None:
	print(event.raw_event)
	GROUP_INVITE = 0
	flag = event.raw_event['flag']
	req_type = event.raw_event['request_type']
	if req_type == 'group' and event.raw_event['sub_type'] == 'invite':
		for sup in master:
			msg0 = '主人，收到一条群邀请：\n'
			msg0 += f"邀请人：{event.raw_event['user_id']}\n"
			msg0 += f"目标群：{event.raw_event['group_id']}\n"

			if GROUP_INVITE == 0:
				msg0 += '由于master未允许添加群聊，已回拒'
				await bot.set_group_add_request(
					flag=flag,
					sub_type=event.raw_event['sub_type'],
					approve=False,
					reason=f'ねね..ごんめね...\n主人不允许咱添加其他群聊...\n如需寻求帮助，请联系master：{sup}'
				)

			else:
				msg0 += 'master设置了同意加群,已入群'
				await bot.set_group_add_request(
					flag=flag,
					sub_type=event.raw_event['sub_type'],
					approve=True)
			await bot.send_private_msg(user_id=sup, message=msg0)