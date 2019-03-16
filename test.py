# -*- coding: utf-8 -*-
"""
Created on Thu Feb  7 10:48:01 2019

@author: asus
""" 
from explain import *

if __name__=='__main__':
    for k,v in diyun.iterrows():
        for i in range(1864,2025,20):
            print(i)
            for j in ['正','兼']:
                if j=='正':
                    a=Explain([i,i+10,k[0],k[1]],['xx','男',1983,10,2])
                    fname=a.yun+'运'+k[0]+'山'+k[1]+'向'
                elif j=='兼':
                    a=Explain([i,i+10,k[0],k[1],' ',' '],['xx','男',1983,10,2])
                    fname=a.yun+'运'+k[0]+'山'+k[1]+'向'+'兼'
                try:
                    a.getFeixingfigure(fname)
                    #a.getExplainfigure(fname)
                    a.getExplainFigureFurther(fname)
                    a.combinepic(fname)
                except:
                    print(fname)