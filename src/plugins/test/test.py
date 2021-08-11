import os,json,re
import uuid,random
from datetime import datetime
from pathlib import Path
fname="src\\plugins\\test\\686728501.json"
with open(fname,'r') as f:
	check_list=[]
	js=json.load(f)
	for x in js.keys():
		if js[x]["id"]!="id":
			check_list.append({x:js[x]})
	msg = ""
	print(check_list)
	'''
	for x in check_list:
		msg+=f'{x["id"]}:{x["date"]}--{x["title"]}\n'
'''