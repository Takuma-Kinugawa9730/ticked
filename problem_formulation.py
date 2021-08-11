# -*- coding: utf-8 -*-
"""
Created on Thu Jul  1 10:14:40 2021

@author: takuma
"""
import translate_des_to_tdes

"""
pDES(top-level DES)
"""
import pDES
import constr_for_pTDES

"""
middle-level DES
"""
import DES_1
import DES_2
import DES_3
import constr_for_TDES_1
import constr_for_TDES_2
import constr_for_TDES_3

"""
lowest-level DES
"""
import DES_1_1
import DES_2_1
import DES_3_1
import DES_3_2
import constr_for_TDES_1_1
import constr_for_TDES_2_1
import constr_for_TDES_3_1
import constr_for_TDES_3_2


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

    p_f_list = []
    
    
    
    """
    lowest-level TDESについて、入力情報を読み取る
    """
    
    p_f_list_for_lowest =[]
    
    problem_formulation = ProblemFormulation(translate_des_to_tdes.get_TDES(DES_1_1.get_DES()), 
                                             constr_for_TDES_1_1.get_hard_constraint(), constr_for_TDES_1_1.get_soft_constraint(), 
                                             constr_for_TDES_1_1.HORIZON)
    p_f_list_for_lowest.append(problem_formulation)
    
    """
    problem_formulation = ProblemFormulation(translate_des_to_tdes.get_TDES(DES_2_1.get_DES()), 
                                             constr_for_TDES_2_1.get_hard_constraint(), constr_for_TDES_2_1.get_soft_constraint(), 
                                             constr_for_TDES_2_1.HORIZON)
    p_f_list_for_lowest.append(problem_formulation)
    
    
    problem_formulation = ProblemFormulation(translate_des_to_tdes.get_TDES(DES_3_1.get_DES()), 
                                             constr_for_TDES_3_1.get_hard_constraint(), constr_for_TDES_3_1.get_soft_constraint(), 
                                             constr_for_TDES_3_1.HORIZON)
    p_f_list_for_lowest.append(problem_formulation)
    
    
    problem_formulation = ProblemFormulation(translate_des_to_tdes.get_TDES(DES_3_2.get_DES()), 
                                             constr_for_TDES_3_2.get_hard_constraint(), constr_for_TDES_3_2.get_soft_constraint(), 
                                             constr_for_TDES_3_2.HORIZON)
    p_f_list_for_lowest.append(problem_formulation)
    """
    
    
    p_f_list.append(p_f_list_for_lowest)
        
     
    """
    middle-level TDESについて、入力情報を読み取る
    """
    
    p_f_list_for_middle =[]
    
    problem_formulation = ProblemFormulation(translate_des_to_tdes.get_TDES(DES_1.get_DES()), 
                                             constr_for_TDES_1.get_hard_constraint(), constr_for_TDES_1.get_soft_constraint(), 
                                             constr_for_TDES_1.HORIZON)
    p_f_list_for_middle.append(problem_formulation)
    
    """
    problem_formulation = ProblemFormulation(translate_des_to_tdes.get_TDES(DES_2.get_DES()), 
                                             constr_for_TDES_2.get_hard_constraint(), constr_for_TDES_2.get_soft_constraint(), 
                                             constr_for_TDES_2.HORIZON)
    p_f_list_for_middle.append(problem_formulation)
    
    
    problem_formulation = ProblemFormulation(translate_des_to_tdes.get_TDES(DES_3.get_DES()), 
                                             constr_for_TDES_3.get_hard_constraint(), constr_for_TDES_3.get_soft_constraint(), 
                                             constr_for_TDES_3.HORIZON)
    p_f_list_for_middle.append(problem_formulation)
    """
    
    p_f_list.append(p_f_list_for_middle)
    
    
    
    """
    top-level TDESについて、入力情報を読み取る
    """
    
    p_f_list_for_top =[]
    problem_formulation = ProblemFormulation(translate_des_to_tdes.get_TDES(pDES.get_DES()), 
                                             constr_for_pTDES.get_hard_constraint(), constr_for_pTDES.get_soft_constraint(), 
                                             constr_for_pTDES.HORIZON)
    p_f_list_for_top.append(problem_formulation)
    
    
    p_f_list.append(p_f_list_for_top)
    
     
    
    return p_f_list
    