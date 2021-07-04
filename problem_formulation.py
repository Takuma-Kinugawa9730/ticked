# -*- coding: utf-8 -*-
"""
Created on Thu Jul  1 10:14:40 2021

@author: takuma
"""

class ProblemFormulation():
    
    def __init__(self, TDES, hard, soft, L):
        self.L = L
        self.hard_constraint = hard
        self.soft_constraint_list = soft
        self.TDES = TDES