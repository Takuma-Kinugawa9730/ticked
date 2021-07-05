# -*- coding: utf-8 -*-

import gurobipy as gp#


import time
import datetime
import os
import translate_des_to_tdes
import encoder_main
import numpy as np
import csv
"""
pDES
"""
import pDES
import constraint_for_pTDES
"""
cDES
"""
import cDES_1
import cDES_2
import constr_for_cTDES_1
import constr_for_cTDES_2



"""
問題設定に必要な情報を保持するクラス
"""
class ProblemFormulation():
    
    def __init__(self,TDES, hard, soft, HORIZON):
        self.TDES = TDES
        self.hard_constraint = hard
        self.soft_constraint_list = soft
        self.HORIZON = HORIZON
        

"""
実行列のi番目の状態を表すw[i,]と、j番目の事象がtickなら1を持つz_e[j]を導入
"""
def get_variable_for_execution(m, HORIZON, size_of_state, index_initial_state,
                                 adjacency_matrix, alpha, beta):

    z_e = m.addMVar(HORIZON-1,vtype=gp.GRB.BINARY, name = "z_e")
    w = m.addMVar((HORIZON, size_of_state),vtype=gp.GRB.BINARY, name = "w")
    
    
    """
    二値変数z_eについて制約を加える
    """
       
    for i in range(HORIZON-1):
        sum2 = 0
        sum1 = 0
        for j in range(size_of_state):
        
            sum1 += w[i,j]*alpha[j]
            sum2 += w[i+1,j]*beta[j]
        
        m.addConstr(z_e[i] <= sum1)
        m.addConstr(z_e[i] <= sum2)
        m.addConstr(z_e[i] >= -1 + sum1 + sum2)
       
    """
    二値変数wについて制約を加える
    """
    m.addConstrs(w[h,].sum() == 1 for h in range(HORIZON))
    m.addConstr(w[0, index_initial_state] == 1)
    Sum = 0
    for i in range(HORIZON-1):
        for j in range(size_of_state):
            Sum = 0
            for k in range(size_of_state):

                Sum += w[i,k]*adjacency_matrix[k][j]
            
            m.addConstr(w[i+1,j] <= Sum)
            
    return z_e, w
      
def output_result(TDES, z_e, w, len_hard_constraint, encoder_hard):

    """
    実行列をテキストファイルで出力
    """
    f=open(dir_path + TDES.name + "_c-{}_".format(c) + 'execution_state.txt', 'w')
    for h in range(HORIZON):
        for index_state in range(len(TDES.s)):
            if w.X[h, index_state] == 1:
                break
        
        if index_state > len(TDES.s):
            print("ERROR.")
        else:    
            f.write("h:{0}, state(DES):{1}, state(TDES):{2}\n".format(
                    h, TDES.s[index_state][0], TDES.s[index_state])
                    )
    f.close()

    """
    二値変数zの値を出力
    """
    with open(dir_path + TDES.name + '_c-{}_'.format(c) + 'z.csv', 'w') as f:
        writer = csv.writer(f)
        for index_fml in range(len_hard_constraint):
            writer.writerow(encoder_hard.z[index_fml].X)
  
    """
    二値変数z_eの値を出力
    """
    with open(dir_path + TDES.name + '_c-{}_'.format(c) + 'z_e.csv', 'w') as f:
        writer = csv.writer(f)
        for index_fml in range(len_hard_constraint):
            writer.writerow(z_e.X)
      
        
"""
実際の実行列を求める
戻り値＝（事象tickの数：m、Soft制約の重要度の合計：w）
"""

def get_execution(TDES, hard_constraint, soft_constraint_list, HORIZON, c, dir_path):
    
    LARGE_NUMBER = 100
    
    f_record=open(dir_path + TDES.name + '_time_record.txt', 'w')
    
    
    m = gp.Model("Planning for TDES:{0} c:{1}".format(TDES.name, c))
    m.Params.LogFile = dir_path +"Log.txt"

    """
    ラベル関数の行列、遷移関数の行列、事象tickに関するベクトルを手に入れる
    """    
    label_matrix = TDES.get_label_matrix()
    (adjacency_matrix, alpha, beta) = TDES.get_transition_matrix()

    """
    二値変数を用意    
    """        
    (z_e, w) = get_variable_for_execution(m, HORIZON, len(TDES.s), TDES.s.index(TDES.istate),
                                            adjacency_matrix, alpha, beta)
    
    
    """
    Hard制約をエンコード
    """    
    print(hard_constraint)    
    encoder_hard = encoder_main.EncoderBool(hard_constraint)
    
    start = time.time()
    encoder_hard.start_encodeing(m, HORIZON, TDES, label_matrix, z_e, w, TDES.ap)
    finish = time.time() - start
    f_record.write("time to encode hard constraint, {}\n".format(finish))
    
    if type(hard_constraint[-1])==list:
        m.addConstr(encoder_hard.z[-2,0] == 1) 
    else:
        m.addConstr(encoder_hard.z[-1,0] == 1)
      
    
    """
    Soft制約をエンコード
    """    
    part_of_obj_function = 0
    for (soft_constraint, weight) in soft_constraint_list:
        print(soft_constraint, weight)
        encoder = encoder_main.EncoderBool(soft_constraint)
        
        start = time.time()
        encoder.start_encodeing(m, HORIZON, TDES, label_matrix, z_e, w, TDES.ap)
        finish = time.time() - start
        f_record.write("time to encode soft constraint, {}\n".format(finish))
            
            
        """
        Soft制約の重みの合計を目的関数に使うため、ここでその式を入手する
        """    
        if type(soft_constraint[-1]) == list:
            part_of_obj_function = part_of_obj_function + encoder.z[-2,0]*weight
        else:
            part_of_obj_function = part_of_obj_function + encoder.z[-1,0]*weight
        
    m.update() 
    
    
    """
    事象tickの合計数を目的関数に使うため、ここでその式を入手する
    """    
    sum_z_e = 0
    for t in range(HORIZON-1):
        sum_z_e += z_e[t]
    
    """
    目的関数をセットする
    """
    m.setObjective(c*(sum_z_e) - (1-c)*part_of_obj_function, 
                   gp.GRB.MINIMIZE)
    #解く
    print("-"*40 + "\n" + "-"*15 + " c = {} ".format(c) + "-"*15 + "\n" + "-"*40 )
    start = time.time()
    m.update()
    m.optimize()
    finish = time.time() - start
    f_record.write("time to optimize with {0}, {1}\n".format(c, finish))
           
    f_record.close() 
    
    print("-"*40)
        
    
    if m.Status != gp.GRB.OPTIMAL: 
        return 0, -LARGE_NUMBER
        
    # 最適解が得られた場合、結果を出力
    else:
        
        m.update() 
        output_result(TDES, z_e, w, len(hard_constraint), encoder_hard)
        
        """
        pTDESのパラメータになる値m,wを取得する
        """
        if TDES.time_ratio == -1:
            return
        else: #TDESがcTDESであるときに以下の処理を行う
            
            z_e_sum = 0
            for t in range(HORIZON-1):
                z_e_sum += z_e[t].x
           
            mm = np.ceil((z_e_sum[0]+1)*TDES.time_ratio)
            if c != 1: 
                ww = (c*(z_e_sum[0]) - m.ObjVal)/(1-c)
            else:
                ww = 1               
             
            
            """
            念のため、リセットして、ILP制約を消した状態で次のTDESに進む
            """
            m.reset(0)         
            return mm, ww

        
        
if    __name__ == '__main__':
    
    today = datetime.date.today()
    todaydetail = datetime.datetime.today()
    dir_path = 'data/'+str(today)+'/'+str(todaydetail.hour)+'-'+str(todaydetail.minute)+'-'+str(todaydetail.second)+'/'
    print(todaydetail)
    os.makedirs(dir_path, exist_ok=True)
    
    """
    プログラム全体でかかる時間を計測する
    """
    start_all = time.time() 
    
    """
    cTDESについて、入力情報を読み取る
    """
    p_f_list = []
    problem_formulation = ProblemFormulation(translate_des_to_tdes.get_TDES(cDES_1.get_DES()), 
                                             constr_for_cTDES_1.get_hard_constraint(), constr_for_cTDES_1.get_soft_constraint(), 
                                             constr_for_cTDES_1.HORIZON)
    p_f_list.append(problem_formulation)
    
    
    problem_formulation = ProblemFormulation(translate_des_to_tdes.get_TDES(cDES_2.get_DES()), 
                                             constr_for_cTDES_2.get_hard_constraint(), constr_for_cTDES_2.get_soft_constraint(), 
                                             constr_for_cTDES_2.HORIZON)
    p_f_list.append(problem_formulation)
    
    
    """
    αの集合
    """
    
    #A=[0.01, 0.5, 1]
    A=[0.5]
    
    
    """
    下位TDESのプランニング
    """
    M = []
    W = []
    for p_f in p_f_list:
        print("\n" + "*"*40 + "\n" + "*"*15 + "  " + p_f.TDES.name + "  " + "*"*15 + "\n" + "*"*40 + "\n")
        #print(p_f.HORIZON)
        list_m = []
        list_w = []
        for c in A:
            (m, w) = get_execution(p_f.TDES, p_f.hard_constraint, p_f.soft_constraint_list, p_f.HORIZON, c, dir_path)
             
            list_m.append(m)
            list_w.append(w)    
        M.append(list_m) 
        W.append(list_w)
        p_f.TDES.output(dir_path)
    
    """
    MとWをテキストファイルに出力
    """
    f=open(dir_path + 'M.txt', 'w')
    f.write("{}".format(M))
    f=open(dir_path + 'W.txt', 'w')
    f.write("{}".format(W))
    f.close()

    """
    上位TDESのプランニング
    """
    pTDES = translate_des_to_tdes.get_TDES(pDES.get_DES())
    print("\n" + "*"*40 + "\n" + "*"*15 + "  " + pTDES.name + "  " + "*"*15 + "\n" + "*"*40 + "\n")
    (p_hard_constraint, p_soft_constraint_list) = constraint_for_pTDES.get_constraint(M, W)
    HORIZON = constraint_for_pTDES.HORIZON
    
    
    get_execution(pTDES, p_hard_constraint, p_soft_constraint_list, HORIZON, 0, dir_path)
    
    
    """
    プログラムの最初から最後までにかかった時間を出力する
    """
    finish = time.time() - start_all
    f_record_all=open(dir_path + 'all_time_record.txt', 'w')
    f_record_all.write("time to execute this program, {}\n".format(finish))
    f_record_all.close()
        
    
    