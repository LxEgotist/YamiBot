#!/usr/bin/env python
from nonebot import on_command
from nonebot.rule import to_me
from nonebot.adapters.cqhttp import Bot, Event
import requests,json

yx=on_command("团分", priority=5)
@yx.handle()
async def handle_first_receive(bot: Bot, event: Event, state: dict):
    args = str(event.message).strip()
    if args:
        state["name"] = args


@yx.got("name", prompt="呐~你要查谁的团分呢~")
async def handle_yx(bot: Bot, event: Event, state: dict):
    name = state["name"]
    if not name:
        await yx.reject("请输入查询ID")
    ss=''
    url='http://300report.jumpw.com/api/getrole?name=%s'%name
    j=json.loads(requests.get(url).text)
    print(url,j['Result'])
    if j['Result']=="OK":
        try:
            for tmp in j['Rank']:
                if tmp["RankName"]=="团队实力排行":
                    ss="ID:%s 排名:%s 团分:%s 排名变化:%s 胜率:%.2f"%(j["Role"]["RoleName"],tmp["Rank"],tmp["Value"],tmp["RankChange"],j["Role"]["WinCount"]/j["Role"]["MatchCount"]*100)+'%'
        except:
            ss="碰到了奇怪的错误"
    else:
        ss=("呐~没有这个人哦")
    #print(ss)
    await yx.finish(ss)