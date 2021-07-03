# -*- coding: utf-8 -*-
"""
Created on Fri Jul  2 15:15:46 2021

@author: takuma
"""
HORIZON = 20
def get_constraint(M, W):
    """
    原子命題　0　は、Trueを表す
    """
    
    """
    M[i,j]はi番目のcTDESのj番目のαの値の時の、（実行列に含まれる事象tickの数）+1
    """
    hard_constraint = ['0', '1', 'U', [M[2,4], M[2,4]+2], #== F_[M[2,4], M[2,4]+2] '1'
                       '2','&']
    
    soft_constraint = [(['0', '2', '!', 'U', [M[2,4], M[2,4]+2], '!'], W[2,2]), # == G_[M[2,4], M[2,4]+2] '2'
                       (['3'], W[1,2]+3)]
    
    return hard_constraint, soft_constraint