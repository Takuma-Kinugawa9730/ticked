# -*- coding: utf-8 -*-
"""
Created on Fri Jul  2 09:02:36 2021

@author: takuma
"""

import gurobipy as gp#


class test():
    
    def __init__(self):
        
        self.a=0
        self.b=0
        

def hoge(a,b):
    
    return (a,b,a+b)


if	__name__ == '__main__':
    
    
    m = gp.Model("test")
    
    z_e = m.addVar(vtype=gp.GRB.CONTINUOUS, name = "z_e")
    
    m.addConstr(z_e >= 0)
    
    m.setObjective(z_e*2, gp.GRB.MINIMIZE)
    
    m.update()
    m.optimize()
    print(z_e.x)
    print("\n---------------------\n")
   #$ m.reset(0)
    
    m.addConstr(z_e >= 3)
    
    m.setObjective(z_e*3, gp.GRB.MINIMIZE)
    
    m.update()
    m.optimize()
    print(z_e.x)
    