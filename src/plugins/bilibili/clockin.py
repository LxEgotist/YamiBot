#!/usr/bin/env python
from nonebot import on_command
from nonebot.rule import to_me
from nonebot.adapters.cqhttp import Bot, Event
import requests,json,random
import sys
import requests,json

checkUrl="https://v-xxtb.zust.edu.cn/api/Ncov2019/get_record"
url="https://v-xxtb.zust.edu.cn/api/Ncov2019/update_record_student"
cookies={'Referer':'https://v-xxtb.zust.edu.cn/web/mobile47/', 'Hm_lvt_0d261a1cc090e61ad0a6fc0eb2f4fada':'1602643141', 'Hm_lpvt_0d261a1cc090e61ad0a6fc0eb2f4fada':'1603384251','User-Agent':'Mozilla/5.0 (Linux; Android 10; Redmi K30 5G Build/QKQ1.191117.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/77.0.3865.120 MQQBrowser/6.2 TBS/045331 Mobile Safari/537.36 MMWEBID/8261 MicroMessenger/7.0.19.1760(0x27001353) Process/tools WeChat/arm64 NetType/4G Language/zh_CN ABI/arm64'}
id_data={
        'id':"66662233",
        'user_type':'1',
        'environment_type':'101',
        'module_id':'63'}
html=requests.post(url=checkUrl,data=id_data)
r_id=json.loads(html.text)['data'][0]['id']

clock = on_command("打卡", priority=5)
@clock.handle()
async def handle_first_receive(bot: Bot, event: Event, state: dict):
    args = str(event.message).strip().split()
    if args:
        state["id"] = args[0]

@clock.got("id", prompt="你要给哪个憨批打卡呢,请回复学号")
async def handle_clock(bot: Bot, event: Event, state: dict):
    student_id=state["id"]
    daka_data={
    'id':student_id,
    'user_type':'1',
    'environment_type':'101',
    'location_province':'浙江省',
    'location_city':'杭州市',
    'location_country':'西湖区',
    'morning_state':'1',
    'afternoon_state':'1',
    'is_body_ok':'1',
    'is_gl':'0',
    'is_tl':'0',
    'is_jc':'0',
    'is_2_man':'0',
    'is_family':'0',
    'user_location':'1',
    'student_id':student_id,
    'r_id':r_id,
    'module_id':'63'}
    html=requests.post(url=checkUrl,data=daka_data)
    #print(html.text)
    if html.text.find("\"state\":0")!=-1:
        await clock.send(student_id+'未打卡')
        html=requests.post(url=url,data=daka_data,headers=cookies)
        #print(html.text)
        if html.text.find("\"message\":\"ok\"")!=-1:
        	await clock.finish(student_id+"打卡成功!")
    else:
        await clock.finish(student_id+'已经打过卡了哟')