# -*- coding: utf-8 -*-
"""
Created on Wed Jan 30 20:17:54 2019

@author: asus
"""

from paipan import *

class Explain(House,People):
    
    def __init__(self,house,people):
        houseyear=house[0]
        liunian=house[1]
        zuo=house[2]
        xiang=house[3]
        if len(house)==4:
            jianzuo=None
            jianxiang=None
        else:
            jianzuo=house[4]
            jianxiang=house[5]
        name=people[0]
        gender=people[1]
        peopleyear=people[2]
        month=people[3]
        day=people[4]
        House.__init__(self,houseyear,liunian,zuo,xiang,jianzuo,jianxiang)
        People.__init__(self,name,gender,peopleyear,month,day)
        self.explain=dict.fromkeys(list('坎艮震巽离坤兑乾中总'))
    def getShanxiangguanxi(self):
        pass
    def getLiunianzhuxingguanxi(self):
        pass
    def getMinggongguanxi(self):
        dong=list('震巽离坎')
        xi=list('坤兑乾艮')
        ming=''
        zhai=''
        if self.minggua in dong:
            ming='东四命'
        elif self.minggua in xi:
            ding='西四命'
        if self.zuogua in dong:
            zhai='东四命'
        elif self.zuogua in xi:
            zhai='西四命'
        if ming==zhai:
            return '命宅匹配'
        else:
            return '命宅不匹配'
    def getLiantoushanxiangguanxi(self):
        pass
    def getFeixingfigure(self,fname):
        parts=dict.fromkeys('巽离坤震中兑艮坎乾')
        edge=120
        mid=int(edge/3)
        right=int(edge*2/3)
        img = Image.new('RGB', (edge*3, edge*3), (255,255,255))
        draw = ImageDraw.Draw(img)
        font = ImageFont.truetype("simhei.ttf", 20, encoding="utf-8")
        font1 = ImageFont.truetype("simhei.ttf", 12, encoding="utf-8")
        for k,v in self.pan.iterrows():
            draw.text((10+edge*(v.loc['横']-1),10+edge*(v.loc['竖']-1)),v.loc['山盘'],(0,0,0),font=font)
            draw.text((10+right+edge*(v.loc['横']-1),10+edge*(v.loc['竖']-1)),v.loc['向盘'],(0,0,0),font=font)
            draw.text((10+mid+edge*(v.loc['横']-1),10+mid+edge*(v.loc['竖']-1)),v.loc['天盘'],(0,0,0),font=font)
            draw.text((10+edge*(v.loc['横']-1),10+right+edge*(v.loc['竖']-1)),v.loc['方位'],(0,0,0),font=font)
            draw.text((10+mid+edge*(v.loc['横']-1),10+right+edge*(v.loc['竖']-1)),k[1],(0,0,0),font=font)
            draw.rectangle([(0+edge*(v.loc['横']-1),0+edge*(v.loc['竖']-1)),(edge+edge*(v.loc['横']-1),edge+edge*(v.loc['竖']-1))],outline=(0,0,0))

        img.save(userfolder+fname+'.png')

    def explainFitfig(self,exp):
        line=24
        expnew=''
        #print(repr(exp))
        exp=exp.replace('\xa0','')
        exp=exp.split('\n')
        for ex in exp:
            for i in range(int(len(ex)/line)+1):
                if line*(i+1)<=len(ex):
                    expnew+=ex[line*i:line*(i+1)]+'\n'
                else:
                    expnew+=ex[line*(i):]
            expnew+='\n'
        return expnew
    '''
    def getExplainfigure(self,fname):
        img=Image.open(userfolder+fname+'.png')
        draw=ImageDraw.Draw(img)
        edge=120
        mid=int(edge/3)
        right=int(edge*2/3)
        font1 = ImageFont.truetype("simhei.ttf", 12, encoding="utf-8")
        if not self.isjian:
            draw.text((5+edge*3,5),self.yun+'运'+self.zuo+'山'+self.xiang+'向',(0,0,0),font=font1)
        else:
            draw.text((5+edge*3,5),self.yun+'运'+self.zuo+'山'+self.xiang+'向'+'兼'+self.jianzuo+self.jianxiang,(0,0,0),font=font1)
        draw.text((5+edge*3,30),'文昌位在'+self.wenchangwei,(0,0,0),font=font1)
        draw.text((5+edge*3,60),'财位在'+self.caiwei,(0,0,0),font=font1)
        gejuw='格局有：'+'、'.join(self.geju)
        for i in range(int(len(gejuw)/18)):
            gejuw=gejuw[:18*(i+1)]+'\n'+gejuw[18*(i+1):]
        draw.text((5+edge*3,90),gejuw,(0,0,0),font=font1)
        img.save(userfolder+fname+'解释.png')
    '''
    def getExplainfigure(self,fname):
        edge=130
        img = Image.new('RGB', (edge*4, edge*11), (255,255,255))
        draw = ImageDraw.Draw(img)
        font = ImageFont.truetype("simhei.ttf", 20, encoding="utf-8")
        if self.isjian:
            title=self.yun+'运'+self.zuo+'山'+self.xiang+'向'+'替卦'
        else:
            title=self.yun+'运'+self.zuo+'山'+self.xiang+'向'+'下卦'
        if not self.isjian:
            draw.text((200,5),self.yun+'运'+self.zuo+'山'+self.xiang+'向',(0,0,0),font=font)
        else:
            draw.text((200,5),self.yun+'运'+self.zuo+'山'+self.xiang+'向'+'兼'+self.jianzuo+self.jianxiang,(0,0,0),font=font)
        draw.text((5,35),self.explainFitfig('以下内容多为古书记载内容，其价值观和当今社会恐有不同，且风水门派众多，还请斟酌理解。'),(0,0,0),font=font)
        with open(jieshiwebfolder+title+'.txt','r',encoding='utf-8') as f:
            text=f.read()
            textnew=self.explainFitfig(text)
            #print(repr(textnew[:100]))
            draw.text((5,90),textnew,(0,0,0),font=font)
        img.save(userfolder+fname+'解释.png')
    def getExplainFurther(self):
        words={}
        for k,v in self.pan.iterrows():
            word=dict.fromkeys(['山星','向星','山向五行','向山五行','双星组合','流年'])
            shanxing=gonggua.loc[v.loc['山盘']]
            shanyun=self.pan[self.pan['天盘']==v.loc['山盘']]['生旺'].values[0]
            word['山星']=shanxing.loc['九星']+'，又称'+shanxing.loc['别称']+'星，为'+shanxing.loc['吉凶']+'星。'
            if shanyun in ['生','旺']:
                word['山星']+='得令，寓意%s'%(jiuxing.loc[v.loc['山盘'],'旺'])
            elif shanyun in ['死','煞']:
                if shudict[v.loc['山盘']]+shudict[v.loc['地盘']]==10:
                    word['山星']+='虽然失令，但因为与地运星合十，以旺星论，寓意%s'%(jiuxing.loc[v.loc['山盘'],'旺'])
                else:
                    word['山星']+='失令，寓意%s'%(jiuxing.loc[v.loc['山盘'],'衰'])
            elif shanyun in ['退']:
                word['山星']+='虽然退气，但余温尚存，不旺不衰。'

            xiangxing=gonggua.loc[v.loc['向盘']]
            xiangyun=self.pan[self.pan['天盘']==v.loc['向盘']]['生旺'].values[0]
            word['向星']=xiangxing.loc['九星']+'，又称'+xiangxing.loc['别称']+'星，为'+xiangxing.loc['吉凶']+'星。'
            if xiangyun in ['生','旺']:
                word['向星']+='得令，寓意%s'%(jiuxing.loc[v.loc['向盘'],'旺'])
            elif xiangyun in ['死','煞']:
                if shudict[v.loc['山盘']]+shudict[v.loc['地盘']]==10:
                    word['向星']+='虽然失令，但因为与地运星合十，以旺星论，寓意%s'%(jiuxing.loc[v.loc['向盘'],'旺'])
                else:
                    word['向星']+='失令，寓意%s'%(jiuxing.loc[v.loc['向盘'],'衰'])
            elif xiangyun in ['退']:
                word['向星']+='虽然退气，但余温尚存，不旺不衰。'
            zhuwx,kewx,skb=self.getXingshengkebi(v.loc['山盘'],v.loc['向盘'])
            word['山向五行']='山'+zhuwx+'向'+kewx+skb
            if skb in ['生入','生出']:
                word['山向五行']+='，吉'
            elif skb in ['克入','克出']:
                word['山向五行']+='，凶'
            zhuwx,kewx,skb=self.getXingshengkebi(v.loc['向盘'],v.loc['山盘'])
            word['向山五行']='向'+zhuwx+'山'+kewx+skb
            if skb in ['生入','生出']:
                word['向山五行']+='，吉'
            elif skb in ['克入','克出']:
                word['向山五行']+='，凶'
            if v.loc['山盘']+v.loc['向盘'] in jiuxingzuhe.index:
                guafu=v.loc['山盘']+v.loc['向盘']
            else: 
                guafu=v.loc['向盘']+v.loc['山盘']    
            word['双星组合']=jiuxingzuhe.loc[guafu].values[1]
            words.update({k[1]:word})
        return words

    '''
    def getExplain(self,fname):
        self.getFigure(fname)
        self.explain['总']={}
        for item in self.geju:
            ind=''
            if item in ['旺山旺水','上山下水','双星会坐','双星会向','全局合十','对宫合十','连珠三般','父母三般','离宫打劫','坎宫打劫']:
                ind=item
            elif '星伏吟' in item:
                ind='全局伏吟'
            elif '星反吟' in item:
                ind='全局反吟'
            elif '伏吟在' in item:
                ind='单宫伏吟'
            elif '反吟在' in item:
                ind='单宫反吟'
            elif '替卦反伏吟' in item:
                ind='全局伏吟'
            elif '文昌' in item:
                ind='文昌'
            self.explain['总'].update({item:gejujieshi.loc[ind].values[0]})
        for k,v in self.pan.iterrows():
            #明确坐向宫位
            if k[1] in [self.zuo,self.xiang]:
                if k[1]==self.zuo:
                    self.explain[k[1]]={'性质':'坐位'}
                elif k[1]==self.xiang:
                    self.explain[k[1]]={'性质':'向位'}
            else:
                self.explain[k[1]]={'性质':'无'}
            #生克比
            self.explain[k[1]].update({'生克比':self.getXingshengkebi(v.loc['山盘'],v.loc['向盘'])})
            if v.loc['山盘']+v.loc['向盘'] in jieshi.index:
                guafu=v.loc['山盘']+v.loc['向盘']
            else: 
                guafu=v.loc['向盘']+v.loc['山盘'] 
            #基于生克比的吉凶
            if self.explain[k[1]]['生克比'] in ['生入','生出','比']:
                self.explain[k[1]]['吉凶']='吉'

            else:
                self.explain[k[1]]['吉凶']='凶'
            #解卦
            self.explain[k[1]].update({'八卦解释':jieshi.loc[guafu].values[0]})
            #九星寓意
            if  self.explain[k[1]]['吉凶']=='吉':           
                self.explain[k[1]].update({'九星寓意':{'山星':jiuxing.loc[v.loc['山盘'],'旺'],'向星':jiuxing.loc[v.loc['向盘'],'衰']}})
            else:
                self.explain[k[1]].update({'九星寓意':{'山星':jiuxing.loc[v.loc['山盘'],'衰'],'向星':jiuxing.loc[v.loc['向盘'],'旺']}})
            #流年
            self.explain[k[1]].update({self.liunian:liunianjiuxing.loc[k[1],self.liunianfeixing.xs(k[1],level='八卦')['流年紫白飞星'].values[0]]})                
    '''
    
    def getExplainFigureFurther(self,fname):
        words=self.getExplainFurther()
        i=0
        edge=130
        img = Image.new('RGB', (edge*4, edge*27), (255,255,255))
        draw = ImageDraw.Draw(img)
        font = ImageFont.truetype("simhei.ttf", 20, encoding="utf-8")
        font1 = ImageFont.truetype("simhei.ttf", 12, encoding="utf-8")
        explains=''
        explains+=self.explainFitfig('看风水盘的原则是各宫的飞星要得令，山向两星的五行要匹配。盘理和环境要搭。\n')
        explains+=self.explainFitfig(self.getGejuexplain()+'\n')
        explains+=self.explainFitfig('文昌位在'+self.wenchangwei+'\n')
        explains+=self.explainFitfig('财位在'+self.caiwei+'\n')
        explains+=self.explainFitfig('该盘九星的得令失令情况如下：\n旺星：%s，\n生气星：%s，\n退气星：%s，\n煞星：%s，\n死星：%s\n'%(self.xingyun['旺'],'、'.join(self.xingyun['生']),self.xingyun['退'],'、'.join(self.xingyun['煞']),'、'.join(self.xingyun['死'])))
        explains+=self.explainFitfig('在下面各宫位的介绍中，除山向两位，其他宫位应视该方位见山还是见水，取是以山为主还是以向为主。\n')

        for gong,word in words.items():
            if self.zuogua==gong:
                explains+=gong+'：山位\n'
                explains+='山向五行：'+word['山向五行']+'\n'
            elif self.xianggua==gong:
                explains+=gong+'：向位'+'\n'
                explains+='向山五行：'+word['向山五行']+'\n'
            else:
                explains+=gong+'：'+'\n'
                explains+='山向五行：'+word['山向五行']+'\n'
                explains+='向山五行：'+word['向山五行']+'\n'
            explains+=self.explainFitfig('本宫山星为:\n'+word['山星'])
            explains+=self.explainFitfig('本宫向星为:\n'+word['向星'])
            explains+=self.explainFitfig('本宫山向两星的组合关系为：')
            explains+=self.explainFitfig(word['双星组合'])
            draw.text((5,i+5),explains,(0,0,0),font=font)
            cnt=explains.count('\n')
            if cnt==0:
                i+=30
            else:
                i+=23*cnt
            explains=''
            
        img.save(userfolder+fname+'解释收费.png') 
    
    def getGejuexplain(self):
        explains=''
        for item in self.geju:
            ind=''
            if item in ['旺山旺水','上山下水','双星会坐','双星会向','全局合十','对宫合十','连珠三般','父母三般','离宫打劫','坎宫打劫']:
                ind=item
            elif '星伏吟' in item:
                ind='全局伏吟'
            elif '星反吟' in item:
                ind='全局反吟'
            elif '伏吟在' in item:
                ind='单宫伏吟'
            elif '反吟在' in item:
                ind='单宫反吟'
            elif '替卦反伏吟' in item:
                ind='全局伏吟'
            elif '文昌' in item:
                ind='文昌'
            if ind in ['旺山旺水','上山下水','双星会坐','双星会向']:
                explains+='此盘为'+ind+'的格局,本身的意义是'+gejujieshi.loc[ind,'解释']+'，但如果峦头不美，吉者不吉，凶者更凶。所以'+gejujieshi.loc[ind,'峦头']
            if ind in ['全局合十','对宫合十','连珠三般','父母三般','离宫打劫','坎宫打劫']:
                explains+='符合%s的格局，所以%s'%(ind,gejujieshi.loc[ind,'解释'])

        return explains

    def getWorkplaceexplain(self,bd=None,gm=None,sqw=None):
        tmpdict=dict.fromkeys('')
        if bd:
            tmpdict['董事长']='董事长办公室的方位应在%s上。办公室的面积不应贪图气派空旷，\
如果没有复杂的功能需要，最好在15-30平米左右。如果有会客功能不受此平米数限制。办公室形状\
应中规中矩，不要奇形怪状，尤其不要在西北方缺角，因为西北是乾位，寓意领导者。办公桌应该\
放在%s上。同时要注意办公桌前的区域应该开阔整洁，因为这是“内明堂”，不要正对门，不要在\
办公室门的右手边。对于董事长的座位设计，一是有靠山，即背后不能玄空，应该倚墙或者高一点的\
柜子;二是不能靠窗而坐；三是不能座位上方有横梁；四是办公室两侧最好左右都有人，是为左辅右弼\
，如果不行，可以右空不可左空；五是办公室门不要正对会议室门、卫生间门、公司大门、尖角。\
如果希望给董事长增加权运，办公桌应该在%s上。如果希望增加贵人运，办公桌应该在%s上。\
如果设计会客空间，主位应该在%s上，客位应该在%s上。'%(self.caiwei.split('， ')[0],bd.minggua['阴阳方'],bd.minggua['化权'],bd.minggua['化科'],''.join(bd.minggua['化吉']),''.join(bd.minggua['化凶']))
        if gm:
            tmpdict['总经理']='董事长办公室的方位应在%s上。办公室的面积不应贪图气派空旷，\
应小于董事长办公室。形状应中规中矩，不要奇形怪状，尤其不要在西北方缺角，因为西北是乾位，\
寓意领导者。办公桌应该放在%s上。同时要注意办公桌前的区域应该开阔整洁，因为这是“内明堂”，\
不要正对门，不要在办公室门的右手边。对于总经理的座位设计，一是有靠山，即背后不能玄空，\
应该倚墙或者高一点的柜子;二是不能靠窗而坐；三是不能座位上方有横梁；四是办公室最好在董事长左右两侧\
，以左为好；五是办公室门不要正对会议室门、卫生间门、公司大门、尖角。如果希望给总经理\
增加权运，办公桌应该在%s上。如果希望增加贵人运，办公桌应该在%s上。如果设计会客空间，\
主位应该在%s上，客位应该在%s上。对于总经理，其椅子最好是有靠背，有扶手的，因为既有靠山，又有辅佐。'%(self.caiwei.split('， ')[0],gm.minggua['阴阳方'],gm.minggua['化权'],gm.minggua['化科'],''.join(gm.minggua['化吉']),''.join(gm.minggua['化凶']))
        tmpdict['业务人员']='大楼坐北朝南，办公区域西南、东南；坐南朝北，西北、东北；\
坐东朝西，西南、西北；坐西朝东，东南、靠近中央；坐东南朝西北，北、西；坐西南朝东北，东、北；\
坐东北朝西南，西、南。'
        tmpdict['文职人员']='大楼坐北朝南，办公区域东北、西；坐南朝北，南、东南；\
坐东朝西，西南、西北；坐西朝东，西南、东北；坐东南朝西北，北、靠近中央；坐西南朝东北，西、北；\
坐西北朝东南，东、南；坐东北朝西南，北、东、东南。'
        if sqw:
            tmpdict['升迁位']=shengqianwei.loc[sqw[0],sqw[1]].values[0]
        return tmpdict

    def combinepic(self,fname):
        edge=120
        img1=Image.open(userfolder+fname+'.png')
        img2=Image.open(userfolder+fname+'解释.png')
        img=Image.new('RGB', (img2.size[0]+30, img1.size[1]+img2.size[1]+30), (255,255,255))
        img.paste(img1,(int(edge/2),15,int(edge/2)+img1.size[0],15+img1.size[1]))
        img.paste(img2,(10,img1.size[1]+30))        
        draw = ImageDraw.Draw(img)
        draw.rectangle((int(edge/2),15,int(edge/2)+img1.size[0],15+img1.size[1]),outline=(0,0,0))
        print(img2.size)
        img.save(userfolder+fname+'公众号.png')
if __name__=='__main__':
    a=Explain([2003,2019,'子','午'],['xx','男',1984,10,2])
    #bd=People('xx','男',1983,10,2)
    #gm=People('yy','男',1976,6,2)
    #print(a.yun,a.getWorkplaceexplain(bd,gm,'子午'))
    #a.getFeixingfigure('xx')
    #a.getExplainfigure('xx')
    #a.combinepic('xx')
    #a.getExplainFigureFurther('xx')
