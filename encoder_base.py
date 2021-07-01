# -*- coding: utf-8 -*-
"""
Created on Thu Jul  1 10:26:35 2021

@author: takuma
"""

import gurobipy as gp
import numpy as np
import matplotlib.pyplot as plt

#Boolean semantics と、Robust semantics についてエンコードするクラスの継承元となるクラス
class EncoderBasis(object):
    
    def __init__(self, formula, ell, EPSILON, M, mode):
        #ellは数字であることが前提で、L.index(ell)=ellとなるようにする
        if type(ell) == int:
            self.ell = ell          
        else:
            print("error")
            
        self.formula = formula
        self.EPSILON = EPSILON
        
        #MはBoolに対してはM_d、Robustに対してはM_r
        self.M = M   
        
        self.zr = 0 
        if (mode == "r") or (mode == "b"):
            self.mode = mode
        else:
            print("*"*20 + "\n eroor. mode is not correct\n" + "*"*20)
    
    def start_encodeing(self, m, HORIZON, system):
        
        
        len_fml = len(self.formula)
        self.zr = m.addMVar((len_fml, HORIZON),vtype=gp.GRB.BINARY, name = "z")
            
        
        if type(self.formula[-1])==list:
            m.addConstr(self.zr[-2,0,self.ell] == 1) #L.index(self.ell)=self.ell
        else:
            m.addConstr(self.zr[-1,0,self.ell] == 1)
        
        #at_location = "_at:{}".format(self.ell)
        len_L = len(system.L)
        len_fml = len(self.formula)
        
        #処理した式の要素をためる（伝わりにくい）
        stack = []
        
            
        for i in range(len_fml):	#i represent subfomula
            
            
               
            if self.formula[i] == '!':
                if stack == False :
                    print ("SYNTAX ERROR: '!' at {}th element in self.formula.".format(i))
    
                m = self.negation2milp(m, HORIZON,self.zr[i],self.zr[stack[-1]], len_L)
                stack = self.stack_manage(stack, del_list=[stack[-1]], set_list=[i])
                
    
            elif self.formula[i] == '&':
            
                #  &は二項演算子だから、&の対象が二つ必要
                if len(stack) <= 1:
                    ("SYNTAX ERROR: '&' at {}th element in self.formula.".format(i))
                else:
                    
                    m = self.and2smt(m, HORIZON,
                                     self.zr[i], [self.zr[stack[-1]],self.zr[stack[-2]]],
                                     len_L)
                    """
                    m = self.and2smt_ver2(m, HORIZON,
                                          self.zr[i], [self.zr[stack[-1]],self.zr[stack[-2]]],
                                          len_L)
                    """
                    stack = self.stack_manage(stack, del_list=[stack[-1],stack[-2]], set_list=[i])
                    
    
            elif self.formula[i] == '|':
                if len(stack) <= 1:
                    print("SYNTAX ERROR: '|' at {}th element in self.formula.".format(i))
                else:
                    
                    m = self.or2smt(m, HORIZON,
                                    self.zr[i], [self.zr[stack[-1]],self.zr[stack[-2]]], 
                                    len_L)
                    """
                    m = self.or2smt_ver2(m, HORIZON,
                                         self.zr[i], [self.zr[stack[-1]],self.zr[stack[-2]]],
                                         len_L)
                    """
                    stack = self.stack_manage(stack, del_list=[stack[-1],stack[-2]], set_list=[i])
                
            elif self.formula[i] == 'U':
                if len(stack) <= 1:
                    print("SYNTAX ERROR: 'U' at {}th element in self.formula.".format(i))
                if type(self.formula[i+1]) != list:
                    print("SYNTAX ERROR at {}th element in self.formula.".format(i))
                    print("There is no interval after temporal operator")
                    
                m = self.until2smt(m, HORIZON,
                                   self.zr[i], self.zr[stack[-2]],self.zr[stack[-1]],
                                   self.formula[i+1], i,
                                   len_L)
                stack = self.stack_manage(stack, del_list=[stack[-1],stack[-2]], set_list=[i])
                
                #  時相論理演算子・空間演算子は、後ろに時間・空間を表す区間を式に入れる
                #  つまり、演算子と区間で1セット
                #  だから、ここでiを一つ増やしておく
                i+=1
                if i >= len_fml:
                    break
    
            elif self.formula[i] == 'G':
                if len(stack) < 1:
                    print("SYNTAX ERROR: 'G' at {}th element in self.formula.".format(i))
                if type(self.formula[i+1]) != list:
                    print("SYNTAX ERROR at {}th element in self.formula.".format(i))
                    print("There is no interval after temporal operator")
                m = self.global2smt(m, HORIZON,
                                    self.zr[i], self.zr[stack[-1]],self.formula[i+1],
                                    len_L)
                stack = self.stack_manage(stack, del_list=[stack[-1]], set_list=[i])
                
                i+=1
                if i >= len_fml:
                    break
    
            elif self.formula[i] == 'F':
                if len(stack) < 1:
                    print("SYNTAX ERROR: 'F' at {}th element in self.formula.".format(i))
                
                if type(self.formula[i+1]) != list:
                    print("SYNTAX ERROR at {}th element in self.formula.".format(i))
                    print("There is no interval after temporal operator")
                    
                m = self.eventually2smt(m, HORIZON,
                                        self.zr[i], self.zr[stack[-1]],self.formula[i+1],
                                        len_L)
                self.stack_manage(stack, del_list=[stack[-1]], set_list=[i])
                
                i+=1
                if i >= len_fml:
                    break
                
                
            #atomic propositionの時
            else:
                m = self.ap2smt(m, HORIZON,
                                        self.zr[i], self.zr[stack[-1]],self.formula[i+1],
                                        len_L)
                
                
                stack = self.stack_manage(stack, del_list=[], set_list=[i])
    
        if len(stack) != 1 :
            print("SYNTAX ERROR: len(stack)={0},stack={1}".format(len(stack),stack))
    
        #ここの戻り値いらない
        return 	m, self.zr
    
    #stack_manage よりもupdate_stack の方がいいかも
    def stack_manage(self, stack, del_list, set_list):
        
        #stack[-2],stack[-1]の順番のリストが送られてくる前提
        for del_obj in del_list:
            if stack[-1] == del_obj:
                del stack[-1]
            else:
                print("This {}th element has not been encoded yet.".format(del_obj))
          
        for set_obj in set_list:
            if set_obj in stack == True:
                print("This {}th element has been encoded.".format(set_obj))
        
            else:
                stack.append(set_obj)
                
        return stack
 
    
    #  グラフ上のtarget_ellの4近傍の場所をリストとして求める。
    #  ただし、prev_ellは除いて返す
    def get_neighbor_list(self, target_ell, prev_ell, graph_size_h, graph_size_v):
        
        #左上
        if target_ell == 0:
            neighbor =[target_ell+1, target_ell+graph_size_h]
        
        #右上    
        elif target_ell == graph_size_h-1:
            neighbor =[target_ell-1, target_ell+graph_size_h]
            
        #左下
        elif target_ell == graph_size_h*(graph_size_h-1):
            neighbor =[target_ell+1, target_ell - graph_size_h]
            
        #右下    
        elif target_ell == graph_size_h*(graph_size_v-1) + (graph_size_h-1):
            neighbor =[target_ell- 1, target_ell - graph_size_h]
           
            
         #target_ell が左端
        elif (target_ell)%(graph_size_h) == 0:
            neighbor =[target_ell+1, target_ell+graph_size_h, target_ell - graph_size_h]
            
        #target_ell が右端
        elif (target_ell+1)%(graph_size_h) == 0:
            neighbor =[target_ell-1, target_ell+graph_size_h, target_ell - graph_size_h]
            
        #target_ell が上端
        elif target_ell <= graph_size_h-1:
            neighbor =[target_ell+1, target_ell-1, target_ell + graph_size_h]
            
        #target_ell が下端
        elif target_ell >= graph_size_h*(graph_size_v-1):
            neighbor =[target_ell+1, target_ell-1, target_ell - graph_size_h]
            
        else:
            neighbor =[target_ell+1, target_ell-1, target_ell - graph_size_h, target_ell + graph_size_h]
            
        if prev_ell == -1:
            #print(prev_ell,neighbor)
            return neighbor
        
        else:      
            #print(prev_ell,neighbor)
            if prev_ell in neighbor:
                neighbor.remove(prev_ell)
            #print(neighbor)
            return neighbor
          
      
    def output(self, new_dir_path_recursive, GRAPH_SIZE_H, GRAPH_SIZE_V, HORIZON):
         
        #  最適解が得られたら、メンバ変数zrの値を出力する
        #  数字・画像の両方で出力
        len_fml = len(self.formula)
        
        file_name_z= 'ell-{}_output_z.txt'.format(self.ell)
        fz=open(new_dir_path_recursive+file_name_z, 'w')
        
        fz.write("\n"+"-"*20+"z"+"-"*20)
        for i in range(len_fml):
         
            fz.write("\nposition  formula: {0}, {1}".format(i, self.formula[i]))
            for t in range(HORIZON):
                fz.write("\nt: {}".format(t))
                fz.write("\n{}".format(self.zr.X[i,t,].reshape(GRAPH_SIZE_H,GRAPH_SIZE_V) ))
        fz.close()
        
        
   
        #os.makedirs(new_dir_path_recursive, exist_ok=True)
        
        for position_in_FORMULA in range(len_fml):
            for t in range(HORIZON):
                fig1 = plt.figure()
                    
                
                x1 = np.linspace(0, GRAPH_SIZE_H, num=GRAPH_SIZE_H)
                y = np.linspace(GRAPH_SIZE_V, 0, num=GRAPH_SIZE_V)
                X, Y = np.meshgrid(x1, y)
                r_4_4= self.zr.X[position_in_FORMULA,t,:].reshape(GRAPH_SIZE_H, GRAPH_SIZE_V)
                Z = r_4_4
                
                plt.axes([0.025, 0.025, 0.95, 0.95])
                plt.imshow(Z, interpolation='nearest', cmap='bone', origin='upper', vmin=0.0,vmax=1.0)
                plt.colorbar(shrink=.92)
                
                plt.xticks(())
                plt.yticks(())
                #plt.show()
                plt.close(fig1)
              
                fig1.savefig(new_dir_path_recursive +'ell-{0}_z_pos-{1}_t-{2}.png'.format(self.ell, position_in_FORMULA, t))