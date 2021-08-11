#!/usr/bin/env python
from nonebot import on_command
from nonebot.rule import to_me
from nonebot.adapters.cqhttp import Bot, Event
import requests,json,random
import sys
sys.path.append('../../')
from zoneID import zoneID
from zoneID import difficulty
logs_url="https://cn.fflogs.com/v1/rankings/character/{characterName}/{server}/CN"
tag=["encounterName","percentile","characterName","server","spec"]
headers={
"Host":"cn.fflogs.com",
"User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.146 Safari/537.36"
}
diff=["1047","1048","1050"]
logs = on_command("logs", priority=5)

@logs.handle()
async def handle_first_receive(bot: Bot, event: Event, state: dict):
    args = str(event.message).strip().split()  # 首次发送命令时跟随的参数，例：/天气 上海，则args为上海
    if args:
        state["name"] = args[0]
        state["server"] = args[1]
        state["boss"] = args[2]
    #metric=session.get('metric')


@logs.got("name", prompt="呐~告诉暗酱你要出警谁好不好~")
@logs.got("server", prompt="这小b崽子是哪个服务器的呢")
@logs.got("boss", prompt="要查询特定副本吗")
async def handle_logs(bot: Bot, event: Event, state: dict):
    name=state["name"]
    server=state["server"]
    boss_name=state["boss"]
    (zone,boss)=("","")
    for d in zoneID:
        if boss_name.lower() in d["name"]:
            #print(d["name"])
            (zone,boss)=d["id"]
    logs_data =await get_logs(name,server,zone,boss,"dps")
    await logs.finish(logs_data)

async def get_logs(characterName: str,server: str,zone_id: str,boss_id: str,metric: str) -> str:
    dirts={}
    params={}
    dirts["characterName"]=characterName
    dirts["server"]=server
    url=logs_url.format(**dirts)
    encounter="0"
    if zone_id:
        params["zone"]=zone_id
        if boss_id:
            params["encounter"]=boss_id
            encounter=boss_id
    params["metric"]=metric
    params["timeframe"]="historical"
    params["api_key"]="fe7b33659147c216efc93755d78304a4"
    print("params:",params)
    print(url)
    html=requests.get(url,headers=headers,params=params)
    if not html:
        return ("呐~暗酱查不到呢")
    try:
        D=json.loads(html.text)
        if D in [[],{},"",0]:
            return "无logs"
        dirt={}
        x=-1
        try:
            for i in D:
                if i["percentile"]>x and (i["difficulty"]==101 or encounter in diff):
                    x=i["percentile"]
                    dirt=i
                    dirt["difficulty"]=difficulty[i["difficulty"]]
                    dirt["metric"]=metric
            if encounter in diff:
                dirt["difficulty"]="绝"
            return ('呐~最近几次boss为({difficulty}){encounterName}的战斗中,{characterName}最高logs为({metric}){percentile}%,职业为{spec},{metric}:{total:.1f}'.format(**dirt))
        except:
            for i in D:
                if i["percentile"]>x:
                    x=i["percentile"]
                    dirt=i
                    dirt["difficulty"]=difficulty[i["difficulty"]]
                    dirt["metric"]=metric
            return ('呐~最近几次boss为({difficulty}){encounterName}的战斗中,{characterName}最高logs({metric})为{percentile}%,职业为{spec},{metric}:{total:.1f}'.format(**dirt))
    except:
        return "鬼知道发生了什么错误"