import json
from nonebot import on_command
from utils.utils_banList import banList
from nonebot.adapters.cqhttp import Bot, Event

OCGSearch = on_command("ocg", priority=5)


@OCGSearch.handle()
async def _(bot: Bot, event: Event, state: dict) -> None:
    user = str(event.user_id)
    group = str(event.group_id)

    if not banList(user, group):
        msg = str(event.message).strip()

        if msg:
            pass
        else:
            msg0 = "-==Yu-Gi-Oh!==-\n"
            msg0 += "ocg:\n"
            msg0 += "├search [keyword]\n"
            msg0 += "└image [card ID]"

            await OCGSearch.finish(msg0)

        if not (len(msg) == 2 and (msg[0] == "search" or msg[0] == "image")):
            await OCGSearch.finish('你在输什么j8')
        else:
            if msg[0] == "search":
                key = msg[1]
                url = f'https://www.ourocg.cn/search/{key}/'

                await OCGSearch.finish(url)
            elif msg[0] == "image":
                Key = msg[1]
                num = eval(Key)
                if isinstance(num, int):
                    url = f'https://storage.googleapis.com/ygoprodeck.com/pics/{Key}.jpg'
                else:
                    await OCGSearch.finish('你在输什么j8')


