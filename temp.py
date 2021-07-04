# -*- coding: utf-8 -*-

import gurobipy as gp#


import time
import datetime
import os
import copy
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
        self.soft_constraint = soft
        self.HORIZON = HORIZON
        

"""
実行列のi番目の状態を表すw[i,]と、j番目の事象がtickなら1を持つz_e[j]を導入
"""
def get_variable_for_execution(m, HORIZON, size_of_state,
                                 adjacency_matrix, tick_matrix):

    z_e = m.addMVar(HORIZON,vtype=gp.GRB.BINARY, name = "z_e")
    w = m.addMVar(HORIZON, (size_of_state),vtype=gp.GRB.BINARY, name = "w")
    
    
    """
    二値変数z_eについて制約を加える
    """
       
    for i in range(HORIZON-1):
        sum2 = 0
        sum1 = 0
        for j in range(size_of_state):
            
            for k in range(size_of_state):
                sum1 += w[i,k]*tick_matrix[k,j]
                sum2 += w[i+1,k]*tick_matrix[j,k]
            #Sum2 += Sum1*W[i+1][j]

        
        m.addConstr(z_e[i] <= sum1)
        m.addConstr(z_e[i] <= sum2)
        m.addConstr(z_e[i] >= -1 + sum1 + sum2)
        #s.add(E[i] <= Sum2, Sum2 < E[i] + 1 )
        
    """
    二値変数wについて制約を加える
    """
    m.addConstrs(w[h,] == 1 for h in range(HORIZON))
    
    Sum = 0
    for i in range(HORIZON-1):
        for j in range(size_of_state):
            Sum = 0
            for k in range(size_of_state):

                Sum += w[i,k]*adjacency_matrix[k,j]
            
            m.addConstr(w[i+1,j] <= Sum)
            
    return z_e, w
      
        
"""
実際の実行列を求める
戻り値＝（事象tickの数：m、Soft制約の重要度の合計：w）
"""
def main(TDES, hard_constraint, soft_constraint_list, HORIZON, A, dir_path):
    
    f_record=open(dir_path + TDES.name + 'time_record.txt', 'w')
    
    
    """
    α（0以上1以下）を要素にもつAを値が大きい順にソートする.
    ただし、Aには1が必ず含まれるとする
    """
    A.sort(reverse=True)
    if A[0] != 1:
        print("ERROR. There is not the value of 1 in A \n")
    
    m = gp.Model("Planning for TDES:{}".format(TDES.name))

    print("get matrix of label")
    label_matrix = TDES.get_label_matrix()

    print("get matrix of transition")
    (adjacency_matrix, tick_matrix) = TDES.get_transition_matrix()

    (z_e, w) = get_variable_for_execution(m, HORIZON, len(TDES.s),adjacency_matrix, tick_matrix)
    
    encoder_hard = encoder_main.EncoderBool(hard_constraint)
    encoder_hard.set_constraint_for_variable(m, HORIZON)
    
    start = time.time()
    encoder_hard.start_encodeing(m, HORIZON, TDES, label_matrix, z_e, w)
    finish = time.time() - start
    f_record.write("time to encode hard constraint, {}\n".format(finish))
    
    
    part_of_obj_function = 0
    for (soft_constraint, weight) in soft_constraint_list:
        encoder = encoder_main.EncoderBool(hard_constraint)
        
        start = time.time()
        encoder.start_encodeing(m, HORIZON, TDES, label_matrix, z_e, w)
        finish = time.time() - start
        f_record.write("time to encode soft constraint, {}\n".format(finish))
            
        
                    
        if type(soft_constraint[-1]) == list:
            part_of_obj_function = part_of_obj_function + encoder.z[-2,0]*weight
        else:
            part_of_obj_function = part_of_obj_function + encoder.z[-1,0]*weight
        
    m.update() 
    
    
    list_m = []
    list_w = []
    for alpha in A:
        """
        目的関数のみを変更させるので、コピーを行う
        """
        copy_model = m.copy()
        copy_model.setObjective(alpha*(z_e.sum()) - (1-alpha)*part_of_obj_function, 
                       gp.GRB.MINIMIZE)
        
        
        #解く
        print("-"*40)
        start = time.time()
        copy_model.optimize()
        finish = time.time() - start
        f_record.write("time to optimize with {0}, {1}\n".format(alpha, finish))
            
        
        print("-"*40)
            
        # 最適解が得られた場合、結果を出力
        if copy_model.Status == gp.GRB.OPTIMAL:        
            copy_model.update() 
            
            """
            pTDESのパラメータになる値m,wを取得する
            """
            if TDES.time_ratio != -1: #TDESがcTDESであるときに以下の処理を行う
                list_m.append(np.ceil((z_e.X.sum()+1)*TDES.time_ratio))
                if alpha != 1:
                    list_w.append((alpha*(z_e.sum()) - copy.ObjVal)/(1-alpha))
                else:
                    list_w.append(1)
            
            
            
            """
            実行列をテキストファイルで出力
            """
            f=open(dir_path + TDES.name + "alpha:{}".format(alpha) + 'execution_state.txt', 'w')
            for h in range(HORIZON):
                for index_state in range(len(TDES.s)):
                    if w.X[h, index_state] == 1:
                        break
                
                if index_state > len(TDES.s):
                    print("ERROR.")
                else:    
                    f.write("h:{0}, state(DES):{1}, state(TDES):{2}\n".format(
                            h, TDES.s.index(index_state)[0], TDES.s.index(index_state))
                            )
            f.close()
        
            """
            二値変数zの値を出力
            """
            with open(dir_path + TDES.name + 'alpha:{}'.format(alpha) + 'z.csv', 'w') as f:
                writer = csv.writer(f)
                for index_fml in range(hard_constraint):
                    writer.writerow(encoder_hard.z[index_fml].X)
      
    f_record.close() 
    
    """
    念のため、リセットして、ILP制約を消した状態で次のTDESに進む
    """
    m.reset(0)         
    return list_m, list_w


if    __name__ == '__main__':
    
    today = datetime.date.today()
    todaydetail = datetime.datetime.today()
    dir_path = 'data/pic/'+str(today)+'/'+str(todaydetail.hour)+'-'+str(todaydetail.minute)+'-'+str(todaydetail.second)+'/'
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
    problem_formulation = ProblemFormulation(translate_des_to_tdes.get_TDES(cDES_1.get_cDES()), 
                                             constr_for_cTDES_1.get_hard_constraint(), constr_for_cTDES_1.get_hard_constraint(), 
                                             constr_for_cTDES_1.HORIZON)
    p_f_list.appned(problem_formulation)
    
    
    problem_formulation = ProblemFormulation(translate_des_to_tdes.get_TDES(cDES_2.get_cDES()), 
                                             constr_for_cTDES_2.get_hard_constraint(), constr_for_cTDES_2.get_hard_constraint(), 
                                             constr_for_cTDES_2.get_horizon())
    p_f_list.appned(problem_formulation)
    
    
    """
    αの集合
    """
    
    A=[0.01, 0.5, 1]
    
    
    """
    下位TDESのプランニング
    """
    M = []
    W = []
    for p_f in p_f_list:
        (list_m, list_w) = main(p_f.TDES, p_f.hard_constraint, p_f.soft_constraint_list, p_f.HORIZON, A, dir_path)
        M.appned(list_m)
        W.appned(list_w)    
           
 
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
    (p_hard_constraint, p_soft_constraint_list) = constraint_for_pTDES.get_constraint(M, W)
    HORIZON = constraint_for_pTDES.HORIZON
    pTDES = translate_des_to_tdes.get_TDES(pDES.get_DES())
    
    main(pTDES, p_hard_constraint, p_soft_constraint_list, HORIZON, [0], dir_path)
    
    
    """
    プログラムの最初から最後までにかかった時間を出力する
    """
    finish = time.time() - start_all
    f_record_all=open(dir_path + 'all_time_record.txt', 'w')
    f_record_all.write("time to execute this program, {}\n".format(finish))
    f_record_all.close()
        
    
    