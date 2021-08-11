import os,random,time,uuid
from PIL import Image
def ex_card(cards, num):
    labels = [0]
    for card in cards:
        labels.append(labels[-1] + card[1])
 
    rands = [random.randint(1, labels[-1]) for _ in range(num)]
    for rand_i, rand in enumerate(rands):
        for label_i, label in enumerate(labels):
            if label >= rand:
                rands[rand_i] = cards[label_i - 1]
                break
    return rands
def main(l1):
    cards=l1
    exs = ex_card(cards, 10)
 
    # 验证
    res = {card[1]: 0 for card in cards}
    for ex in exs:
        res[ex[1]] += 1
    '''print('各种卡片的个数：')
    print(res)
    print()
    print('权重，实际权重')
    for k, v in res.items():
        print(k / sum(res.keys()), v / sum(res.values()))
    '''
    return res
def gbfdraw():
    random.seed(time.time())
    box=[(20,47,138,113),(145,47,263,113),(270,47,289,113),(20,146,138,212),(145,146,263,212),(270,146,289,212),(20,245,138,312),(145,245,263,312),(270,245,289,312)]
    respath='/root/LxBot/src/plugins/gbf'
    model="/root/LxBot/src/plugins/gbf/模板/1.png"
    pr={'ssr':30,'sr':150,'r':820}
    daily=[['ssr', pr['ssr']], ['sr', pr['sr']], ['r', pr['r']]]
    out=main(daily)
    res={}
    res['ssr']=out[pr['ssr']]
    res['sr']=out[pr['sr']]
    res['r']=out[pr['r']]
    delete = random.choice(['ssr','sr','r'])
    while res[delete] == 0:
        delete = random.choice(['ssr','sr','r'])
    #print(delete)
    res[delete]=res[delete]-1
    #print(res)
    ssrlist=[]
    srlist=[]
    rlist=[]
    for filename in os.listdir(os.path.join(respath,'ssr')):
        ssrlist.append(os.path.join(os.path.join(respath,'ssr'),filename))
    for filename in os.listdir(os.path.join(respath,'sr')):
        srlist.append(os.path.join(os.path.join(respath,'sr'),filename))
    for filename in os.listdir(os.path.join(respath,'r')):
        rlist.append(os.path.join(os.path.join(respath,'r'),filename))
    last=[]
    last.append(random.sample(ssrlist,res['ssr']))
    last.append(random.sample(srlist,res['sr']))
    last.append(random.sample(rlist,res['r']))
    def listdel(x):
        return [a for b in x for a in listdel(b)] if isinstance(x, list) else [x]
    last=listdel(last)

    origin_img = Image.open(model)
    def image_resize(img, size=(138-20, 113-47)):
        try:  
            if img.mode not in ('L', 'RGB'):  
                img = img.convert('RGB')  
            img = img.resize(size)  
        except:  
            pass  
        return img
    for i in range(len(last)):
        origin_img.paste(image_resize(Image.open(last[i])),box[i][0:2])
    uuid_str = uuid.uuid4().hex
    tmp_file_name = '%s.png' % uuid_str
    origin_img.save(os.path.join('/root/plugins/image',tmp_file_name))
    return (tmp_file_name,delete)
