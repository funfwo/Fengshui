# -*- coding: utf-8 -*-
"""
Created on Sun Jan 27 19:13:39 2019

@author: asus
"""

from data import *
from collections import OrderedDict as od
from eacal import EACal, lang
import datetime as dt
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont 
from lunardate import LunarDate
import math

c=EACal(zh_s=True)

class Location():
    
    def __init__(self,deg):
        self.zuo=''
        self.xiang=''
        self.jianzuo=None
        self.jianxiang=None
        
        if deg<=352.5 and deg>=7.5:
            #print(1)
            for k,v in dingxiang.iterrows():                
                if v.loc['逆左']<=deg and v.loc['顺右']>=deg:
                    self.zuo=k
                    self.xiang=shan.dui(self.zuo)
                    if v.loc['正左']>=deg:
                        self.jianzuo=shan.ni(self.zuo,2)
                        self.jianxiang=shan.dui(self.jianzuo)
                    elif v.loc['正右']<=deg:
                        self.jianzuo=shan.shun(self.zuo,2)
                        self.jianxiang=shan.dui(self.jianzuo)
        else:
            self.zuo='子'
            self.xiang='午'  
            if 355.5>=deg:
                self.jianzuo=shan.ni(self.zuo,2)
                self.jianxiang=shan.dui(self.jianzuo)
            elif 4.5<=deg:
                self.jianzuo=shan.shun(self.zuo,2)
                self.jianxiang=shan.dui(self.jianzuo)                        
                

class House():
    
    def __init__(self,year,liunian,zuo,xiang,jianzuo=None,jianxiang=None):
        self.year=year
        self.liunian=liunian
        self.liunianyun=self.getLiunianyun(self.liunian)
        self.yun=self.getYuanyun()
        self.zheng,self.ling,self.zhao=self.getSanshen()
        self.zuo,self.xiang=self.getShanxiang(zuo,xiang)
        self.zuogua=shangua.loc[self.zuo,'八卦']
        self.xianggua=shangua.loc[self.xiang,'八卦']
        self.luantou=None
        if jianzuo and jianxiang:
            #self.zuo,self.xiang=self.getShanxiang(jianzuo,jianxiang)
            self.isjian=True
            self.jianzuo=jianzuo
            self.jianxiang=jianxiang
        else:
            self.isjian=False
        self.pan=deepcopy(dipan)
        self.getTianpan()
        self.shanshunni=''
        self.xiangshunni=''
        self.shanshu=self.getShanxiangshu(self.zuo)
        self.xiangshu=self.getShanxiangshu(self.xiang)
        if self.isjian:
            self.getJianshanpan()
            self.getJianxiangpan()
        else:
            self.getShanpan()
            self.getXiangpan()
        self.xingyun=self.getStarsyun()
        self.caiwei=self.getCaiwei()
        self.geju=[]
        self.getGeju()
        self.liunianfeixing=self.getLiunianfeixing()
        self.wenchangwei=''
        self.wenchangwei=self.getWenchangwei()
    def getBybagua(self,bagua):
        return self.pan.xs(bagua,level='八卦')
    def getYuanyun(self):
        cond1=yuanyun.loc[:,'起始']<=self.year
        cond2=yuanyun.loc[:,'终止']>=self.year
        return yuanyun.loc[cond1&cond2]['运'].values[0]
    def getShanxiang(self,zuo,xiang):
        if shan.isDui(zuo,xiang):
            return zuo,xiang
    def feixing(self,pantype,zhong,sn):
        self.pan[pantype]=list(['']*9)
        tmpdict=od.fromkeys(self.pan.index.get_level_values('卦数'))
        for i,v in enumerate(shunni[sn]):
            tmpdict[v]=jiu.shun(zhong,i+1)
        self.pan[pantype]=tmpdict.values()
    def feixing_notpan(self,pantype,zhong,sn):
        tmppan=deepcopy(dipan)
        tmppan[pantype]=list(['']*9)
        tmpdict=od.fromkeys(tmppan.index.get_level_values('卦数'))
        for i,v in enumerate(shunni[sn]):
            tmpdict[v]=jiu.shun(zhong,i+1)
        tmppan[pantype]=tmpdict.values()
        return tmppan
    def shan2gua(self,s):
            return shangua.loc[s,'八卦']
    def shu2gua(self,s):
        if s!='五':
            return gonggua.loc[s,'八卦']
        else:
            return None
    def getGuayinyang(self,gua):
        return gonggua[gonggua['八卦']==gua]['阴阳'].values[0]
    def getTianpan(self):
        self.feixing('天盘',self.yun,'顺')
    def getShanxiangshu(self,zhong):
        #以山星为例，先按二十四山取其在地盘对应的卦，然后按后天八卦取卦数，、
        #最后按此卦数把天盘中对应的飞星找出来，飞星用数字表示
        zuogua=self.shan2gua(zhong)
        dipanguashu=gonggua[gonggua['八卦']==zuogua].index.values[0]
        return self.pan.loc[dipanguashu,'天盘'].values[0]


    def getShunniyinyang(self,zhong,shu):
        tmpbagua=self.shu2gua(shu)
        if tmpbagua:
            tmppan=shangua[shangua['八卦']==tmpbagua]
            tmpxing=tmppan[tmppan['元龙']==shangua.loc[zhong,'元龙']]
            return tmpxing,tmpxing['阴阳'].values[0]
        else:
            return None,shangua.loc[zhong,'阴阳']

    def getShanxiangpan(self,pantype,zhong,shu):
        #以山星为例，把山星数视为后天八卦数，找出对应的八卦，然后在此八卦对应的二十四山中、
        #找出与山星元龙属性相同的对应八卦的阴阳，从而决定顺飞还是逆飞。
        tmpxing,yinyang=self.getShunniyinyang(zhong,shu)
        if pantype=='山盘':
            self.shanshunni=shunnidict[yinyang]
        elif pantype=='向盘':
            self.xiangshunni=shunnidict[yinyang]            
        self.feixing(pantype,shu,shunnidict[yinyang])
    def getJianshanxiangpan(self,pantype,zhong,shu):
        #与正向类似，差异在找替星过程。
        tmpxing,yinyang=self.getShunniyinyang(zhong,shu)
        if tmpxing is None:
            tmpshu=shangua.loc[zhong,'替星']
        else:
            tmpshu=tmpxing['替星'].values[0]
        if pantype=='山盘':
            self.shanshu=tmpshu
        elif pantype=='向盘':
            self.xiangshu=tmpshu                 
        self.feixing(pantype,tmpshu,shunnidict[yinyang])        

    def getShanpan(self):
        self.getShanxiangpan('山盘',self.zuo,self.shanshu)
    def getXiangpan(self):
        self.getShanxiangpan('向盘',self.xiang,self.xiangshu)
    def getJianshanpan(self):
        self.getJianshanxiangpan('山盘',self.zuo,self.shanshu)
    def getJianxiangpan(self):
        self.getJianshanxiangpan('向盘',self.xiang,self.xiangshu)

    def getShanxianglocation(self,shanxiang):
        return self.shan2gua(shanxiang)

    def getStarsyun(self):
        
        tmp=self.pan[['生旺','天盘']]
        tmp=tmp.set_index('生旺')
        yundict=dict.fromkeys(list('旺生死煞退'))
        yundict['旺']=gonggua.loc[tmp.loc['旺'].values.tolist()[0],'九星']
        yundict['退']=gonggua.loc[tmp.loc['退'].values.tolist()[0],'九星']
        yundict['生']=gonggua.loc[[i[0] for i in tmp.loc['生'].values.tolist()],'九星'].values.tolist()
        yundict['煞']=gonggua.loc[[i[0] for i in tmp.loc['煞'].values.tolist()],'九星'].values.tolist()
        yundict['死']=gonggua.loc[[i[0] for i in tmp.loc['死'].values.tolist()],'九星'].values.tolist()

        return yundict
        
    def isWangshanWangshui(self,shanbagua,xiangbagua):

        tmpshanshu=self.getBybagua(shanbagua)['山盘'].values[0]
        tmpxiangshu=self.getBybagua(xiangbagua)['向盘'].values[0]        
        if tmpshanshu==self.yun and tmpxiangshu==self.yun:
            return True,['旺山旺水']
        else:
            return False,['无']
    def isShangshanxiashui(self,shanbagua,xiangbagua):
        tmpshanshu=self.getBybagua(xiangbagua)['山盘'].values[0]
        tmpxiangshu=self.getBybagua(shanbagua)['向盘'].values[0]        
        if tmpshanshu==self.yun and tmpxiangshu==self.yun:
            return True,['上山下水']
        else:
            return False,['无']       
    def isShuangxinghuixiang(self,shanbagua,xiangbagua):
        tmpshanshu=self.getBybagua(xiangbagua)['山盘'].values[0]
        tmpxiangshu=self.getBybagua(xiangbagua)['向盘'].values[0]         
        if tmpshanshu==self.yun and tmpxiangshu==self.yun:
            return True,['双星会向']
        else:
            return False,['无']
    def isShuangxinghuizuo(self,shanbagua,xiangbagua):
        tmpshanshu=self.getBybagua(shanbagua)['山盘'].values[0]
        tmpxiangshu=self.getBybagua(shanbagua)['向盘'].values[0]         
        if tmpshanshu==self.yun and tmpxiangshu==self.yun:
            return True,['双星会坐']
        else:
            return False,['无']  
    def isFufuheshi(self):

        tmppan=deepcopy(self.pan)        
        tmppan['山盘数']=self.pan['山盘'].apply(lambda x:shudict[x])
        tmppan['向盘数']=self.pan['向盘'].apply(lambda x:shudict[x])
        tmppan['天盘数']=self.pan['天盘'].apply(lambda x:shudict[x])
        if (tmppan['山盘数']+tmppan['天盘数']==10).all() or (tmppan['山盘数']+tmppan['向盘数']==10).all() or (tmppan['向盘数']+tmppan['天盘数']==10).all():
            return True,['全局合十']
        elif tmppan.loc[self.shanshu,'天盘数'].values[0]+tmppan.loc[self.xiangshu,'天盘数'].values[0]==10 and tmppan.loc[self.shanshu,'天盘数'].values[0]+tmppan.loc[self.xiangshu,'天盘数'].values[0]==10 and tmppan.loc[self.shanshu,'天盘数'].values[0]+tmppan.loc[self.xiangshu,'天盘数'].values[0]==10:
            return True,['对宫合十']
        else:
            return False,['无']
    def isFuyin(self):
        geju=[]
        #全局伏吟
        if self.shanshu=='五' and (self.pan['山盘']==self.pan['地盘']).any() and self.shanshunni=='顺':
            geju.extend(['山星伏吟'])
        elif self.shanshu=='五' and (self.pan['向盘']==self.pan['地盘']).any() and self.xiangshunni=='顺':
            geju.extend(['向星伏吟'])
        #单宫伏吟
        shandanyin=self.pan[(self.pan['山盘']==self.pan['地盘'])|(self.pan['山盘']==self.pan['地盘'])]
        xiangdanyin=self.pan[(self.pan['向盘']==self.pan['地盘'])|(self.pan['向盘']==self.pan['地盘'])]
        shandanyin=shandanyin.dropna(axis=0)
        xiangdanyin=xiangdanyin.dropna(axis=0)
        if not shandanyin.empty:
            geju.extend(['伏吟在山，宫位在'+''.join(shandanyin.index.get_level_values('八卦').tolist())])
        elif not xiangdanyin.empty:
            geju.extend(['伏吟在向，宫位在'+''.join(xiangdanyin.index.get_level_values('八卦').tolist())])            
        if geju:
            return True,geju
        else:
            return False,['无']
    def isFanyin(self):
        geju=[]
        #全局反吟
        if self.shanshu=='五' and (self.pan['山盘']==self.pan['地盘']).any() and self.shanshunni=='逆':
            geju.extend(['山星伏吟'])
        elif self.shanshu=='五' and (self.pan['向盘']==self.pan['地盘']).any() and self.xiangshunni=='逆':
            geju.extend(['向星伏吟'])
        #单宫反吟，注意与单宫伏吟规则不同
        tmppan=deepcopy(self.pan)        
        tmppan['山盘数']=self.pan['山盘'].apply(lambda x:shudict[x])
        tmppan['向盘数']=self.pan['向盘'].apply(lambda x:shudict[x])
        tmppan['地盘数']=self.pan['地盘'].apply(lambda x:shudict[x])
        tmppan['山地合十']=tmppan['山盘数']+tmppan['地盘数']
        tmppan['向地合十']=tmppan['向盘数']+tmppan['地盘数']

        shandanyin=tmppan[tmppan['山地合十']==10]
        xiangdanyin=tmppan[tmppan['向地合十']==10]
        shandanyin=shandanyin.dropna(axis=0)
        xiangdanyin=xiangdanyin.dropna(axis=0)
        if not shandanyin.empty:
            geju.extend(['反吟在山，宫位在'+''.join(shandanyin.index.get_level_values('八卦').tolist())])
        elif not xiangdanyin.empty:
            geju.extend(['反吟在向，宫位在'+''.join(xiangdanyin.index.get_level_values('八卦').tolist())])            
        if geju:
            return True,geju
        else:
            return False,['无']
    def isJianfufanyin(self):
        if self.isjian and self.yun=='五':
            if self.zuo+self.xiang in '乾巽 巽乾 亥巳 巳亥 辰戌 戌辰'.split():
                return True,['替卦反伏吟']
            else:
                return False,['无']
        else:
            return False,['无']        
    def isLianzhusanban(self):
        lianzhu=sorted([shudict[self.yun],shudict[self.shanshu],shudict[self.xiangshu]])
        if lianzhu[1]-lianzhu[0]==1 and lianzhu[2]-lianzhu[1]==1:
            return True,['连珠三般']
        else:
            return False,['无']
    def isFumusanban(self):
        lianzhu=sorted([shudict[self.yun],shudict[self.shanshu],shudict[self.xiangshu]])
        if lianzhu[1]-lianzhu[0]==3 and lianzhu[2]-lianzhu[1]==3:
            return True,['父母三般']
        else:
            return False,['无']
    def isLigongdajie(self,shanbagua,xiangbagua):
        tmpxiangshu=self.getBybagua(xiangbagua)['向盘'].values[0]        
        xiangsanban=bool()
        shansanban=bool()
        if tmpxiangshu==self.yun:
            qianxiang=self.getBybagua('乾')['向盘'].values[0]
            lixiang=self.getBybagua('离')['向盘'].values[0]
            zhenxiang=self.getBybagua('震')['向盘'].values[0]
            xianglianzhu=sorted([shudict[qianxiang],shudict[lixiang],shudict[zhenxiang]])
            if xianglianzhu[1]-xianglianzhu[0]==3 and xianglianzhu[2]-xianglianzhu[1]==3:
                xiangsanban=True
            qianshan=self.getBybagua('乾')['山盘'].values[0]
            lishan=self.getBybagua('离')['山盘'].values[0]
            zhenshan=self.getBybagua('震')['山盘'].values[0]
            shanlianzhu=sorted([shudict[qianshan],shudict[lishan],shudict[zhenshan]])
            if shanlianzhu[1]-shanlianzhu[0]==3 and shanlianzhu[2]-shanlianzhu[1]==3:
                shansanban=True
            if xiangsanban and shansanban and xianglianzhu==shanlianzhu:
                return True,['离宫打劫']
            else:
                return False,['无']
        else:
            return False,['无']
    def isKangongdajie(self,shanbagua,xiangbagua):
        tmpxiangshu=self.getBybagua(xiangbagua)['向盘'].values[0]
        xiangsanban=bool()
        shansanban=bool()
        if tmpxiangshu==self.yun:
            qianxiang=self.getBybagua('巽')['向盘'].values[0]
            lixiang=self.getBybagua('坎')['向盘'].values[0]
            zhenxiang=self.getBybagua('兑')['向盘'].values[0]
            xianglianzhu=sorted([shudict[qianxiang],shudict[lixiang],shudict[zhenxiang]])
            if xianglianzhu[1]-xianglianzhu[0]==3 and xianglianzhu[2]-xianglianzhu[1]==3:
                xiangsanban=True
            qianshan=self.getBybagua('巽')['山盘'].values[0]
            lishan=self.getBybagua('坎')['山盘'].values[0]
            zhenshan=self.getBybagua('兑')['山盘'].values[0]
            shanlianzhu=sorted([shudict[qianshan],shudict[lishan],shudict[zhenshan]])
            if shanlianzhu[1]-shanlianzhu[0]==3 and shanlianzhu[2]-shanlianzhu[1]==3:
                shansanban=True
            if xiangsanban and shansanban and xianglianzhu==shanlianzhu:
                return True,['坎宫打劫']
            else:
                return False,['无']
        else:
            return False,['无']
    def isRuqiushan(self):
        if self.yun!='五':
            if not self.isjian:
                if shudict[self.yun]+1==shudict[self.shanshu]:
                    return True
                else:
                    return False
            else:
                if shudict[self.yun]==shudict[self.shanshu]:
                    return True
                else:
                    return False            
    def isRuqiuxiang(self):
        if self.yun!='五':
            if not self.isjian:
                if shudict[self.yun]+1==shudict[self.xiangshu]:
                    return True
                else:
                    return False
            else:
                if shudict[self.yun]==shudict[self.xiangshu]:
                    return True
                else:
                    return False            
    def getWenchangwei(self):
        tmppan=deepcopy(self.pan)
        tmppan=tmppan[['天盘','山盘','向盘']]
        tmppan['三盘数']=tmppan['天盘']+tmppan['山盘']+tmppan['向盘']
        tmppan=tmppan[tmppan['三盘数'].str.contains('一四')|tmppan['三盘数'].str.contains('四一')]
        tmppan=tmppan.dropna()
        words=[]
        if not tmppan.empty:
            words=''.join(tmppan.index.get_level_values('八卦').tolist())
        if words:
            if '巽' in words:
                return words
            else:
                return '巽'+words
        else:
            return '巽'

    def getCaiwei(self):
        shengwang=[v[0] for k,v in self.xingyun.items() if k in ['生','旺']]
        cond1=self.pan['向盘'].isin(shengwang)
        
        tmp=self.pan['向盘'][cond1]
        tmp=self.pan.loc[tmp.index,['天盘','山盘','向盘']]
        tmp['山向']=tmp['山盘']+tmp['向盘']
        tmp['山向list']=tmp['山向'].apply(lambda x:list(x))
        caiweizuhe['组合list']=caiweizuhe['组合'].apply(lambda x:list(x))
        caiwei=[]
        zuhe=[]
        for k,v in tmp['山向list'].iteritems():
            if v in caiweizuhe['组合list'].tolist():
                caiwei.extend(k[1])
                if v[0]+v[1] in caiweizuhe['组合'].tolist():
                    zuhe.extend(caiweizuhe[caiweizuhe['组合']==v[0]+v[1]]['解释'])
                else:
                    zuhe.extend(caiweizuhe[caiweizuhe['组合']==v[1]+v[0]]['解释'])
        
        if caiwei:
            total=zip(caiwei,zuhe)
            words=[i[0]+'，'+i[1] for i in total]
            return ';'.join(words)
        else:
            caiwei=[i[1] for i in tmp.index.values]
            return '、'.join(caiwei)+'，但财位相对强度弱'
        

    def isGeju(self,*args):
        if args[0][0]:
            self.geju.extend(args[0][1])
    def getGeju(self):
        shanbagua=self.getShanxianglocation(self.zuo)
        xiangbagua=self.getShanxianglocation(self.xiang)
        self.isGeju(self.isWangshanWangshui(shanbagua,xiangbagua))
        self.isGeju(self.isShangshanxiashui(shanbagua,xiangbagua))
        self.isGeju(self.isShuangxinghuixiang(shanbagua,xiangbagua))
        self.isGeju(self.isShuangxinghuizuo(shanbagua,xiangbagua))
        self.isGeju(self.isFufuheshi())
        self.isGeju(self.isFuyin())
        self.isGeju(self.isFanyin())
        self.isGeju(self.isJianfufanyin())
        self.isGeju(self.isLigongdajie(shanbagua,xiangbagua))
        self.isGeju(self.isKangongdajie(shanbagua,xiangbagua))
    def getLiunianyun(self,liunian):
            for i in range(9):
                if liunian>=yuanyun.loc[i,'起始'] and liunian<=yuanyun.loc[i,'终止']:
                    return yuanyun.loc[i,'运']         
    def getLiunianfeixing(self):
        return self.feixing_notpan('流年紫白飞星',nianzb.loc[c.get_cycle_ymd(dt.datetime(self.liunian,4,1))[0],self.liunianyun].values[0],'顺')
    def getSanshen(self):
        zheng=self.yun
        ling=zidict[10-shudict[zheng]]
        zhao1,zhao2=jiu.shun(ling,2),jiu.ni(ling,2)
        return zheng,ling,(zhao1,zhao2)
    def getShengkebi(self,zhu,ke):
        if shengke.loc[zhu,'生']==ke:
            return '生入'
        elif shengke.loc[zhu,'克']==ke:
            return '克入'        
        elif shengke.loc[ke,'生']==zhu:
            return '生出'
        elif shengke.loc[ke,'克']==zhu:
            return '克出'
        elif zhu==ke:
            return '比'
    def getXingshengkebi(self,zhuxing,kexing):
        zhu=gonggua.loc[zhuxing,'五行']
        ke=gonggua.loc[kexing,'五行']
        skb=self.getShengkebi(zhu,ke)
        return zhu,ke,skb


class People():
    def __init__(self,name,gender,year,month,day,hour=0):
        
        self.name=name
        self.gender=gender
        self.birthday=c.get_cycle_ymd(dt.datetime(year,month,day))        
        tmpbirthday=c.get_cycle_ymd(dt.datetime(year,1,1))
        if tmpbirthday==self.birthday[0]:
            for i in [0,3,6]:
                if year-1>=yuanyun.loc[i,'起始'] and year-1<=yuanyun.loc[i+2,'终止']:
                    self.yuan=yuanyun.loc[i,'元']
        else:
            for i in [0,3,6]:
                if year>=yuanyun.loc[i,'起始'] and year<=yuanyun.loc[i+2,'终止']:
                    self.yuan=yuanyun.loc[i,'元']            
        self.minggua=self.getBazhai()
        self.birthdayfull=self.getbirthday(year,month,day,hour,'阳历')
        self.sizhu=self.get_sizhu(self.birthdayfull)

    def getBazhai(self):
        mingguadict=dict.fromkeys('命卦 配卦 阴阳方 八宅星 化权 化科 化吉 化凶'.split())
        mingguadict['命卦']=minggua.loc[self.yuan,self.birthday[0]][self.gender]
        if mingguadict['命卦'] in '坎离震巽'.split():
            mingguadict['配卦']='东四命'
            mingguadict['阴阳方']='乾坎艮震'
        else:
            mingguadict['配卦']='西四命'
            mingguadict['阴阳方']='巽离坤兑'
        mingguadict['八宅星']=bazhai.loc[mingguadict['命卦']]
        mingguadict['化权']=mingguadict['八宅星'][mingguadict['八宅星']=='延年'].dropna().index.values[0]
        mingguadict['化科']=mingguadict['八宅星'][mingguadict['八宅星']=='天医'].dropna().index.values[0]
        mingguadict['化吉']=mingguadict['八宅星'][mingguadict['八宅星'].isin(['生气','延年','天医'])].dropna().index.values.tolist()
        mingguadict['化凶']=mingguadict['八宅星'][mingguadict['八宅星'].isin(['伏位','五鬼','六煞','绝命','祸害'])].dropna().index.values.tolist()
        
        return mingguadict


    def getbirthday(self,year,month,day,hour,birthdaytype):
    
        f=open(datafolder+'万年历.txt')
        cal=pd.read_csv(f,header=0,index_col=0,encoding='utf-8')
        if birthdaytype=='阳历':
            l=cal.loc[dt.date(year,month,day).strftime('%Y-%m-%d')]
            
            return {'阳历':dt.datetime(year,month,day,hour),\
                    '阴历':{'生日':[l[0],l[1],l[2],hour]}
                    }
        elif birthdaytype=='阴历':
    
            l=LunarDate(year,month,day,isLeapMonth).toSolarDate()
            return {'阳历':dt.datetime(l[0],l[1],l[2],hour),\
                    '阴历':{'生日':[year,month,day,hour]}
                    }

    def get_sizhu(self,t):
        yanli=t['阳历']
        year_zhu,month_zhu,day_zhu=c.get_cycle_ymd(yanli)
        yinli=t['阴历']['生日']
        year_zhu=c.get_cycle_year(yinli[0])
        '''
        month_tg=2*tiangan2numDict[year_zhu[0]]+yint.month
        if month_tg<=10:
                t_tg=num2tianganDict[month_tg]
            else:
                t_tg=num2tianganDict[month_tg%10]
        month_dz=num2numDict[yint.month]
        '''
        t_dz=num2dizhiDict[math.ceil(yinli[3]/2)+1]
        tmp=math.ceil(yinli[3]/2)+tiangan2numDict[day_zhu[0]]*2-1
    
        t_tg=num2tianganDict[self.TianganCycleCheck(tmp)]
        return [year_zhu,month_zhu,day_zhu,t_tg+t_dz]
    
    def TianganCycleCheck(self,num):
        if num==10:
            return 10
        elif num%10==0:
            return 10
        elif num<10 and num>0:
            return num
        elif num<0 and num>-10:
            return num+10
        elif num<-10 and num>-20:
            return num+20
        else:
            return num%10
        
    def sizhuwuxing(self):
        swxdict=dict()
        index='年月日时'
        for i,item in enumerate(self.sizhu):
            swxdict.update({index[i]:{'天干':tianganexcel.loc[item[0],'五行'],'地支':dizhiexcel.loc[item[1],'五行']}})
        swxdf=pd.DataFrame.from_dict(swxdict,orient='index')
        wxdict=dict.fromkeys(list('木火土金水'))
        values=swxdf.values.reshape(1,-1).tolist()[0]
        wxdict['木']=values.count('木')
        wxdict['火']=values.count('火')
        wxdict['土']=values.count('土')
        wxdict['金']=values.count('金')
        wxdict['水']=values.count('水')
        wxser=pd.Series(wxdict)
        wxser.sort_values(inplace=True)
        if wxser.iloc[0:4].sum()==0:
            return wxser.index[0],wxser.index[1],wxser.index[2],wxser.index[3]
        elif wxser.iloc[0:3].sum()==0:
            return wxser.index[0],wxser.index[1],wxser.index[2]
        elif wxser.iloc[0:2].sum()==0:
            return wxser.index[0],wxser.index[1]
        else:
            return wxser.index[0]
        
if __name__=='__main__':
    #l=Location(35)
    #print(l.zuo,l.xiang,l.jianzuo,l.jianxiang)
    #a=House(1963,2013,'坤','艮')
    #a=House(2004,2013,'乙','辛')
    #print(a.pan['生旺'],a.xingyun)

    b=People('xx','男',1985,10,2,14)
    b.sizhuwuxing()
    #print(b.birthday,b.yuan,b.minggua)
    #a.getFigure()