# -*- coding: utf-8 -*-
# __init__.py
# @author LxEgotist
# @description 
# @created 2020-11-09T17:16:25.641Z+08:00
# @last-modified 2020-11-09T20:29:04.424Z+08:00
#



import os
import string
import aiohttp
import PIL.Image as Image
from pathlib import Path
from random import sample

from PIL import Image
from PIL import ImageFile

async def aio_download_pics(url):
    """
    :说明:
    
      下载图片并重名文件
    
    :参数:

      * ``URL: str``: 目标网址
    
    :返回:

      文件根目录
    
    :用法:

    .. code-block:: python

        aio_download_pics(URL="https://www.demo.com/demo.jpg")

    """
    path = Path('.') / 'LxBot' / 'data' / 'data_Temp' / 'img'
    path = os.path.abspath(path)
    img_key = ''.join(sample(string.ascii_letters + string.digits, 16))
    img = os.path.join(path,f'{img_key}.png')
    async with aiohttp.ClientSession() as session:         
        async with session.get(url) as response:                
            pic = await response.read()    #以Bytes方式读入非文字                     
            with open(img, mode='wb') as f:# 写入文件
                f.write(pic)
                f.close()
    return img

def compress_image(outfile: str, kb=400, quality=85, k=0.9) -> str:
    """
    :说明:
    
      不改变图片尺寸压缩到指定大小
    
    :参数:

      * ``outfile: str``: 文件目录
      * ``kb=150``: 目标文件大小，单位：KB

    :返回:

      文件根目录

    :用法:

    .. code-block:: python

        compress_image(outfile=C:/xxx)

    """
    o_size = os.path.getsize(outfile) // 1024
    if o_size <= kb:
        return outfile
   
    ImageFile.LOAD_TRUNCATED_IMAGES = True # type: ignore
    while o_size > kb:
        im = Image.open(outfile)
        x, y = im.size
        out = im.resize((int(x*k), int(y*k)), Image.ANTIALIAS)
        try:
            out.save(outfile, quality=quality)
        except Exception as e:
            print(e)
            break
        o_size = os.path.getsize(outfile) // 1024
    return outfile
