import sys
import nonebot,os
from nonebot import on_command
from nonebot.rule import to_me
from nonebot.adapters.cqhttp import Bot, Event
sys.path.append('/root/LxBot/src/plugins/gbf')
import gbfdraw
draw = on_command("gbf", priority=5)
@draw.handle()
async def handle_draw(bot: Bot, event: Event, state: dict):
    (filename,delete)=gbfdraw.gbfdraw()
    print('[CQ:image,file=%s]' % filename)
    await draw.send("作为手续费暗酱随机拿走了你的一张%s"%delete)
    await draw.finish('[CQ:image,file=%s]'%filename)
    os.remove(os.path.join('/root/plugins/image',filename))
