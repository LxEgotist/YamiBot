'''
Descripttion: 
version: 
Author: LxEgotist
Date: 2020-11-09 10:08:09
LastEditors: LxEgotist
LastEditTime: 2020-11-09 10:08:14
'''
import os
from pathlib import Path
from random import sample

import nonebot
from nonebot.plugin import on_command, on_message
from nonebot.permission import SUPERUSER
from nonebot.adapters.cqhttp import Bot, Event


# 此目录下均为功能测试！


testRecord = on_command('苏帕酱噗', permission=SUPERUSER)

@testRecord.handle() # type: ignore
async def _(bot: Bot, event: Event, state: dict) -> None:
    msg0='[CQ:record,file=test.mp3]'
    print(msg0)
    await testRecord.finish(msg0)