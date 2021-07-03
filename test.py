# -*- coding: utf-8 -*-
"""
Created on Fri Jul  2 09:02:36 2021

@author: takuma
"""

class test():
    
    def __init__(self):
        
        self.a=0
        self.b=0
        

def hoge(a,b):
    
    return (a,b,a+b)


if	__name__ == '__main__':
    
    tup = (1,2)
    tup2 = hoge(tup[0],tup[1])
    print(tup2)