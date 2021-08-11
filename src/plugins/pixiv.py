#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
'''
Descripttion: 
version: 
Author: LxEgotist
Date: 2020-11-04 12:01:22
LastEditors: LxEgotist
LastEditTime: 2020-11-09 16:40:33
'''


import os,time,re
import json,sys,requests
import sqlite3,random
from ast import literal_eval
from pathlib import Path
from nonebot.plugin import on_command
from nonebot.permission import SUPERUSER
from nonebot.adapters.cqhttp import Bot, Event
sys.path.append('/root/LxBot')
from utils.utils_error import errorRepo
from utils.utils_whiteList import whiteList
from utils.utils_banList import banList
from utils.refuse import refuse

def checkImages(img_url) -> int:
	'''
	检查pid是否为图集
	返回值 (flag,msg)
	flag=1/0 
	flag返回 0 则msg为str 异常信息
	flag返回 1 则msg为int 图片数目
	'''
	try:
		html=requests.head(img_url)
	except requests.exceptions.ConnectTimeout as e:
		msg0 = str(e.args)
		return 0,msg0
	except requests.exceptions.ReadTimeout as e:
		msg0 = str(e.args)
		return 0,msg0
	if html.status_code==404:
		html=requests.get(img_url)
		return 1,int(re.search(r"這個作品ID中有 (?P<sums>\d+) 張圖片",html.text).group("sums"))
	else:
		return 1,1
	


SetuData = on_command('setu', priority=5)
@SetuData.handle() # type: ignore
async def _(bot: Bot, event: Event, state: dict) -> None:
	msg0 = "-==暗酱的涩图库==-\n"
	msg0 += "上传(通过pid):\n"
	msg0 += " - /setu-upload [pid]\n"
	msg0 += "Delete:\n"
	msg0 += " - /setu-delete [type] [pid]\n"
	msg0 += " * type: normal r18,r18g\n"
	await SetuData.send(msg0)
	msg0 = "get图片:\n"
	msg0 += " - /setu-get [type] [arg1] [arg2]\n"
	msg0 += " * type: normal,r18,r18g\n"
	msg0 += " arg1				arg2\n"
	msg0 += "|---tags   :  标签1,标签2... \n"
	msg0 += "|---pid	:  pid \n"
	msg0 += "|---title  :  标题 \n"
	msg0 += "|---name   :  画师名		  \n"
	msg0 += "|---random :   空			  \n"
	await SetuData.send(msg0)
	msg0 = "随机返回标签/画师/pid/标题:\n"
	msg0 += " - /setu-gettag [type] [arg]\n"
	msg0 += " * type: normal r18,r18g\n"
	msg0 += " * arg : tags/name/pid/title\n"
	await SetuData.send(msg0)
	msg0 = "搜索标签:\n"
	msg0 += " - /setu-search [type] [tag]\n"
	msg0 += " * type: normal r18,r18g\n"
	msg0 += " * tag : 查找的tag/画师名/pid\n"
	await SetuData.send(msg0)
	msg0 = "返回图片信息:\n"
	msg0 += " - /setu-info [typer] [pid]\n"
	msg0 += " * type: normal r18,r18g\n"
	await SetuData.finish(msg0)

UploadSetu = on_command('setu-upload')
@UploadSetu.handle() # type: ignore
async def _(bot: Bot, event: Event, state: dict) -> None:
	msg = str(event.message).strip().split(' ')
	if banList(user=str(event.user_id)):
		await UploadSetu.finish("都进黑名单了就别搁着传了")
	if msg[0]:
		pass
	else:
		msg0 = "请检查格式嗷~！\n"
		msg0 += "setu-upload [pid]\n"
		await UploadSetu.finish(msg0)
	pid = msg[0]
	URL = f'https://api.imjad.cn/pixiv/v1/?type=illust&id={pid}'
	info = {}
	try:
		info = json.loads(requests.get(url=URL).text)
	except:
		await UploadSetu.finish(errorRepo("网络请求出错"))
	info = info["response"][0]
	title = info["title"]
	tags = info["tags"]
	account = info["user"]["account"]
	name = info["user"]["name"]
	u_id = info["user"]["id"]

	if "R-18G" in tags:
		s_type = "r18g"
		pass
	elif "R-18" in tags:
		s_type = 'r18'
		pass
	else:
		s_type = 'normal'
		pass
	if s_type in ["r18",'r18g'] and (not whiteList(user=str(event.user_id))):
		await UploadSetu.finish('宁不配上传图片嗷~')
	user_link = f'https://www.pixiv.net/users/' + f'{u_id}'
	img = f'https://pixiv.cat/{pid}.jpg'
	data_setu = (f'{pid}', f'{title}', f'{tags}', f'{account}', f'{name}', f'{u_id}', f'{user_link}', f'{img}')
	s_type = s_type.lower()
	if s_type == "normal":
		for tag in info["tags"]:
			if tag.upper() in ["R-18","R-18G"]:
				await UploadSetu.send('就是你丫的把r18图片传到normal图库里的?')
				file=Path('.') / 'utils' /'utils_banList' / f'banList_user.json'
				#print(file)
				number=str(event.user_id)
				j=json.load(open(file,'r'))
				j['list'].append(number)
				with open(file,'w') as f:
					json.dump(j,f)
				await UploadSetu.finish(f'user:{number}加入黑名单')
	if os.path.exists(f'LxBot/data/data_Sqlite/setu/{s_type}.db'):
		print('数据文件存在！')
	else:
		await UploadSetu.send("数据库都不在添加锤子！？罢了我现创一个")
		con = sqlite3.connect(Path('.') / 'LxBot' / 'data' / 'data_Sqlite' / 'setu' / f'{s_type}.db')
		cur = con.cursor()
		cur.execute(f'CREATE TABLE {s_type}(pid PID, title TITLE, tags TAGS, account ACCOUNT, name NAME, u_id UID, user_link USERLINK, img IMG, UNIQUE(pid, title, tags, account, name, u_id, user_link, img))')
		con.commit()
		cur.close()
		await bot.send(event, '完成')
	con = sqlite3.connect(Path('.') / 'LxBot' / 'data' / 'data_Sqlite' / 'setu' / f'{s_type}.db')
	cur = con.cursor()
	cur.execute(f'INSERT INTO {s_type}(pid, title, tags, account, name, u_id, user_link, img) VALUES(?, ?, ?, ?, ?, ?, ?, ?)', data_setu)
	con.commit()
	cur.close()
	await UploadSetu.finish(f"数据上传完成~！\n涩图库[{s_type}]涩图 +1")


DeleteSetu = on_command('setu-delete', permission=SUPERUSER)
@DeleteSetu.handle() # type: ignore
async def _(bot: Bot, event: Event, state: dict) -> None:
	msg = str(event.message).strip().split(' ')
	if msg[0] and msg[1]:
		pass
	else:
		msg0 = "请检查格式奥~！\n"
		msg0 += "setu-delete [type] [pid]\n"
		msg0 += "type: normal, r18, r18g"
		await DeleteSetu.finish(msg0)
	if msg[0] not in ["normal", "r18", "R18",'r18g']:
		msg0 = "请检查类型~！\n"
		msg0 += "type: normal, r18, r18g"
		await UploadSetu.finish(msg0)
	s_type = msg[0]
	pid = msg[1]
	s_type = s_type.lower()
	if os.path.exists(f'LxBot/data/data_Sqlite/setu/{s_type}.db'):
		print('数据文件存在！')
	else:
		await DeleteSetu.finish("数据库都不在删锤子！？")
	con = sqlite3.connect(Path('.') / 'LxBot' / 'data' / 'data_Sqlite' / 'setu' / f'{s_type}.db')
	cur = con.cursor()
	cur.execute(f'DELETE FROM {s_type} WHERE pid = {pid}')
	con.commit()
	con.close()
	await UploadSetu.finish(f"数据删除完成~！\n涩图库[{s_type}]涩图 -1")




GetSetu = on_command('setu-get')
@GetSetu.handle() # type: ignore
async def _(bot: Bot, event: Event, state: dict) -> None:
	msg = str(event.message).strip().split(' ')
	msg0 = "请检查格式嗷~！\n"
	action='random'
	arg_list=[]
	tmp=[]
	l1=[]
	if msg[0].lower() in ['normal','r18','r18g']:
		s_typer=msg[0]
		if len(msg)==1:
			msg.append("random")
			action='random'
		elif  msg[1]=='random':
			action='random'
		elif msg[1] == 'tags':
			action=msg[1]
			if len(msg)>2:
				arg_list=msg[2:]
			else:
				await GetSetu.finish('tags都不给我搜nm呢(ノ=Д=)ノ┻━┻')
		elif msg[1] == 'name':
			if len(msg)>2:
				action='name'
				arg_list=msg[2:]
			else:
				await GetSetu.finish('画师名不告诉我我搜个鸡儿ヽ(‘⌒´メ)ノ')
		elif msg[1] == 'pid':
			if len(msg)>2:
				action='pid'
				arg_list=msg[2]
			else:
				await GetSetu.finish('Pid不给我给你看空气嗷~')
		elif msg[1] == 'title':
			if len(msg)>2:
				action='title'
				arg_list=msg[2]
			else:
				await GetSetu.finish('标题不给我给给你画张无题?')
	else:
		await GetSetu.finish(msg0)
	state["s_typer"]=s_typer.lower()
	
	if s_typer.lower() in ['r18','r18g','r18g'] and event.detail_type=="group":
		if not whiteList(str(event.user_id)):
			await GetSetu.finish(refuse(user_id=event.user_id,at=True))
	conn = sqlite3.connect(Path('.')/'LxBot'/'data'/'data_Sqlite'/'setu'/f'{s_typer}.db')
	conn.row_factory = sqlite3.Row
	c = conn.cursor()
	cur=c.execute(f"SELECT pid, title, tags, account, name, u_id, user_link, img from {s_typer}")
	if action.lower() == 'pid' or action.lower()=='title':
		for row in cur:
			if row[action]==arg_list:
				pix={'pid':row['pid'],'img_url':row['img'],'author':row['name'],'title':row['title']}
				break
			else:
				await GetSetu.finish('查无此图')
		


	if action.lower() in ['name','tags']:
		for row in cur:
			tmp=[]
			flag=1
			if row[action].startswith("["):
				tmp=literal_eval(row[action])
			else:
				tmp.append(row[action])
			for a in arg_list:
				if a in tmp:
					pass
				else:
					flag=0
					break
			if not flag:
				continue
			l1.append({'pid':row['pid'],'img_url':row['img'],'author':row['name'],'title':row['title']})
		if len(l1)==0:
			await GetSetu.finish("无此标签")
		pix=random.choice(l1)
	if action =='random':
		for row in cur:
			l1.append({'pid':row['pid'],'img_url':row['img'],'author':row['name'],'title':row['title']})
		pix=random.choice(l1)
	msg0='Title:{}\nAuthor:{} pid:{}\n'.format(pix['title'],pix['author'],pix['pid'])
	img='[CQ:image,file={}]'.format(pix['img_url'])
	await GetSetu.send(msg0)	
	flag,vol = checkImages(pix['img_url'])
	if  not (s_typer.lower() in ['r18','r18g']):
		if not flag:
			await GetSetu.finish(vol)
		elif vol==1:
			await GetSetu.finish('[CQ:image,url={}]'.format(pix['img_url']))
		else:
			state["flag"]=vol
			state["img_url"]=pix['img_url']
			await GetSetu.send(f"此图集共有{vol}张图片")
	

	if s_typer.lower() in ['r18','r18g']:
		state["vol"]=1
		if event.detail_type == "group":
			a = await bot.send_group_msg(group_id=event.group_id,message=img)
			time.sleep(1)
			await bot.delete_msg(message_id=a['message_id'],self_id=event.self_id)
			await GetSetu.finish("唉嘿没看到吧~自己去找吧\n")
		elif event.detail_type == "private":
			a = await bot.send_private_msg(user_id=event.user_id,message=img)
			await GetSetu.finish("悄咪咪发给你就不撤回了,注意身体哦")
		

		

@GetSetu.got("vol", prompt="你想获取第几张图片呢？")
async def handle_vol(bot: Bot, event: Event, state: dict):
	vol = state["vol"]
	if not vol or (not vol.isdigit()):
		await GetSetu.reject("我问你要第几张你回了个啥j8东西?告诉我你要第几张")
	elif int(vol)>state["flag"]:
		await GetSetu.reject("我问你要第几张你回了个啥j8东西?告诉我你要第几张")
	else:
		await GetSetu.finish('[CQ:image,url={}]'.format(state["img_url"][:-4]+f"-{state['vol']}.jpg"))


GetTag = on_command('setu-gettag')
@GetTag.handle() # type: ignore
async def _(bot: Bot, event: Event, state: dict) -> None:
	#if not whiteList(user=str(event.user_id)):
	#	await GetTag.finish('宁不配')
	msg = str(event.message).strip().split(' ')
	tmp=[]
	if msg[0].lower() in ['normal','r18','r18g'] and len(msg)>=2:
		s_typer=msg[0]
		if msg[1] in ['tags','name',"title","pid"]:
			mo=msg[1]
	conn = sqlite3.connect(Path('.')/'LxBot'/'data'/'data_Sqlite'/'setu'/f'{s_typer}.db')
	conn.row_factory = sqlite3.Row
	c = conn.cursor()
	cur=c.execute(f"SELECT pid, title, tags, account, name, u_id, user_link, img from {s_typer}")
	for row in cur:
		if mo=='tags':
			tmp+=literal_eval(row[mo])
		else:
			if type(row[mo])==type(0):
				tmp.append(str(row[mo]))
			else:
				tmp.append(row[mo])
	tmp=list(set(tmp))
	tmp=random.sample(tmp,10)
	await GetTag.finish("\n".join(tmp))


SearchTag = on_command('setu-search')
@SearchTag.handle() # type: ignore
async def _(bot: Bot, event: Event, state: dict) -> None:
	#if not whiteList(user=str(event.user_id)):
	#	await SearchTag.finish('宁不配')
	msg = str(event.message).strip().split(' ')
	if msg[0].lower() in ['normal','r18','r18g'] and len(msg)>=2:
		s_typer=msg[0]
		mo=msg[1]
	conn = sqlite3.connect(Path('.')/'LxBot'/'data'/'data_Sqlite'/'setu'/f'{s_typer}.db')
	conn.row_factory = sqlite3.Row
	c = conn.cursor()
	cur=c.execute(f"SELECT pid, title, tags, account, name, u_id, user_link, img from {s_typer}")
	for row in cur:
		for tag in ['tags','name','pid']:
			if tag=='tags':
				if mo in row['tags']:
					await SearchTag.finish('True')
			elif tag=='name':
				if row["name"]==mo:
					await SearchTag.finish('True')
			elif tag=='pid':
				if str(row['pid'])==mo:
					await SearchTag.finish('True')
			else:
				await SearchTag.finish('False')

info = on_command('setu-info')
@info.handle() # type: ignore
async def _(bot: Bot, event: Event, state: dict) -> None:
	#if not whiteList(user=str(event.user_id)):
	#	await info.finish('宁不配')
	msg = str(event.message).strip().split(' ')
	data={'flag':False}
	if (msg[0].lower() in ['normal','r18','r18g']) and (len(msg)==2):
		s_typer=msg[0]
		pid=msg[1]
	else:
		await info.finish("请检查格式嗷~")
	conn = sqlite3.connect(Path('.')/'LxBot'/'data'/'data_Sqlite'/'setu'/f'{s_typer}.db')
	conn.row_factory = sqlite3.Row
	c = conn.cursor()
	cur=c.execute(f"SELECT pid, title, tags, account, name, u_id, user_link, img from {s_typer}")
	for row in cur:
		if str(row["pid"])==pid:
			data={
				'flag':True,
				'pid':str(row["pid"]),
				'tags':row['tags'],
				'title':row['title'],
				'name':row['name'],
				'img':row['img'],
				'typer':s_typer
			}
			break
	else:
		msg0="无此记录"
	if data['flag']:
		msg0=f"标题:{data['title']} 画师:{data['name']} pid:{data['pid']} typer:{data['typer']}\ntags:{data['tags']}\n{data['img']}"
	await info.finish(msg0)