# -*- coding: utf-8 -*-
"""
Created on Sun Jan 27 16:52:25 2019

@author: asus
"""

from collections import deque as dq
from copy import deepcopy

class Ring():
    def __init__(self,seq):
        self.q=dq(seq)
        
    def indexnew(self,d,v):
        return d.index(v)+1

    def shun(self,add1,add2):
        self.dc=deepcopy(self.q)
        self.dc.rotate(-(self.q.index(add1)))
        self.dc.rotate(-(add2-1))
        return self.dc[0]
    def ni(self,add1,add2):
        self.dc=deepcopy(self.q)
        self.dc.rotate(-(self.q.index(add1)))
        self.dc.rotate(add2-1)
        return self.dc[0]
    def dui(self,v):
        return self.shun(v,int(len(self.q)/2)+1)
    def isDui(self,v1,v2):
        return self.dui(v1)==v2
    
if __name__=='__main__':
    ring=Ring(['壬', '子', '癸', '丑', '艮', '寅', '甲', '卯', '乙', '辰', '巽', '巳', '丙', '午', '丁', '未', '坤', '申', '庚', '酉', '辛', '戌', '乾', '亥'])
    print(ring.q)
    print(ring.isDui('子','午'))
    '''
    for i in range(1,10):
        for j in range(1,10):
            print('%d,%d shun %d ni %d'%(i,j,ring.shun(i,j),ring.ni(i,j)))
    '''