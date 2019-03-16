# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import pandas as pd
from computor import *

datafolder='./data/'
userfolder='./user/'
jieshiwebfolder='./data/解释web/'
shangua=pd.read_excel(datafolder+'风水表.xlsx',sheet_name='山卦',encoding='utf-8',index_col=0,header=0)
gonggua=pd.read_excel(datafolder+'风水表.xlsx',sheet_name='宫卦',encoding='utf-8',index_col=0,header=0)
yuanyun=pd.read_excel(datafolder+'风水表.xlsx',sheet_name='元运',encoding='utf-8',header=0)
dipan=pd.read_excel(datafolder+'风水表.xlsx',sheet_name='地盘',encoding='utf-8',index_col=[2,3],header=0)
shunni=pd.read_excel(datafolder+'风水表.xlsx',sheet_name='顺逆',encoding='utf-8',index_col=0,header=0)
diyun=pd.read_excel(datafolder+'风水表.xlsx',sheet_name='地运',encoding='utf-8',index_col=[0,1],header=0)
dingxiang=pd.read_excel(datafolder+'风水表.xlsx',sheet_name='定向',encoding='utf-8',index_col=0,header=0)
#根据八宅宝镜
minggua=pd.read_excel(datafolder+'风水表.xlsx',sheet_name='命卦',encoding='utf-8',index_col=[0,1],header=0)
shengke=pd.read_excel(datafolder+'风水表.xlsx',sheet_name='生克',encoding='utf-8',index_col=0,header=0)
nianzb=pd.read_excel(datafolder+'风水表.xlsx',sheet_name='年紫白入中',encoding='utf-8',index_col=[0,1],header=0)

caiweizuhe=pd.read_excel(datafolder+'风水表.xlsx',sheet_name='财位飞星组合',encoding='utf-8',index=False,header=0)
bazhai=pd.read_excel(datafolder+'风水表.xlsx',sheet_name='八宅星吉凶',encoding='utf-8',index_col=[0,1],header=0)
shengqianwei=pd.read_excel(datafolder+'风水表.xlsx',sheet_name='升迁位',encoding='utf-8',index_col=[0,1],header=0)

tianganexcel=pd.read_excel(datafolder+'天干.xlsx',encoding='utf-8',index_col=0,header=0)
dizhiexcel=pd.read_excel(datafolder+'地支.xlsx',encoding='utf-8',index_col=0,header=0)
#jieshi=pd.read_excel(datafolder+'解释.xlsx',sheet_name='卦',encoding='utf-8',index_col=0,header=0)
jiuxing=pd.read_excel(datafolder+'解释.xlsx',sheet_name='九星解释',encoding='utf-8',index_col=0,header=0)
jiuxingzuhe=pd.read_excel(datafolder+'解释.xlsx',sheet_name='九星组合解释',encoding='utf-8',index_col=0,header=0)
liunianjiuxing=pd.read_excel(datafolder+'解释.xlsx',sheet_name='流年飞星入宫',encoding='utf-8',index_col=0,header=0)
gejujieshi=pd.read_excel(datafolder+'解释.xlsx',sheet_name='坐向格局',encoding='utf-8',index_col=0,header=0)


#shan=dict(zip(range(1,25),shangua.index.tolist()))
shan=Ring(shangua.index.tolist())
jiu=Ring('一二三四五六七八九')
shudict=dict(zip(list('一二三四五六七八九'),[1,2,3,4,5,6,7,8,9]))
zidict=dict(zip([1,2,3,4,5,6,7,8,9],list('一二三四五六七八九')))
shunnidict=dict(zip(list('阴阳'),list('逆顺')))

tiangan = u'甲|乙|丙|丁|戊|己|庚|辛|壬|癸'.split('|')
tiangan2numDict=dict(zip(tiangan,range(1,11)))
num2tianganDict=dict(zip(range(1,11),tiangan))

dizhi = u'子|丑|寅|卯|辰|巳|午|未|申|酉|戌|亥'.split('|') 
dizhi2numDict=dict(zip(dizhi,range(1,13)))
num2dizhiDict=dict(zip(range(1,13),dizhi))

if __name__=='__main__':
    print(shudict)