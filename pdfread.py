# -*- coding: utf-8 -*-
"""
Created on Sat Feb  9 10:46:08 2019

@author: asus
"""

from pdfminer.pdfinterp import PDFResourceManager,process_pdf
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from io import StringIO


def readPDF(fname):
    file=open(fname,'rb')
    
    rsrcmgr=PDFResourceManager()
    retstr=StringIO()
    laparams=LAParams()
    device=TextConverter(rsrcmgr,retstr,laparams=laparams)
    process_pdf(rsrcmgr,device,file)
    device.close()
    content=retstr.getvalue()
    retstr.close()
    strs=str(content).split('\n')
    print(strs)

if __name__=='__main__':
    readPDF('./资料/玄空飞星二十四山九运挨星下卦以及替卦图和详解.pdf')