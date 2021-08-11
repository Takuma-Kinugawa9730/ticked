# -*- coding: utf-8 -*-
"""
Created on Thu Jul  1 10:14:40 2021

@author: takuma
"""
import translate_des_to_tdes

"""
pDES(top-level DES)
"""
import DES_for_compare_plane as DES


HORIZON = 40

def get_hard_constraint(AP):
    
    
    hard_constraint = ['0', 'F', [0, HORIZON]]

    return hard_constraint

def get_soft_constraint(AP):
    """
    soft_constraint = [(['2', '!', '1', 'U', [0, HORIZON]], 1),
                       (['1_1', '!', '1_0', 'U', [0, HORIZON]], 1),
                       (['1_0_1', '!', '1_0_1', 'U', [0, HORIZON]], 1),
                       (['1_1_1', '!', '1_1_0', 'U', [0, HORIZON]], 1),
                       (['0_1', '!', '0_0', 'U', [0, HORIZON]], 1),
                       (['0_0_1', '!', '0_0_0', 'U', [0, HORIZON]], 1),
                       (['0_1_1', '!', '0_1_0', 'U', [0, HORIZON]], 1),
                       (['2_1', '!', '2_0', 'U', [0, HORIZON]], 1),
                       (['2_0_1', '!', '2_0_1', 'U', [0, HORIZON]], 1),
                       (['2_1_1', '!', '2_1_0', 'U', [0, HORIZON]], 1),
                       ]
    """
    soft_constraint = [(['1_1', '!', '1_0', 'U', [0, HORIZON]], 1),
                       (['1_0_1', '!', '1_0_1', 'U', [0, HORIZON]], 1),
                       (['1_1_1', '!', '1_1_0', 'U', [0, HORIZON]], 1),
                       (['0_1', '!', '0_0', 'U', [0, HORIZON]], 1),
                       (['0_0_1', '!', '0_0_0', 'U', [0, HORIZON]], 1),
                       (['0_1_1', '!', '0_1_0', 'U', [0, HORIZON]], 1),
                       ]
    for index_ap in range(1, len(AP)):
        soft_constraint.append( ([AP(index_ap), 'F', [0, HORIZON]], 1) )
    

    return soft_constraint

"""
問題設定に必要な情報を保持するクラス
"""
class ProblemFormulation():
    
    def __init__(self,TDES, hard, soft, HORIZON):
        self.TDES = TDES
        self.hard_constraint = hard
        self.soft_constraint_list = soft
        self.HORIZON = HORIZON
        
def set_problem_formulation():      

    TDES = translate_des_to_tdes.get_TDES(DES.get_DES())

    p_f = ProblemFormulation(TDES, get_hard_constraint(TDES.ap), get_soft_constraint(TDES.ap), HORIZON)
    
    p_f_list = [[p_f]]
   
     
    
    return p_f_list
    