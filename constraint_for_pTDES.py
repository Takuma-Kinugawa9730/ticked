# -*- coding: utf-8 -*-
"""
Created on Fri Jul  2 15:15:46 2021

@author: takuma
"""
HORIZON = 47
def get_constraint(M, W):
   
    """
    M[i,j]（resp. W[i,j]）はi番目のcTDESのj番目のcの値の時の、
    {（実行列に含まれる事象tickの数）+1}*倍率 （resp. 満たしたSoft制約の重要度の合計）
    
    j=0の時、c＝1でSoft制約を無視する
    """
    
    #hard_constraint = ["1", "G", [0,M[0][0]], "F", [0, HORIZON]]
    soft_constraint = []
    
    
    hard_constraint = ["1", "G", [0,M[0][0]], "F", [0, HORIZON],
                       "2", "G", [0,M[1][0]], "F", [0, HORIZON], "&",
                       "3", "G", [0,M[2][0]], "F", [0, HORIZON], "&",
                       "4", "G", [0,M[3][0]], "F", [0, HORIZON], "&"]
    
    
    number_of_cTDES = len(M)
    number_of_c     = len(M[0])
    
    
    
    for index_cDES in range(number_of_cTDES):
        
        for index_C in range(number_of_c):
            
            soft_constraint.append(
                (["{}".format(index_cDES + 1), "G", [0,M[index_cDES][index_C]], "F", [0, HORIZON]],
                 W[index_cDES][index_C]) 
                                  )
    
    #soft_constraint.append((["3", "!", "2", "U",[0, HORIZON]], 1))
    #soft_constraint.append((["2", "!", "3", "U",[0, HORIZON]], 4))
    
    return hard_constraint, soft_constraint