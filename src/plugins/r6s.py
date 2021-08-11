# -*- coding: utf-8 -*-
# r6s.py
# @author LxEgotist
# @description 
# @created 2020-11-11T23:00:19.375Z+08:00
# @last-modified 2020-11-12T01:44:34.188Z+08:00
#

from pathlib import Path
from nonebot.plugin import on_command
from nonebot.adapters.cqhttp import Bot, Event
from utils.utils_img import compress_image, aio_download_pics
import json,requests,cairosvg,os
data_place=Path('/root/LxBot')/"LxBot"/"data"/"r6s"
token="6131ccb4-efb0-4a03-82d9-9429fe61ebc5"
headers={"Authorization": f"Bearer {token}"}
with open(data_place/"weapon.json",'r') as f:
	js=json.load(f)
with open(data_place/"operators.json",'r') as f:
	operators_name=json.load(f)
current_season='shadow_legacy'
categories={
	"突击步枪":"Assault Rifle",
	"步枪":"Assault Rifle",
	"冲锋枪":"Submachine Gun",
	"轻机枪":"Light Machine Gun",
	"半自动步枪":"Marksman Rifle",
	"神射手步枪":"Marksman Rifle",
	"手枪":"Handgun",
	"霰弹枪":"Shotgun",
	"喷子":"Shotgun",
	"机枪":"Machine Pistol",
}
async def download_svg_as_png(img_url:str) -> str:
	fname=img_url.split('/')[-1][:-4]
	with open(data_place/"svgs"/f"{fname}.svg",'wb') as f:
		f.write(requests.get(img_url).content)
	file_pth=str(data_place/"imgs"/f"{fname}.png")
	cairosvg.svg2png(url=str(data_place/"svgs"/f"{fname}.svg"),write_to=file_pth)
	return file_pth
#data={"username":"LxEgotist","platform":"pc","type":"generic"}
#url.format(**data)
async def built_msg(arg:str,_type:str,data:dict) -> str:
	if arg == "generic":
		general=data["stats"]["general"]
		msg0=f"Player:{data['username']} Lv{data['progression']['level']} General\n"
		msg0+=f"Alpha Pack:{data['progression']['lootbox_probability']}%\n"
		msg0+=f'K:{general["kills"]} D:{general["deaths"]} A:{general["assists"]}\n'
		msg0+=f'K/D:{general["kd"]}\n'
		msg0+=f'W:{general["wins"]} L:{general["losses"]} W/L:{general["wl"]}\n'
		msg0+=f'Headshots:{general["headshots"]}\n'
		msg0+=f'Melee Kills:{general["melee_kills"]}\n'
		msg0+=f'自杀:{general["suicides"]}'
		return msg0
	elif _type == "rank":
		rank=data["stats"]["queue"]["ranked"]
		msg0=f"Player:{data['username']} Lv{data['progression']['level']} Rank\n"
		msg0+=f'K:{rank["kills"]} D:{rank["deaths"]} K/D:{rank["kd"]}\n'
		msg0+=f'W:{rank["wins"]} L:{rank["losses"]} W/L:{rank["wl"]}\n'
		return msg0
	elif arg == 'mmr':
		rank_data={}
		await r6s.send(f'当前赛季:{current_season}\n users:{data["username"]}:')
		regions=data['seasons'][current_season]['regions']
		for region in regions:
			rank_data[region]={
				'rank_text':regions[region][0]['rank_text'],
				'mmr':regions[region][0]['mmr'],
				'rank_image':regions[region][0]['rank_image']
			}
		imgs_pth=data_place/'imgs'
		for k in rank_data:
			img_url=rank_data[k]['rank_image']
			fname=img_url.split('/')[-1][:-4]+'.png'
			if not os.path.exists(imgs_pth/fname):
				await download_svg_as_png(img_url)
		msg0=''
		for k in rank_data:
			fname=rank_data[k]['rank_image'].split('/')[-1][:-4]+'.png'
			print(fname)
			fname=imgs_pth/fname
			print(fname)
			msg0+= f'{k}:{rank_data[k]["mmr"]} {rank_data[k]["rank_text"]}[CQ:image,file={fname}]'
		print(msg0)
		return msg0
		
		
		
	elif arg in ["Assault Rifle","Submachine Gun","Light Machine Gun","Marksman Rifle","Handgun","Shotgun","Machine Pistol"]:
		general=data["categories"]
		msg0=f"Player:{data['username']} {_type}\n"
		for d in general:
			if _type == d["category"]:
				data=d
		msg0+=f'K:{data["kills"]} D:{data["deaths"]} K/D:{data["kd"]}\n'

		msg0+=f'Headshots:{data["headshots"]} percentage:{data["headshot_percentage"]}'
		return msg0
	elif _type == 'weapons':
		msg0=f"Player:{data['username']}\n"
		for d in js:
			#try:
			if arg.lower()==d["name"].lower():
				msg0+=f'[CQ:image,file=file:///{compress_image(await aio_download_pics(d["image"]))}]\n'
				#msg0+=f'{d["image"]}\n'		
				data=data["weapons"]
				for d in data:
					if arg.lower()==d["weapon"].lower():
						data=d
				msg0+=f'{data["category"]}:{data["weapon"]}\n'
				msg0+=f'K:{data["kills"]} D:{data["deaths"]} K/D:{data["kd"]}\n'
				msg0+=f'Headshots:{data["headshots"]} percentage:{data["headshot_percentage"]}'
				return msg0
			'''
			except Exception as e:
				print(e)
				return '你猜猜发生了什么错误？'
			'''
				
	elif _type=="operators":
		for d in data['operators']:
			if arg==d["name"].lower():
				break
		msg0=f'[CQ:image,file=file:///{compress_image(await aio_download_pics(d["badge_image"]))}]\n'
		msg0+=f"Player:{data['username']}\n"
		msg0+=f"{d['role']} {d['name']}[{d['ctu']}]\n"
		msg0+=f'K:{d["kills"]} D:{d["deaths"]} K/D:{d["kd"]}\n'
		msg0+=f'W:{d["wins"]} L:{d["losses"]} W/L:{d["wl"]}\n'
		msg0+=f'Headshots:{d["headshots"]} '
		msg0+=f"MeleeKill:{d['melee_kills']}"
		return msg0
		pass
	else:
		return "Error"

r6s = on_command('r6s',priority=5)
@r6s.handle()
async def _(bot: Bot, event: Event, state: dict) -> None:
	url="https://api2.r6stats.com/public-api/stats/{username}/{platform}/{_type}"
	msg = str(event.message).strip().split(' ')
	if len(msg) <= 1:
		msg0="R6S数据查询\n"
		msg0+="/r6s [username] [platform] [type]\n"
		msg0+="type(可选参数):武器类型(喷子 步枪等) 具体武器(自己猜名字) rank(排位数据) generic(总览) mmr(排位情况)"
		await r6s.finish(msg0)
	if len(msg) == 2:
		param={
		"username":msg[0],
		"platform":msg[1].lower(),
		"_type":"generic"
		}
	elif len(msg) >= 3:
		param={
		"username":msg[0],
		"platform":msg[1].lower(),
		"_type":" ".join(msg[2:])
		}
		arg=" ".join(msg[2:])
	else:
		await r6s.finish("请检查格式嗷~")
	#print(param)
	if not param['platform'] in ['ps4','xbox','pc']:
		await r6s.finish("请检查格式嗷~(不会有人不知道r6平台有xbox pc和ps4吧)")
	if param['_type'] in ["Assault Rifle","Submachine Gun","Light Machine Gun","Marksman Rifle","Handgun","Shotgun","Machine Pistol","步枪","冲锋枪","轻机枪","半自动步枪","手枪","霰弹枪","机枪","喷子","神射手步枪"]:
		param['_type']="weapon-categories"
		try:
			arg=categories[arg]
		except:
			r6s.finish("请检查参数嗷")
	elif param['_type'] in ["generic","rank"]:
		param['_type'] = "generic"
		arg='generic'
	elif param['_type'].lower()=='mmr':
		param['_type']='seasonal'
		arg='mmr'
	else:
		arg,param['_type'] = check_arg(param['_type'])
	if arg=="-1":
		r6s.finish("你查的是什么j8东西")
	url=url.format(**param)
	html=requests.get(url,headers=headers,timeout=10)
	data=json.loads(html.text)
	print(url)
	#print(json.dumps(data,indent=2))
	try:
		if data['status']=='error':
			await r6s.finish(data['error'])
	except:pass
	
	await r6s.finish(await built_msg(arg,param['_type'],data))

def check_arg(arg:str) -> (str,str):
	'''
	查询传入的参数是个什么j8东西
	干员名: ("干员名","operators")
	武器名: ("武器名","weapons")
	都不是: ("-1","-1")
	'''
	op_file=data_place/"operators.json"
	wp_file=data_place/"weapon.json"
	with open(op_file,'r') as f :
		operators=json.load(f)
	with open(wp_file,'r') as f :
		weapons=json.load(f)
	for x in weapons:
		if x["name"].lower()==arg.lower():
			return (x["name"],"weapons")
	for x in operators:
		#print(x["name"])
		if arg in x["nickname"]:
			#print("="*10,x,"="*10)
			return (x["name"],"operators")
	else:
		return "-1","-1"


r6ss = on_command('r6-weapon',priority=5)
@r6ss.handle()
async def _(bot: Bot, event: Event, state: dict) -> None:
	args = str(event.message).strip()
	if args in ["Assault Rifle","Submachine Gun","Light Machine Gun","Marksman Rifle","Handgun","Shotgun","Machine Pistol","步枪","冲锋枪","轻机枪","半自动步枪","手枪","霰弹枪","机枪","喷子","神射手步枪",'help']:
		state['type']=args
		
	
	
@r6ss.got("type",prompt="你要搜啥类型的武器嘞")
async def handle(bot: Bot, event: Event, state: dict):
	_type=state['type']
	pa={
	"突击步枪":["assault"],
	"步枪":["assault"],
	"冲锋枪":["smg"],
	"轻机枪":["lmg"],
	"半自动步枪":["marksman"],
	"神射手步枪":["marksman"],
	"精确手步枪":["marksman"],
	"手枪":["pistol","mp"],
	"霰弹枪":["shotgun"],
	"喷子":["shotgun"],
	"机枪":["Machine Pistol"],
	}
	if _type=='help':
		await r6ss.finish('没想到吧我没写帮助XD')
	else :
		arg=state['type']
		if _type in ["Assault Rifle","Submachine Gun","Light Machine Gun","Marksman Rifle","Handgun","Shotgun","Machine Pistol","步枪","冲锋枪","轻机枪","半自动步枪","手枪","霰弹枪","机枪","喷子","神射手步枪"]:
			msg0=""
			arg=pa[arg]
			for i in js:
				if i['category'] in arg:
					msg0+= f'{i["name"]}\n'
			await r6ss.finish(msg0)
		else:
			await r6ss.finish('?')

