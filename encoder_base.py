# -*- coding: utf-8 -*-
"""
Created on Thu Jul  1 10:26:35 2021

@author: takuma
"""

import gurobipy as gp
import numpy as np
import matplotlib.pyplot as plt

class EncoderBasis(object):
    
    def __init__(self, formula):
        
        self.formula = formula
        self.z
        
    """
    formulaがHard制約を表すならば、二値変数zについて制約を加える
    """
    def set_constraint_for_variable(self, m, HORIZON):
        
        
        self.z = m.addMVar((len(self.formula), HORIZON),vtype=gp.GRB.BINARY, name = "z")
        if type(self.formula[-1])==list:
            m.addConstr(self.z[-2,0] == 1) #L.index(self.ell)=self.ell
        else:
            m.addConstr(self.z[-1,0] == 1)
        
        
    def start_encodeing(self, m, HORIZON, TDES, label_matrix, z_e, w):
        
        
        len_fml = len(self.formula)
        
        
        #処理した式の要素をためる（伝わりにくい）
        stack = []
        
            
        for i in range(len_fml):    #i represent subfomula
            
            
               
            if self.formula[i] == '!':
                if stack == False :
                    print ("SYNTAX ERROR: '!' at {}th element in self.formula.".format(i))
    
                m = self.negation2milp(m, HORIZON,self.z[i],self.z[stack[-1]])
                stack = self.stack_manage(stack, del_list=[stack[-1]], set_list=[i])
                
    
            elif self.formula[i] == '&':
            
                #  &は二項演算子だから、&の対象が二つ必要
                if len(stack) <= 1:
                    ("SYNTAX ERROR: '&' at {}th element in self.formula.".format(i))
                else:
                    
                    m = self.and2smt(m, HORIZON,
                                     self.z[i], [self.z[stack[-1]],self.z[stack[-2]]]
                                     )
                    
                    stack = self.stack_manage(stack, del_list=[stack[-1],stack[-2]], set_list=[i])
                    
    
            elif self.formula[i] == '|':
                if len(stack) <= 1:
                    print("SYNTAX ERROR: '|' at {}th element in self.formula.".format(i))
                else:
                    
                    m = self.or2smt(m, HORIZON,
                                    self.z[i], [self.z[stack[-1]],self.z[stack[-2]]]
                                    )
                    
                    stack = self.stack_manage(stack, del_list=[stack[-1],stack[-2]], set_list=[i])
                
            elif self.formula[i] == 'U':
                if len(stack) <= 1:
                    print("SYNTAX ERROR: 'U' at {}th element in self.formula.".format(i))
                if type(self.formula[i+1]) != list:
                    print("SYNTAX ERROR at {}th element in self.formula.".format(i))
                    print("There is no interval after temporal operator")
                    
                m = self.until2smt(m, HORIZON,
                                   self.z[i], self.z[stack[-2]],self.z[stack[-1]],
                                   self.formula[i+1], i, z_e
                                   )
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
                                    self.z[i], self.z[stack[-1]],self.formula[i+1]
                                    )
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
                                        self.z[i], self.z[stack[-1]],self.formula[i+1]
                                        )
                self.stack_manage(stack, del_list=[stack[-1]], set_list=[i])
                
                i+=1
                if i >= len_fml:
                    break
                
                
            #atomic propositionの時
            else:
                if int(self.formula[i]) == 0:
                    m.addConstrs(self.z[i, h] ==1 for h in range(HORIZON))
                else:    
                    m = self.ap2smt(m, HORIZON, self.formula[i], self.z[i], 
                                    label_matrix, len(TDES.s), w)
                    
                stack = self.stack_manage(stack, del_list=[], set_list=[i])
    
        if len(stack) != 1 :
            print("SYNTAX ERROR: len(stack)={0},stack={1}".format(len(stack),stack))
    
        m.update()
    
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
                fz.write("\n{}".format(self.z.X[i,t,].reshape(GRAPH_SIZE_H,GRAPH_SIZE_V) ))
        fz.close()
        
        
   
        #os.makedirs(new_dir_path_recursive, exist_ok=True)
        
        for position_in_FORMULA in range(len_fml):
            for t in range(HORIZON):
                fig1 = plt.figure()
                    
                
                x1 = np.linspace(0, GRAPH_SIZE_H, num=GRAPH_SIZE_H)
                y = np.linspace(GRAPH_SIZE_V, 0, num=GRAPH_SIZE_V)
                X, Y = np.meshgrid(x1, y)
                r_4_4= self.z.X[position_in_FORMULA,t,:].reshape(GRAPH_SIZE_H, GRAPH_SIZE_V)
                Z = r_4_4
                
                plt.axes([0.025, 0.025, 0.95, 0.95])
                plt.imshow(Z, interpolation='nearest', cmap='bone', origin='upper', vmin=0.0,vmax=1.0)
                plt.colorbar(shrink=.92)
                
                plt.xticks(())
                plt.yticks(())
                #plt.show()
                plt.close(fig1)
              
                fig1.savefig(new_dir_path_recursive +'ell-{0}_z_pos-{1}_t-{2}.png'.format(self.ell, position_in_FORMULA, t))