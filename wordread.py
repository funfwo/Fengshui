# -*- coding: utf-8 -*-
"""
Created on Sat Feb  9 11:20:06 2019

@author: asus
"""

import docx
import re
import pandas as pd
def readWord(fname):
    file=docx.Document(fname)
    
    patt=dict()
    patt.update({0:re.compile('([\u4e00-\u9fa5]山[\u4e00-\u9fa5]向)([\u4e00-\u9fa5]卦)（([\u4e00-\u9fa5]运)）.*')})
    jieshi=dict()
    for para in file.paragraphs:
        text=para.text
        line=re.findall(patt[0],text)
        if text.strip():
            if line:
                line=line[0]
                title=line[2]+line[0]+line[1]
                print(title)
                cnt=0
                pa=[]
            else:
                if cnt<=3:
                    pa.append(text)
                    cnt+=1
                if cnt==4:
                    jieshi.update({title:pa})   
    pd.DataFrame.from_dict(jieshi,orient='index').to_excel('./资料/飞行盘解释.xlsx',encoding='utf-8')        
            
def jieshiweb():
    tmp=pd.read_excel('./data/解释web/飞行盘解释.xlsx',encoding='utf-8',index_col=0)
    for k,v in tmp.iterrows():
        ser=v.loc[1].strip()+'\n'+v.loc[2].strip()+'\n'+v.loc[3].strip()
        with open('./data/解释web/'+k+'.txt','w',encoding='utf-8') as f:
            f.write(ser)          
if __name__=='__main__':
    jieshiweb()