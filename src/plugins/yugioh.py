import json
from nonebot import on_command
from nonebot.adapters.cqhttp import Bot, Event

ocg = on_command("ocg", priority=5)
@ocg.handle()
async def _(bot: Bot, event: Event, state: dict) -> None:
    msg = str(event.message).strip()
    if len(msg) != 1:
        await ocg.finish('你在输什么j8')
    else:
        name=msg[0]
        url=f'https://www.ourocg.cn/search/{name}/'
        await ocg.finish(url)