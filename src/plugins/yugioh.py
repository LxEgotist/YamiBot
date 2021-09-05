import json
from urllib import parse, request
from nonebot import on_command
from utils.utils_banList import banList
from utils.utils_img import compress_image, aio_download_pics
from nonebot.adapters.cqhttp import Bot, Event
from bs4 import BeautifulSoup
import requests
import re


def getID(key:str) -> str :
    if __name__ == '__main__':
        key = parse.quote(key)
        target = f'https://ygocdb.com/?search={key}'
        req = requests.get(url=target)
        html = req.text
        get = BeautifulSoup(html)
        texts = get.find_all('div', class_='col-md-6 col-xs-8 names')
        texts = texts[0].text.replace('\n', '')
        number = "".join(re.findall("\d+", texts))
    return number


OCGSearch = on_command("ocg", priority = 5)


@OCGSearch.handle()
async def _(bot: Bot, event: Event, state: dict) -> None :
    user = str(event.user_id)
    group = str(event.group_id)

    if not banList(user, group) :
        msg = str(event.message).strip().split(' ')
        if len(msg) == 1:

            msg0 = "-==Yu-Gi-Oh!==-\n"
            msg0 += "ocg:\n"
            msg0 += "搜索：- search [keyword]\n"
            msg0 += "裁定：- rtd [keyword]\n"
            msg0 += "查卡：- card [card ID]/[keyword]\n"
            msg0 += "查图：- image [card ID]/[keyword]"

            await OCGSearch.finish(msg0)
        elif len(msg) == 2:
            mo = msg[0]
            key = msg[1]
            if mo == "search" :  # 搜索
                key = parse.quote(key)
                url = f'https://ygocdb.com/?search={key}/'

                await OCGSearch.finish(url)
            elif mo == "image" :  # 查图
                if key.isdigit() :
                    if isinstance(eval(key), int) :
                        url = f'https://cdn.233.momobako.com/ygopro/pics/{key}.jpg'
                        msg0 = f'[CQ:image,file=file:///{compress_image(await aio_download_pics(url))}]\n'

                        await OCGSearch.finish(msg0)
                    else :
                        await OCGSearch.finish('卡密都不知道查个锤子卡')
                else :
                    key = getID(key)
                    url = f'https://cdn.233.momobako.com/ygopro/pics/{key}.jpg'
                    msg0 = f'[CQ:image,file=file:///{compress_image(await aio_download_pics(url))}]\n'

                    await OCGSearch.finish(msg0)

            elif mo == "rtd" :  # 裁定
                key = parse.quote(key)
                url = f'https://ocg-rule.readthedocs.io/zh_CN/latest/?rtd_search={key}'

                await OCGSearch.finish(url)
            elif mo == "card" :  # 查卡
                if key.isdigit() :
                    if isinstance(eval(key), int) :
                        url = f'https://ygocdb.com/card/{key}'

                        await OCGSearch.finish(url)
                    else :
                        await OCGSearch.finish('卡密都不知道查个锤子卡')
                else :
                    key = getID(key)
                    url = f'https://ygocdb.com/card/{key}'

                    await OCGSearch.finish(url)
            else :

                await OCGSearch.finish('你在输什么j8')
        else:

            await OCGSearch.finish('你在输什么j8')
