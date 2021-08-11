# -*- coding: utf-8 -*-
# __init__.py
# @author LxEgotist
# @description 
# @created 2020-11-10T19:04:38.445Z+08:00
# @last-modified 2020-11-11T20:07:20.768Z+08:00

import os,json,re
import uuid,random
from datetime import datetime
from pathlib import Path
from nonebot import scheduler as sc
from nonebot.plugin import on_command,on_metaevent
from nonebot.permission import SUPERUSER,GROUP_ADMIN,GROUP_OWNER
from nonebot.adapters.cqhttp import Bot, Event
from apscheduler.schedulers.blocking import BlockingScheduler
from utils.helpers import get_first_bot
pattern=re.compile(r"^([1-2]{1}\d{3})\-(([0]{1}[1-9]{1})|([1]{1}[0-2]{1}))\-(([0]{1}[1-9]{1})|([1-2]{1}\d{1})|([3]{1}[0-1]{1}))\s(([0-1]{1}\d{1})|([2]{1}[0-3]))\:([0-5]{1}\d{1})\:([0-5]{1}\d{1})")
data_place=Path('.')/"LxBot"/"data"/"sched"
date_format="%Y-%m-%d %H:%M:%S"
def check_first_connect(bot: Bot, event: Event, state: dict) -> bool:
	if event.sub_type == 'connect':
		return True
	return False
def exists(path:str)->bool:
	#检查文件是否存在并创建
	#schedule专用
	if not os.path.exists(os.path.split(path)[0]):
		os.makedirs(os.path.split(path)[0])
	if not os.path.exists(path):
		with open(path,'w') as f:
			json.dump({"list":[{
					"date":"date",
					"title":"title",
					"id":"0",
					"uuid":"uuid",
					"group":0}]
					},f)
		return False
	pass
#首次运行添加日程

scheduler_metaevent = on_metaevent(rule=check_first_connect, block=True)
@scheduler_metaevent.handle()
async def _(bot: Bot, event: Event, state: dict):
	js=[]
	for fpath, dirname, fnames in os.walk(data_place):
		for fname in fnames:
			with open(Path(fpath)/fname,"r") as f:
				js+=json.load(f)["list"]
	for data in js:
		if data["id"] != "0":
			kwargs={"id":data["id"],"group_id":data["group"],"message":data["title"]}
			sc.add_job(send_msg,"date",kwargs=kwargs,id=data["uuid"],run_date=datetime.strptime(data['date'],date_format))
	pass

async def send_msg(id:str,group_id:int,message:str):
	await get_first_bot().send_msg(
			message_type='group',
			group_id=group_id,
			message=message,
		)
	fname= data_place / f"{group_id}.json"
	print("开始删除")
	with open(fname,'r') as f:
		js=json.load(f)
		for x in js["list"]:
			if x["id"]==id:
				print(f"反正if执行了id是{x['id']}")
				js["list"].remove(x)
				with open(fname,'w') as f:
					json.dump(js,f)


	pass
sched_check = on_command('sched-check',priority=5)
@sched_check.handle()
async def _(bot: Bot, event: Event, state: dict) -> None:
	
	fname= data_place / f"{event.group_id}.json"
	with open(fname,'r') as f:
		check_list=[]
		js=json.load(f)
		for x in js["list"]:
			if x["id"]!="0":
				check_list.append(x)
	msg = " "
	print(bool(check_list))
	if bool(check_list):
		for x in check_list:
			msg+=f'[{x["id"]}]:{x["date"]}--{x["title"]}\n'
		await sched.finish(msg)
	else:
		await sched.finish("无日程")
		pass


sched = on_command('sched',priority=5,permission=(SUPERUSER|GROUP_ADMIN|GROUP_OWNER))
@sched.handle()
async def _(bot: Bot, event: Event, state: dict) -> None:
	msg = str(event.message).strip().split(' ')
	group_id=str(event.group_id)
	fname=data_place/f"{group_id}.json"
	if msg:
		if msg[0] == 'help':
			pass
		elif msg[0]== "check":
				with open(fname,'r') as f:
					check_list=[]
					js=json.load(f)
					for x in js["list"]:
						if x["id"]!="0":
							check_list.append(x)
				msg = " "
				print(bool(check_list))
				if bool(check_list):
					for x in check_list:
						msg+=f'[{x["id"]}]:{x["date"]}--{x["title"]}\n'
					await sched.finish(msg)
				else:
					await sched.finish("无日程")
					pass

		elif len(msg) <= 2 and len(msg)>=1:
			if msg[0]== "del":
				if len(msg)==1:
					await sched.finish(r"请检查格式嗷~")
				fname=data_place/f"{group_id}.json"
				if not exists(fname):
					await sched.finish(r"未查询到日程")
				date  = msg[1]
				msg0  = " ".join(msg[2:])
				with open(fname,'r') as f:
					js=json.load(f)
				for x in js["list"]:
					if x["id"]==msg[1]:
						tmp=x
						js["list"].remove(x)
						#try:
						pass
						#sc.remove_job(x["id"])
						with open(fname,'w') as f:
							json.dump(js,f)
						await sched.finish(f"{tmp['date']}:{tmp['title']} 已取消")
						#except:
						#	await sched.finish("发生了奇怪的错误")

						

				else:
					await sched.finish(r"未查询到日程")
				pass
			
		elif len(msg) >= 3:
			if msg[0] == "add":
				exists(fname)
				msg0  = msg[1]
				date  = " ".join(msg[2:])
				with open(fname,'r') as f:
					js=json.load(f)
				if not re.findall(pattern,date):
					await sched.finish(r"日期格式有误,请输入%Y-%m-%d %H:%M:%S格式时间")
				else:
					x = str(random.randint(1,99))
					while (x in [i["id"] for i in js["list"]]):
						x = str(random.randint(1,99))
					data={
						"group":event.group_id,
						"title":msg0,
						"date":date,
						"id" : x,
						"uuid": str(uuid.uuid4()).split('-')[-1],
					}
					js["list"].append(data)
					with open(fname,'w') as f:
						json.dump(js,f)
					kwargs={"id":data["id"],"group_id":event.group_id,"message":data["title"]}
					sc.add_job(send_msg,"date",kwargs=kwargs,id=data["uuid"],run_date=datetime.strptime(data['date'],date_format))
					await sched.finish(f'已经添加日程:\n{data["title"]}\n{data["date"]}')
				pass
			else:
				await sched.finish(r"请检查格式嗷~")
		else:
			pass
	else:
		pass
