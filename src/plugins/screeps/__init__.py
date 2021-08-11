# -*- coding: utf-8 -*-
# __init__.py
# @author LxEgotist
# @description 
# @created 2020-11-10T17:06:05.377Z+08:00
# @last-modified 2020-11-10T17:28:18.400Z+08:00
#


from websocket import create_connection
import requests as req
import json
import time
import os
import random
import sys
from PIL import Image
import re
from pathlib import Path
data_place=Path('.')/'LxBot'/'data'
resources_pth=data_place/'screeps'