from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
import uuid,json

class ImgText:
	'''
	ImgText(path=图片文件夹路径,text=文字内容,font_path="normal.ttf",text_color=(0, 0, 0),text_size=0)
	'''
	def __init__(self,path,text,font_path="normal.ttf",text_color=(0, 0, 0),text_size=0):
		self.save_name=str(uuid.uuid4()).split('-')[-1]+'.png'
		self.img_path=path/'img.png'
		self.path=path
		self.text=text
		self.text_color=text_color
		with open(path/'data.json','r') as f:
			drawarea=json.load(f)
		self.x1=drawarea[0]
		self.x2=drawarea[2]
		self.y1=drawarea[1]
		self.y2=drawarea[3]
		self.width=self.x2-self.x1
		self.height=self.y2-self.y1
		if not text_size:
			text_size=int((self.width*self.height/len(text))**0.5*0.8)
			self.text_size=text_size
		else:self.text_size=text_size
		self.width=int(self.width-text_size/2)
		print(self.text_size)
		self.fontStyle = ImageFont.truetype(font_path, self.text_size, encoding="utf-8")
	def get_paragraph(self,text):
		txt = Image.new('RGBA', (self.width, self.height), (255, 255, 255, 0))
		draw = ImageDraw.Draw(txt)
		# 所有文字的段落
		paragraph = ""
		# 宽度总和
		sum_width = 0
		# 几行
		line_count = 1
		# 行高
		line_height = 0
		for char in text:
			width, height = draw.textsize(char, self.fontStyle)
			sum_width += width
			if sum_width > self.width: # 超过预设宽度就修改段落 以及当前行数
				line_count += 1
				sum_width = 0
				paragraph += '\n'
			paragraph += char
			line_height = max(height, line_height)
		if not paragraph.endswith('\n'):
			paragraph += '\n'
		return paragraph, line_height, line_count
	def split_text(self):
	# 按规定宽度分组
		max_line_height, total_lines = 0, 0
		allText = []
		for text in self.text.split('\n'):
			paragraph, line_height, line_count = self.get_paragraph(text)
			max_line_height = max(line_height, max_line_height)
			total_lines += line_count
			allText.append((paragraph, line_count))
		line_height = max_line_height
		total_height = total_lines * line_height
		self.line_height=line_height
		return allText, total_height, line_height

	def draw_text(self,save_path=Path('.')):
		paragraph,total_height,line_height=self.split_text()
		note_img = Image.open(self.img_path).convert("RGBA")
		draw = ImageDraw.Draw(note_img)
		x,y=self.x1, self.y1
		for line, line_count in paragraph:
			draw.text((x, y), line, fill=self.text_color, font=self.fontStyle)
			y += line_height * line_count
		note_img.save(save_path/self.save_name)
		return save_path/self.save_name
		#note_img.show()

if __name__=='__main__':
	img=ImgText(Path('.'),'这是一串非常长长长长长长长长长的测试字符串',text_color=(0, 0, 0))
	img2=ImgText(Path('.'),'短话',text_color=(255, 0, 0))