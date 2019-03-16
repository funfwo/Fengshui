# -*- coding: utf-8 -*-
"""
Created on Sun Jan 27 14:31:21 2019

@author: asus
"""

import requests
from bs4 import BeautifulSoup as bs
import re

r=requests.get('http://fate.china95.net/xuankong/index.aspx')
print(r.status_code)
r=r.text

vs=re.findall(r'<input type="hidden" name="__VIEWSTATE" id="__VIEWSTATE" value="(.*?)" />',r)
vg=re.findall(r'<input type="hidden" name="__VIEWSTATEGENERATOR" id="__VIEWSTATEGENERATOR" value="(.*?)" />',r)
ev=re.findall(r'<input type="hidden" name="__EVENTVALIDATION" id="__EVENTVALIDATION" value="(.*?)" />',r)
print(vs[0],'\n',vg[0],'\n\n',ev[0])
payload={'DropDownList1':'辛山乙向','DropDownList2':'八运','cmbOK':'确定',\
         '__VIEWSTATE':vs[0],'__VIEWSTATEGENERATOR':vg[0],'__EVENTVALIDATION':ev[0],'AiXing':'RB_Xia'}
r=requests.post('http://fate.china95.net/xuankong/index.aspx',data=payload)

print(r.text)