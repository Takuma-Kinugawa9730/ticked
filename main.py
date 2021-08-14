# -*- coding: utf-8 -*-

import gurobipy as gp#
# test sim

import time
import datetime
import os
import encoder_main
import numpy as np
import csv
from collections import defaultdict
import problem_formulation
flag_comparison = False
"""
比較検討のためのproblem_formulation、平らなDES
"""
#import problem_formulation_for_compare_plane as problem_formulation
#flag_comparison = True


num_ratio = 3

        

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
      
def output_result(HORIZON, TDES, z_e, w, len_hard_constraint, encoder_hard, ratio, list_encoders_for_soft, ObjVal, tilde_z, z_p, z_dummy):

    """
    満たしたSoft制約を出力と、実行列をテキストファイルで出力
    """
    if len(ratio) ==1:
        f=open(dir_path + TDES.name + "_ratio-{}_".format(ratio[0]) + 'satisfied_soft_constr_and_execution_state.txt', 'w')
    elif len(ratio) ==2:
        f=open(dir_path + TDES.name + "_ratio1-{0}_ratio2-{1}_".format(ratio[0],ratio[1]) + 'satisfied_soft_constr_and_execution_state.txt', 'w')
    else:
        print("error")
        
    f.write("Optimal value:{}\n".format(ObjVal))
        
    if type(encoder_hard.formula[-1])==list:
        if encoder_hard.z.X[-2,0] == 1:
            f.write("Hard\nsat: {}\n\nSoft\n".format(encoder_hard.formula))
        else:
            f.write("Hard\nunsat: {}\n\nSoft\n".format(encoder_hard.formula))
            
    for encoder in list_encoders_for_soft:
        
        if type(encoder.formula[-1])==list:
            if encoder.z.X[-2,0] == 1:
                f.write("sat: {}\n".format(encoder.formula))
            else:
                f.write("unsat: {}\n".format(encoder.formula))
        else:
            if encoder.z.X[-1,0] == 1:
                f.write("sat: {}\n".format(encoder.formula))
            else:
                f.write("unsat: {}\n".format(encoder.formula))
                
    f.write("\n")
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
    os.makedirs(dir_path + 'output_binary_variable/', exist_ok=True)
    if len(ratio) ==1:
        with open(dir_path + 'output_binary_variable/' +  TDES.name +  "_ratio-{}_".format(ratio[0]) + 'z.csv', 'w') as f:
            writer = csv.writer(f)
            for index_fml in range(len_hard_constraint):
                writer.writerow(encoder_hard.z[index_fml].X)
      
    elif len(ratio) ==2:
        with open(dir_path + 'output_binary_variable/' +  TDES.name + "_ratio1-{0}_ratio2-{1}_".format(ratio[0],ratio[1]) + 'z.csv', 'w') as f:
            writer = csv.writer(f)
            for index_fml in range(len_hard_constraint):
                writer.writerow(encoder_hard.z[index_fml].X)
      
    else:
        print("error")
    
  
    """
    二値変数z_eの値を出力
    """
    if len(ratio) ==1:
        f=open(dir_path + '/output_binary_variable/' + TDES.name +  "_ratio-{}_".format(ratio[0]) +  'z_e.txt', 'w')
    elif len(ratio) ==2:
        f=open(dir_path + '/output_binary_variable/' + TDES.name +  "_ratio1-{0}_ratio2-{1}_".format(ratio[0],ratio[1])  + 'z_e.txt', 'w')
    else:
        print("error")
    
    for t in range(len(z_e.X)):
        f.write("{}\n".format(z_e.X[t]))
    f.close()
    
     
  
    """
    二値変数tilde_z とz_pの値を出力
    """
    if len(ratio) ==1:
        f=open(dir_path + '/output_binary_variable/' + TDES.name +  "_ratio-{}_".format(ratio[0]) +  'z_for_obj.txt', 'w')
    elif len(ratio) ==2:
        f=open(dir_path + '/output_binary_variable/' + TDES.name +  "_ratio1-{0}_ratio2-{1}_".format(ratio[0],ratio[1])  + 'z_for_obj.txt', 'w')
    else:
        print("error")
    for ap_R in range(len(TDES.AP_R)):
        f.write("{}-th ap_R \n".format(ap_R))
        #print("{}-th ap_R \n".format(ap_R))
        for index_ratio in range(num_ratio):
            f.write("{}-th index of ratio \ntilde_z, z_p, z_dummy\n".format(index_ratio))
            #print("{}-th index of ratio \ntilde_z, z_p".format(index_ratio))
            for k in range(HORIZON):
                f.write("  {0},   {1},   {2}\n".format(tilde_z.X[ap_R, index_ratio, k], z_p.X[ap_R, index_ratio, k], z_dummy.X[ap_R, k]))
                #print("  {0},  {1} \n".format(tilde_z.X[ap_R, index_ratio, k], z_p.X[ap_R, index_ratio, k]))
                
    f.close()
        
"""
パラメータ（ratio）の数はすべて3つにする
"""    

    
"""
実際の実行列を求める
戻り値＝（事象tickの数：m、Soft制約の重要度の合計：w）
"""

def get_execution(TDES, hard_constraint, soft_constraint_list, HORIZON, list_ratio, dir_path, M, W):
    
    LARGE_NUMBER = 100
    
    f_record=open(dir_path + TDES.name + '_time_record.txt', 'w')
    
    
    #m = gp.Model("Planning for TDES:{0} c:{1}".format(TDES.name, c))
    m = gp.Model("Planning for TDES:{0}".format(TDES.name))
    
    m.Params.LogFile = dir_path +"Log.txt"

    """
    ラベル関数の行列、遷移関数の行列、事象tickに関するベクトルを手に入れる
    """    
    print("encode TDES: {}".format(TDES.name))
    start = time.time()
    
    label_matrix = TDES.get_label_matrix()
    (adjacency_matrix, alpha, beta) = TDES.get_transition_matrix()
    
    finish = time.time() - start
    f_record.write("time to encode TDES, {}\n".format(finish))
    
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
    #tilde_z = m.addMVar((len(AP_R), 3, HORIZON),vtype=gp.GRB.BINARY, name = "tilde_z")
    tilde_z = 0
    z_p = 0
    z_dummy = 0
    tilde_z, z_p, z_dummy = encoder_hard.start_encodeing(m, HORIZON, TDES, label_matrix, z_e, w, TDES.ap, TDES.AP_R, M)
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
    list_encoders_for_soft = []
    for (soft_constraint, weight) in soft_constraint_list:
        print(soft_constraint, weight)
        encoder = encoder_main.EncoderBool(soft_constraint)
        
        start = time.time()
        encoder.start_encodeing(m, HORIZON, TDES, label_matrix, z_e, w, TDES.ap, TDES.AP_R, M)
        finish = time.time() - start
        f_record.write("time to encode soft constraint, {}\n".format(finish))
            
        list_encoders_for_soft.append(encoder)
            
        """
        Soft制約の重みの合計を目的関数に使うため、ここでその式を入手する
        """    
        if type(soft_constraint[-1]) == list:
            part_of_obj_function = part_of_obj_function + encoder.z[-2,0].tolist()[0]*weight
        else:
            part_of_obj_function = part_of_obj_function + encoder.z[-1,0].tolist()[0]*weight
     
    sum_of_w = m.addVar(vtype=gp.GRB.INTEGER)
    m.addConstr(sum_of_w == part_of_obj_function)
    m.update() 
    
    
    """
    事象tickの合計数を目的関数に使うため、ここでその式を入手する
    """    
    sum_z_e = 0
    for t in range(HORIZON-1):
        sum_z_e += z_e[t].tolist()[0]
        
        
    list_m = []
    list_w = []
    for ratio in list_ratio:
        """
        目的関数をセットする
        """
        level = TDES.have_refined_state
        if level == -1:
            
            #ratio[0]が\gamma を表す
            
            m.setObjective(-ratio[0]*(sum_z_e) + (1-ratio[0])*sum_of_w, 
                           gp.GRB.MAXIMIZE)
            
        elif level == 0:
            sum_for_obj = 0
            for ap_R in range(len(TDES.AP_R)):
                for index_ratio in range(num_ratio):
                    for k in range(HORIZON):
                        sum_for_obj += tilde_z[ap_R, index_ratio, k].tolist()[0]*W[ap_R][index_ratio]
                        
            m.setObjective(-ratio[0]*(sum_z_e) +ratio[1]*(sum_for_obj) + (1-ratio[0]-ratio[1])*sum_of_w, 
                           gp.GRB.MAXIMIZE)    
            
        elif level == 1:
            
            sum_for_obj = 0
            for ap_R in range(len(TDES.AP_R)):
                for index_ratio in range(num_ratio):
                    for k in range(HORIZON):
                        sum_for_obj += tilde_z[ap_R, index_ratio, k].tolist()[0]*W[ap_R][index_ratio]
                        
            m.setObjective(ratio[0]*(sum_for_obj) + (1-ratio[0])*sum_of_w, 
                           gp.GRB.MAXIMIZE)          
        else:
            print("error. ")        

        #解く
        print("-"*40 + "\n" + "-"*15 + " c = {0} (TDES:{1}) ".format(ratio, TDES.name) + "-"*15 + "\n" + "-"*40 )
        start = time.time()
        m.update()
        m.optimize()
        finish = time.time() - start
        f_record.write("time to optimize with {0}: {1}\n".format(ratio, finish))
             
        print("-"*40)
            
        
        if m.Status != gp.GRB.OPTIMAL: 
            #return 0, -LARGE_NUMBER
            list_m.append(0)
            list_w.append(-LARGE_NUMBER)
        # 最適解が得られた場合、結果を出力
        else:
            
            m.update() 
            output_result(HORIZON, TDES, z_e, w, len(hard_constraint), encoder_hard, ratio, list_encoders_for_soft, m.ObjVal, tilde_z, z_p, z_dummy)
            
            """
            pTDESのパラメータになる値m,wを取得する
            """
            if TDES.time_ratio == -1:
                pass
            else: #TDESがcTDESであるときに以下の処理を行う
                
                z_e_sum = 0
                for t in range(HORIZON-1):
                    z_e_sum += z_e[t].x
               
                list_m.append(np.ceil((z_e_sum[0]+1)*TDES.time_ratio))
                
                list_w.append(sum_of_w.x)
                #list_w.append(m.ObjVal)
                
  
    f_record.close() 
    if TDES.time_ratio == -1:
        return [0], [0]
    
    else: #TDESがcTDESであるときに以下の処理を行う
                   
        return list_m, list_w     
        
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
    
    print("get problem_formulation")
    p_f_list = problem_formulation.set_problem_formulation()
    
    """
    ratioの集合
    """
    #C=[[1], [0.5], [0.01]]
    #C=[0.5]
    if flag_comparison:
        Kappa = [[1],[0]]
    else:
        Kappa = [[1], [0.5], [0.01]]
    #    Lambda = [[0.5,0.5], [0.33, 0.33], [0.2,0.3]]
        Lambda = [[1,0], [0.33, 0.33], [0.1,0.1]]
        Mu = [[0.1], [0.25], [0.5]]
        
    M = defaultdict(list)
    W = defaultdict(list)
    for p_f_list_for_level in p_f_list:
        
        for p_f in p_f_list_for_level:
            if p_f.TDES.have_refined_state == -1:
                print("get execution")
                (list_m, list_w) = get_execution(p_f.TDES, p_f.hard_constraint, p_f.soft_constraint_list, 
                                                 p_f.HORIZON, Kappa, dir_path, [[0]], [[0]])
            elif p_f.TDES.have_refined_state == 1:
                target_M = []
                target_W = []
                for ap_R in p_f.TDES.AP_R:
                    target_M.append(M[ap_R])
                    target_W.append(W[ap_R])
                    
                if len(target_M) == 0:
                    target_M = [[0]]
                    
                if len(target_W) == 0:
                    target_W = [[0]]
                (list_m, list_w) = get_execution(p_f.TDES, p_f.hard_constraint, p_f.soft_constraint_list, 
                                                 p_f.HORIZON, Mu, dir_path, target_M, target_W)
            else:
                target_M = []
                target_W = []
                for ap_R in p_f.TDES.AP_R:
                    target_M.append(M[ap_R])
                    target_W.append(W[ap_R])
                (list_m, list_w) = get_execution(p_f.TDES, p_f.hard_constraint, p_f.soft_constraint_list, 
                                                 p_f.HORIZON, Lambda, dir_path, target_M, target_W)
                
            M[p_f.TDES.name]=list_m 
            W[p_f.TDES.name]=list_w
            
    
    """
    MとWをテキストファイルに出力
    """
    f=open(dir_path + 'M.txt', 'w')
    f.write("{}".format(M))
    f=open(dir_path + 'W.txt', 'w')
    f.write("{}".format(W))
    f.close()
    
    
    """
    プログラムの最初から最後までにかかった時間を出力する
    """
    finish = time.time() - start_all
    print(finish)
    
    """
    関係するデータを出力
    """
    f_record_all=open(dir_path + 'data.txt', 'w')
    f_record_all.write("time to execute this program, {}\n".format(finish))
    
    f_record_all.write("\n" + "*"*40 + "\n" + "*"*10 + "  " + 
                       "ratio used in objective function" + "  " + "*"*10 + "\n" + "*"*40 + "\n")
        
    f_record_all.write("kappa:{0},\n lambda:{1},\n mu:{2}\n".format(Kappa,Lambda,Mu))
    
    
    for p_f_list_for_level in p_f_list:
        for p_f in p_f_list_for_level:
            
            p_f.TDES.output(dir_path)
            
        
            f_record_all.write("\n" + "*"*40 + "\n" + "*"*15 + "  " + p_f.TDES.name + "  " + "*"*15 + "\n" + "*"*40 + "\n")
        
            f_record_all.write("Hard constraint: {}\n".format(p_f.hard_constraint))
        
            for (soft_constraint, weight) in p_f.soft_constraint_list:
                f_record_all.write("soft_constraint: {0}, weight: {1}\n".format(soft_constraint, weight))
        
            f_record_all.write("HORIZON: {}".format(p_f.HORIZON))
            
    f_record_all.close()
        