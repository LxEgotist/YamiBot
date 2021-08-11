import nonebot,requests,random,json
from nonebot import on_command
from nonebot.rule import to_me
from nonebot.permission import SUPERUSER
from nonebot.adapters.cqhttp import Bot, Event


reboot=on_command("reboot",aliases=["秽土重生"],permission=SUPERUSER)
@reboot.handle()
async def _(bot: Bot, event: Event, state: dict) -> None:
	await bot.set_restart(delay=2000)