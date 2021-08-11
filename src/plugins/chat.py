import json
from pathlib import Path
from random import choice

from nonebot.log import logger
from nonebot.rule import to_me
from nonebot.adapters.cqhttp import Bot, Event
from nonebot.plugin import on_command, on_message, on_notice

from utils.utils_times import countX
from utils.utils_error import errorRepo
from utils.utils_banList import banList

# ------------------戳 一 戳----------------------
pokehah = on_command("戳一戳", rule=to_me())

@pokehah.handle() # type: ignore
async def _poke(bot: Bot, event: Event, state: dict) -> None:
	user = str(event.user_id)
	group = str(event.group_id)

	if not banList(user, group):
		msg = choice(
					[
						"你再戳！",
						"？再戳试试？",
						"别戳了别戳了再戳就坏了555",
						"我爪巴爪巴，球球别再戳了",
						"你戳你🐎呢？！",
						"那...那里...那里不能戳...绝对...",
						"(。´・ω・)ん?",
						"有事恁叫我，别天天一个劲戳戳戳！",
						"欸很烦欸！你戳🔨呢",
						"?"
					])

		await pokehah.finish(msg)

async def poke_(bot: Bot, event: Event, state: dict) -> bool:
	return (event.detail_type == "notify" and event.raw_event["sub_type"] == "poke" and
			event.sub_type == "notice" and int(event.self_id) == event.raw_event["target_id"])
poke = on_notice(poke_, block=True)
poke.handle()(_poke)
#---------------------------------------------------------
