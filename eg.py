'''
Descripttion: 
version: 
Author: LxEgotist
Date: 2020-11-09 10:22:02
LastEditors: LxEgotist
LastEditTime: 2020-11-09 10:31:36
'''
import re,requests

pattern=re.compile(r're.findall(re.compile(r"(https?|ftp|file)://[-A-Za-z0-9+&@#/%?=~_|!:,.;]+[-A-Za-z0-9+&@#/%=~_|]",str)') #匹配规则
ulr="https://cli.shodan.io/"
data={
	"参数1":"值1",
	"参数2":"值2"
} #提交的参数自己改
text= requests.get(url=url,data=data).text #获取返回内容

re.findall(pattern,text)


import shodan    #导入shodan库
api=shodan.Shodan("cB9sXwb7l95ZhSJaNgcaO7NQpkzfhQVM")  #指定API_KEY,返回句柄
try:
    results=api.search('apache')    #搜索apache，返回 JSON格式的数据
    print(results)
    print("Results found:%s"%results['total'])
    for result in results['matches']:
        print(result['ip_str'])     #打印出ip地址
except shoadn.APIError,e:
    print("Error:%s"%e)