import requests,sqlite3,json,xmltodict
from pathlib import Path
data_path=Path('.')/'LxBot'/'data'
conn = sqlite3.connect(data_path/'eve_data.db')
#df = pandas.read_csv('eve_item_data.csv',encoding='GBK')
#df.to_sql('item', conn, if_exists='append', index=False) 
conn.row_factory = sqlite3.Row
rurl='https://www.ceve-market.org/api/market/region/{}/type/{}.json'
iurl="{}https://www.ceve-market.org/api/market/type/{}.json"
def get_item(name:str):
    _type = None
    cur = conn.cursor()
    cur.execute("select typeID, 物品名称 from item")
    for row in cur:
        if row["物品名称"] == name:
            _type=row['typeID']
    return _type
def get_region(name:str):
    region = None
    cur = conn.cursor()
    cur.execute("select 星域ID, 星域名字 from region")
    for row in cur:
        if name.upper() in row["星域名字"]:
            region=row['星域ID']
    return region

def get_data(item,segmentum=""):
    region=segmentum
    if segmentum=="":
        murl=iurl
    else:
        murl=rurl
        segmentum=get_region(segmentum)

    _type=get_item(item)
    #print(segmentum,_type)
    if segmentum==None:
        return -1,item,segmentum #未知星域
    if _type==None:
        return -2,item,segmentum #未查询到物品
    url=murl.format(segmentum,_type)
    return json.loads(requests.get(url).text),item,region


def get_marketstat(action,item,segmentum=""):
    if segmentum=="":
        pass
    else:
        segmentum=get_region(segmentum)
    _type=get_item(item)
    url=f"https://www.ceve-market.org/api/quicklook?typeid={_type}&regionlimit={segmentum}"
    text=requests.get(url).text
    data=xmltodict.parse(text,encoding='utf-8')['evec_api']['quicklook']
    pass
    





def check(item,segmentum=""):
    if segmentum=="":
        pass
    else:
        segmentum=get_region(segmentum)
    _type=get_item(item)
    #print(segmentum,_type)
    if segmentum==None:
        return -1#未知星域
    if _type==None:
        return -2#未查询到物品
    return 1