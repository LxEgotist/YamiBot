
#!/usr/bin/env python
# -*- coding: utf-8 -*- config.py
# -*- coding: utf-8 -*- @author LxEgotist
# -*- coding: utf-8 -*- @description 
# -*- coding: utf-8 -*- @created 2020-11-09T17:16:26.577Z+08:00
# -*- coding: utf-8 -*- @last-modified 2020-12-07T17:37:20.942Z+08:00
#
from nonebot import get_driver
from pydantic import BaseSettings
from pathlib import Path
from utils.plugin import PluginData

DATA = PluginData('morning', config=True)


class Config(BaseSettings):
	data_pth=Path('.')/'LxBot'/'data'
	morning_hour: int = int(DATA.get_config('morning', 'hour', fallback='7'))
	morning_minute: int = int(
		DATA.get_config('morning', 'minute', fallback='30')
	)
	morning_second: int = int(
		DATA.get_config('morning', 'second', fallback='0')
	)
	try:
		with open(Path('.')/'LxBot'/'data'/"morning.json",'r'):
			group_id=[int(x) for x in json.load(f)['list']]
	except:
		group_id=[495823028,868116069,1072659116]
	class Config:
		extra = "allow"
	


config = Config(**get_driver().config.dict())
