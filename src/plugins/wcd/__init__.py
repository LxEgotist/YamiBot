# -*- coding: utf-8 -*-
# __init__.py
# @author LxEgotist
# @description 
# @created 2020-11-09T17:16:27.163Z+08:00
# @last-modified 2020-11-23T19:56:28.838Z+08:00
#


from nonebot.plugin import on_command,on_message
from nonebot.permission import SUPERUSER
from nonebot.adapters.cqhttp import Bot, Event
from nonebot.rule import Rule
from pathlib import Path
from utils.rule import check_wordcloud_group
import jieba.posseg as psg
import os,json
import numpy as np
from wordcloud import WordCloud, ImageColorGenerator
import matplotlib.pyplot as plt
from PIL import Image
work_place = Path('.') / 'LxBot' / 'data' / "wordcloud"
file_pth=Path('/root') / 'plugins'/ 'image'/ "wordcloud"
async def check(bot: Bot, event: Event, state: dict) -> bool:
	return True

MessageSave = on_message(rule=check_wordcloud_group,priority=5)
@MessageSave.handle() # type: ignore
async def _(bot: Bot, event: Event, state: dict) -> None:
	group_id=str(event.group_id)
	if not os.path.exists(Path(".")/work_place/f"{group_id}.json"):
		with open(Path(".")/work_place/f"{group_id}.json",'w') as f:
			json.dump({'test':0},f)
	record_type=['a','ad','n','nr','nr1','nr2','nrj','nrf','ns','nsf','nt','nz','nz','nl','ng','q','r','v','y']
	message=event.raw_message
	result=psg.cut(message)
	with open(Path(".")/work_place/f"{group_id}.json",'r') as f:
		js=json.load(f)
	for word,flag in result:
		if flag in record_type:
			if word in js.keys():
				js[word]+=1
			else:
				js[word]=1
	with open(Path(".")/work_place/f"{group_id}.json",'w') as f:
		json.dump(js,f)
	#print([(x.word,x.flag) for x in result])

cloudclear = on_command('cleanwordcloud', permission=SUPERUSER)
@cloudclear.handle()
async def _(bot: Bot, event: Event, state: dict) -> None:
	group_id=str(event.group_id)
	if os.path.exists(Path(".")/work_place/f"{group_id}.json"):
		os.remove(Path(".")/work_place/f"{group_id}.json")
		await cloudclear.finish("泥群的lsp可以重新做人辣~(词频已清空)")
'''
cloudmake = on_command("makeworldcloud",priority=1)
@cloudmake.handle()
async def _(bot: Bot, event: Event, state: dict) -> None:
	group_id=str(event.group_id)
	if not os.path.exists(os.path.join(work_place,f'{group_id}.json')):
		await cloudmake.finish("这群么得记录哦(●ˇ∀ˇ●)")
	print(group_id)
	if os.path.exists(os.path.join(file_pth,f'{group_id}.png')):
		print('delete')
		os.remove(os.path.join(file_pth,f'{group_id}.png'))
	with open(Path(".")/work_place/f"{group_id}.json",'r') as f:
			js=json.load(f,encoding="utf-8")
	wc = WordCloud(font_path='/usr/share/fonts/SIMKAI.TTF',background_color='white', max_words=100)
	wc.generate_from_frequencies(js)
	print('make')
	wc.to_file(os.path.join(file_pth,f'{group_id}.png'))
	img_pth=os.path.join(file_pth,f'{group_id}.png')
	print(img_pth)
	await cloudmake.finish(f"[CQ:image,file={img_pth}]")
'''
wcd = on_command("wc",permission=SUPERUSER)
@wcd.handle()
async def _(bot: Bot, event: Event, state: dict) -> None:
	group_id=str(event.group_id)
	msg = str(event.message).strip().split(' ')
	if msg[0]=="add":
		work_place = Path('.') / 'LxBot' / 'data' / "wordcloud"
		with open(os.path.join(work_place,"wordcloud_group.json"),'r') as f:
			js=json.load(f)
			js['list'].append(group_id)
		with open(os.path.join(work_place,"wordcloud_group.json"),'w') as f:
			js['list']=list(set(js['list']))
			json.dump(js,f)
		await wcd.finish(f"{group_id} 词云功能 enable")
	elif msg[0]=="del":
		work_place = Path('.') / 'LxBot' / 'data' / "wordcloud"
		with open(os.path.join(work_place,"wordcloud_group.json"),'r') as f:
			js=json.load(f)
			js['list'].remove(group_id)
		with open(os.path.join(work_place,"wordcloud_group.json"),'w') as f:
			js['list']=list(set(js['list']))
			json.dump(js,f)
		await wcd.finish(f"{group_id} 词云功能 disable")
	elif msg[0]=="check":
		work_place = Path('.') / 'LxBot' / 'data' / "wordcloud"
		with open(os.path.join(work_place,f"{group_id}.json"),'r') as f:
			sum=len(json.load(f).keys())
		await wcd.finish(f"群{group_id}已记录词频数:{sum}个")
	elif msg[0]=="make":
		#await wcd.finish("如果看到我发这个说明开发者是个nt")
		work_place = Path('.') / 'LxBot' / 'data' / "wordcloud"
		file_pth=Path('/root') / 'plugins'/ 'image'/ "wordcloud"
		if not os.path.exists(os.path.join(work_place,f'{group_id}.json')):
			await wcd.finish("这群么得记录哦(●ˇ∀ˇ●)")
		print(group_id)
		if os.path.exists(os.path.join(file_pth,f'{group_id}.png')):
			print('delete')
			os.remove(os.path.join(file_pth,f'{group_id}.png'))
		with open(Path(".")/work_place/f"{group_id}.json",'r') as f:
				js=json.load(f,encoding="utf-8")
		wc = WordCloud(font_path='/usr/share/fonts/SIMKAI.TTF',background_color='white', max_words=100)
		wc.generate_from_frequencies(js)
		print('make')
		wc.to_file(os.path.join(file_pth,f'{group_id}.png'))
		img_pth=os.path.join(file_pth,f'{group_id}.png')
		print(img_pth)
		await wcd.finish(f"[CQ:image,file={img_pth}]")