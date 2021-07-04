# -*- coding: utf-8 -*-
"""
Created on Fri Jul  2 15:15:46 2021

@author: takuma
"""
HORIZON = 5
def get_constraint(M, W):
    """
    原子命題　0　は、Trueを表す
    """
    
    """
    M[i,j]はi番目のcTDESのj番目のαの値の時の、（実行列に含まれる事象tickの数）+1
    """
    
    """
    hard_constraint = ['A', 'F', [M[1][1], M[1][1]+2], 
                       'A','&']
    """
    hard_constraint = ['A']
    soft_constraint = [(['A', 'G', [M[0][0], M[0][0]+2]], W[1][0]), 
                       (['A'], W[1][0]+3)]
    
    return hard_constraint, soft_constraint