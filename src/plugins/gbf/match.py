import re,requests,os
os.chdir(r"C:\Users\MSI-PC\Desktop\新建文件夹 (2)\r")
rule="https://huiji-public.huijistatic.com/gbf/uploads/(.*?).jpg"
with open('rurl.txt','r',encoding='utf-8') as f:
    out=re.findall(rule,f.read())
'''for i in range(len(out)):
    out[i]="https://huiji-public.huijistatic.com/gbf/uploads/"+out[i]+".jpg"'''
for name in out:
    print(name[5:])
    with open(name[5:]+".jpg","wb") as f:
        f.write(requests.get("https://huiji-public.huijistatic.com/gbf/uploads/"+name+".jpg").content)
