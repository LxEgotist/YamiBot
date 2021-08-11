from PIL import Image
import json
import requests,os
from datetime import datetime
from PIL import ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True
SCALE=4
def getInfo():
	url='https://himawari8-dl.nict.go.jp/himawari8/img/D531106/latest.json'
	res=requests.get(url=url)
	print(res.text)
	return json.loads(res.text)
def getEarth(flag=0,date='',SCALE=SCALE):
	url_format='https://himawari8-dl.nict.go.jp/himawari8/img/D531106/{}d/{}/{}_{}_{}.png'
	filename_format='{}_{}_{}.png'
	if flag==0:
		info=getInfo()
	else:
		info={
		'date':date
		}
	if info==-1:
		print('奇怪的错误增加了=w=')
		return
	date = datetime.strptime(info['date'], '%Y-%m-%d %H:%M:%S')
	list1=[]
	for x in range(SCALE):
		for y in range(SCALE):
			url = url_format.format(SCALE, 550,date.strftime("%Y/%m/%d/%H%M%S"), x, y)
			list1.append((filename_format.format(date.strftime("%H%M%S"), x, y),url))
	return (list1,info['date'])

def downloadPng(origin_pth='.a',SCALE=SCALE):
	pass


def synthesis(date,SCALE=SCALE):
	date = datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
	filename_format='{}_{}_{}.png'
	pth='{}d'.format(SCALE)
	files_name=date.strftime('%Y%m%d%H%M%S')
	png = Image.new('RGB', (550 * SCALE, 550 * SCALE))
	for x in range(SCALE):
		for y in range(SCALE):
			fname=os.path.join(pth,files_name,filename_format.format(date.strftime("%H%M%S"), x, y))
			img = Image.open(fname)
			png.paste(img, (550 * x, 550 * y, 550 * (x + 1), 550 * (y + 1)))
	png.save(os.path.join(pth,files_name,'earth.png'),'PNG')
	print(os.path.join(pth,files_name,'earth.png'))
if __name__=='__main__':
	pass