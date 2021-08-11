from pathlib import Path
import json
data_place=Path('.')/"LxBot"/"data"/"r6s"
def check_arg(arg:str) -> (str,str):
	'''
	查询传入的参数是个什么j8东西
	干员名: ("干员名","operators")
	武器名: ("武器名","weapons")
	都不是: ("-1","-1")
	'''
	op_file=data_place/"operators.json"
	wp_file=data_place/"weapon.json"
	with open(op_file,'r') as f :
		operators=json.load(f,encoding="GB2312")
	with open(wp_file,'r') as f :
		weapons=json.load(f)
	for x in weapons:
		if x["name"].lower()==arg.lower():
			return (x["name"],"weapons")
	for x in operators:
		print(x)
		if arg in x["nickname"]:
			print("="*10,x,"="*10)
			return (x["name"],"operators")
	else:
		return "-1","-1"
if __name__=="__main__":
	print(check_arg("大锤"))