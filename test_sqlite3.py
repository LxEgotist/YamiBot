'''
Descripttion: 
version: 
Author: LxEgotist
Date: 2020-11-09 16:37:18
LastEditors: LxEgotist
LastEditTime: 2020-11-09 16:53:53
'''
import requests,sqlite3,os,json,base64

URL="https://api.imjad.cn/pixiv/v1/?type=illust&id=84932457"
url="https://i.pixiv.cat/img-original/img/2020/10/11/00/00/12/84932457_p0.png"
pid="84932457"
info = json.loads(requests.get(url=URL).text)
info = info["response"][0]
title = info["title"]
tags = info["tags"]
account = info["user"]["account"]
name = info["user"]["name"]
u_id = info["user"]["id"]
#cont=base64.b64encode(requests.get(url).content)
cont=requests.get(url,timeout=10).content
user_link = f'https://www.pixiv.net/users/' + f'{u_id}'
data_setu = (f'{pid}', f'{title}', f'{tags}', f'{account}', f'{name}', f'{u_id}', f'{user_link}', f'{url}',f'{cont}')
#创建
if not os.path.exists('test.db'):
	con = sqlite3.connect('test.db')
	cur = con.cursor()
	cur.execute(f'CREATE TABLE test(pid PID, title TITLE, tags TAGS, account ACCOUNT, name NAME, u_id UID, user_link USERLINK, img_url IMGURL,img IMG, UNIQUE(pid, title, tags, account, name, u_id, user_link, img_url, img))')
	con.commit()
	cur.close()
con = sqlite3.connect( 'test.db')
cur = con.cursor()
cur.execute(f'INSERT INTO test(pid, title, tags, account, name, u_id, user_link, img_url, img) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)', data_setu)
con.commit()
cur.close()