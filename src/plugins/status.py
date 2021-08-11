'''
Descripttion: 
version: 
Author: LxEgotist
Date: 2020-11-04 12:01:22
LastEditors: LxEgotist
LastEditTime: 2020-11-09 01:27:19
'''
#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import psutil
import sqlite3
from pathlib import Path

from nonebot.plugin import on_command
from nonebot.adapters.cqhttp import Bot, Event
from utils.utils_banList import banList
from utils.utils_error import errorRepo


status_info = on_command('status')

@status_info.handle() # type: ignore
async def _(bot: Bot, event: Event, state: dict) -> None:
	user = str(event.user_id)
	group = str(event.group_id)

	if not banList(user, group):
		msg = str(event.message).strip()
		
		if msg:
			pass
		else:
			msg0 = "States :\n"
			msg0 += "├info\n"
			msg0 += "└sqlite\n"

			await status_info.finish(msg0)

		if msg == "info":
			try:
				cpu = psutil.cpu_percent(interval=1)
				memory = psutil.virtual_memory().percent
				disk = psutil.disk_usage('/').percent
				inteSENT = psutil.net_io_counters().bytes_sent # type: ignore
				inteRECV = psutil.net_io_counters().bytes_recv # type: ignore
			except:
				await status_info.finish(errorRepo("读取系统状态失败"))
			
			status = "そう、私は闇ちゃんです。"

			if cpu > 80: # type: ignore
				status = '暗酱感觉头有点晕...'
				if memory > 80: # type: ignore
					status = '暗酱感觉有点头晕并且有点累...'
			elif disk > 80: # type: ignore
				status = '暗酱感觉身体要被塞满了...'
			
			msg0 = "暗酱的身体状况:\n"
			msg0 += f"* CPU: {cpu}%\n" # type: ignore
			msg0 += f"* MEM: {memory}%\n" # type: ignore
			msg0 += f"* Disk {disk}%\n" # type: ignore
			msg0 += f"* BytesSENT: {inteSENT}\n" # type: ignore
			msg0 += f"* BytesRECV: {inteRECV}\n" # type: ignore
			msg0 += status

			await status_info.finish(msg0)
		
		elif msg == "sqlite":
			con = sqlite3.connect(Path('.') / 'LxBot' / 'data' / 'data_Sqlite' / 'setu' / 'normal.db') # setu-normal
			cur = con.cursor()
			cur.execute("select * from normal")
			data_normal = len(cur.fetchall())
			con.close()


			con = sqlite3.connect(Path('.') / 'LxBot' / 'data' / 'data_Sqlite' / 'setu' / 'r18.db') # setu-r18
			cur = con.cursor()
			cur.execute("select * from r18")
			data_r18 = len(cur.fetchall())
			con.close()

			
			con = sqlite3.connect(Path('.') / 'LxBot' / 'data' / 'data_Sqlite' / 'setu' / 'r18g.db') # setu-r18
			cur = con.cursor()
			cur.execute("select * from r18g")
			data_r18g = len(cur.fetchall())
			con.close()

			msg0 = "暗酱的涩图库:\n"
			msg0 += f"├normal: {data_normal}\n"
			msg0 += f"└R-18: {data_r18}\n"
			msg0 += f"└R-18G: {data_r18g}"

			await status_info.finish(msg0)
