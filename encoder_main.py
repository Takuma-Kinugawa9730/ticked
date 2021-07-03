# -*- coding: utf-8 -*-
"""
Created on Thu Jul  1 10:31:31 2021

@author: takuma
"""
import encoder_base

import gurobipy as gp#

epsilon = 0.01

class EncoderBool(encoder_base.EncoderBasis):

    def ap2smt(self, m, target_ap, HORIZON, z_curr, label_matrix, size_of_state, w):
        #T_w= [[0 for k in range(self.size)] for j in range(self.size)] 
        #T_w = list(map(list, zip(*self.w)))
        index = self.AP.index(target_ap)
        for h in range(HORIZON):    #h is horizon
            Sum = 0
            for j in range(size_of_state):
                Sum += label_matrix[index][j]*w[h][j]
            m.add(z_curr <= Sum )
            
            """
            ここ注意。epsilonを入れている            
            """
            m.add(z_curr + 1 - epsilon >= Sum)
        
        return m

    def negation2milp(self, m, HORIZON,z_curr,z_target):
    
        m.addConstrs(z_curr[t] == 1- z_target[t] 
            for t in range(HORIZON))
        
        return m
    
    
    def and2smt(self, m, HORIZON,
                     z_curr, z_target_list):
        
        for z_target in z_target_list:
            m.addConstrs(z_curr[t] <= z_target[t] for t in range(HORIZON) )
        
        for t in range(HORIZON):
            sum_z = 0 
            for z_target in z_target_list:
                sum_z = sum_z + z_target[t]
            m.addConstr(z_curr[t] >= 1 - len(z_target_list) + sum_z)
        return m
    
    def or2smt(self, m, HORIZON,
                     z_curr, z_target_list,
                     len_L):
        
        for z_target in z_target_list:
            m.addConstrs(z_curr[t] >= z_target[t] for t in range(HORIZON) )
        
        for t in range(HORIZON):
           
            sum_z = 0 
            for z_target in z_target_list:
                sum_z = sum_z + z_target[t]
            m.addConstr(z_curr[t] <= sum_z)
        return m



    def until2smt(self, m, HORIZON,
                  z_curr,z_target1,z_target2,
                  interval, position_in_formula, z_e):

        l = interval[0]
        r = interval[1]
        
        at_location = "_i{}".format(position_in_formula)
        
        zz_l = m.addMVar((HORIZON,HORIZON),vtype=gp.GRB.BINARY, name ="zz_psi1"+at_location)
        zz_r1 = m.addMVar((HORIZON,HORIZON),vtype=gp.GRB.BINARY, name ="zz_r1"+at_location)
        zz_and = m.addMVar((HORIZON,HORIZON),vtype=gp.GRB.BINARY, name ="zz_and"+at_location)
        zz_total1 = m.addMVar((HORIZON,HORIZON),vtype=gp.GRB.BINARY, name ="zz_total1"+at_location)
        zz_total2 = m.addMVar((HORIZON,HORIZON),vtype=gp.GRB.BINARY, name ="zz_total2"+at_location)
        zz_psi1 = m.addMVar((HORIZON,HORIZON),vtype=gp.GRB.BINARY, name ="zz_psi1"+at_location)
        

        Sum = [0 for z in range(HORIZON)]
    
        for x in range(HORIZON):


            for y in range(x, HORIZON):
    
                if y > x :

                    Sum[x] += z_e[y-1]
            
                    m.addConstr(zz_psi1[x][y] <= z_target1[y-1])
                    m.addConstr(zz_psi1[x][y] <= zz_psi1[x][y-1])
                    m.addConstr(zz_psi1[x][y] >= -1 + z_target1[y-1] + zz_psi1[x][y-1])
                    
                    
                else :
                    m.addConstr(zz_psi1[x][y] == 1)

                
                m.addConstr(zz_l[x][y] == (l <= Sum[x]))
                m.addConstr(zz_r1[x][y] == (Sum[x] <= r))
                
                
                
                m.addConstr(zz_and[x][y] <= zz_l[x][y])
                m.addConstr(zz_and[x][y] <= zz_r1[x][y])
                m.addConstr(zz_and[x][y] >= -1 + zz_r1[x][y] + zz_l[x][y])
                
                m.addConstr(zz_total1[x][y] <= zz_psi1[x][y])
                m.addConstr(zz_total1[x][y] <= zz_and[x][y])
                m.addConstr(zz_total1[x][y] <= z_target2[y])
                m.addConstr(zz_total1[x][y] >= 1 - 3 + zz_psi1[x][y]+zz_and[x][y]+z_target2[y])
    
        
        
                if y > x :

                    m.addConstr(zz_total2[x][y] >= zz_total1[x][y])
                    m.addConstr(zz_total2[x][y] >= zz_total2[x][y-1])
                    m.addConstr(zz_total2[x][y] <= zz_total1[x][y]+zz_total2[x][y-1])

                else:

                    m.addConstr(zz_total2[x][y] == zz_total1[x][y])

            if y== HORIZON-1:

                m.addConstr(z_curr[x] == zz_total2[x][HORIZON-1])
    
        return m


    
    def eventually2smt(self, m, HORIZON,z_curr,z_target1,
                       interval, position_in_formula):


        l = interval[0]
        r = interval[1]
        
        at_location = "_i{}".format(position_in_formula)
        
        zz_l = m.addMVar((HORIZON,HORIZON),vtype=gp.GRB.BINARY, name ="zz_psi1"+at_location)
        zz_r1 = m.addMVar((HORIZON,HORIZON),vtype=gp.GRB.BINARY, name ="zz_r1"+at_location)
        zz_and = m.addMVar((HORIZON,HORIZON),vtype=gp.GRB.BINARY, name ="zz_and"+at_location)
        zz_total1 = m.addMVar((HORIZON,HORIZON),vtype=gp.GRB.BINARY, name ="zz_total1"+at_location)
        zz_total2 = m.addMVar((HORIZON,HORIZON),vtype=gp.GRB.BINARY, name ="zz_total2"+at_location)
        zz_psi1 = m.addMVar((HORIZON,HORIZON),vtype=gp.GRB.BINARY, name ="zz_psi1"+at_location)
        

        Sum = [0 for z in range(HORIZON)]
    
        for x in range(HORIZON):


            for y in range(x, HORIZON):
    

                m.addConstr(zz_psi1[x][y] == 1)

                if y > x :

                    Sum[x] += self.e[y-1]
            
                    
                m.addConstr(zz_l[x][y] == (l <= Sum[x]))
                m.addConstr(zz_r1[x][y] == (Sum[x] <= r))
                m.addConstr(zz_and[x][y] <= zz_l[x][y])
                m.addConstr(zz_and[x][y] <= zz_r1[x][y])
                m.addConstr(zz_and[x][y] >= -1 + zz_r1[x][y] + zz_l[x][y])
    
                m.addConstr(zz_total1[x][y] <= zz_psi1[x][y])
                m.addConstr(zz_total1[x][y] <= zz_and[x][y])
                m.addConstr(zz_total1[x][y] <= z_target1[y])
                m.addConstr(zz_total1[x][y] >= 1-3+zz_psi1[x][y]+zz_and[x][y]+z_target1[y])
    
                if y > x :

                    m.addConstr(zz_total2[x][y] >= zz_total1[x][y])
                    m.addConstr(zz_total2[x][y] >= zz_total2[x][y-1])
                    m.addConstr(zz_total2[x][y] <= zz_total1[x][y]+zz_total2[x][y-1])

                else:

                    m.addConstr(zz_total2[x][y] == zz_total1[x][y])

            if y==HORIZON-1:

                m.addConstr(z_curr[x] == zz_total2[x][HORIZON-1])
    
        return m

    def grobal2smt(self, m, HORIZON,z_curr,z_target1,
                       interval, position_in_formula):
       
        l = interval[0]
        r = interval[1]
        
        at_location = "_i{}".format(position_in_formula)
        
        zz_l = m.addMVar((HORIZON,HORIZON),vtype=gp.GRB.BINARY, name ="zz_psi1"+at_location)
        zz_r1 = m.addMVar((HORIZON,HORIZON),vtype=gp.GRB.BINARY, name ="zz_r1"+at_location)
        zz_and = m.addMVar((HORIZON,HORIZON),vtype=gp.GRB.BINARY, name ="zz_and"+at_location)
        zz_total1 = m.addMVar((HORIZON,HORIZON),vtype=gp.GRB.BINARY, name ="zz_total1"+at_location)
        zz_total2 = m.addMVar((HORIZON,HORIZON),vtype=gp.GRB.BINARY, name ="zz_total2"+at_location)
        zz_psi1 = m.addMVar((HORIZON,HORIZON),vtype=gp.GRB.BINARY, name ="zz_psi1"+at_location)
        

        Sum = [0 for z in range(HORIZON)]
    
        for x in range(HORIZON):

            #print("\n\n{}".format(x))

            if l > HORIZON-1-x:

                m.addConstr(self.z[x] == 0)
                continue

            for y in range(x, HORIZON):
    

                m.addConstr(zz_psi1[x][y] == 1)

                if y > x :

                    Sum[x] += self.e[y-1]
            
                    
                m.addConstr(zz_l[x][y] == (l <= Sum[x]))
                m.addConstr(zz_r1[x][y] == (Sum[x] <= r))
                m.addConstr(zz_and[x][y] <= zz_l[x][y])
                m.addConstr(zz_and[x][y] <= zz_r1[x][y])
                m.addConstr(zz_and[x][y] >= -1 + zz_r1[x][y] + zz_l[x][y])
    
                m.addConstr(zz_total1[x][y] <= zz_psi1[x][y])
                m.addConstr(zz_total1[x][y] <= zz_and[x][y])
                m.addConstr(zz_total1[x][y] <= (1-z_target1[y]))
                m.addConstr(zz_total1[x][y] >= 1-3+zz_psi1[x][y]+zz_and[x][y]+ (1-z_target1[y]))
    
                if y > x :

                    m.addConstr(zz_total2[x][y] >= zz_total1[x][y])
                    m.addConstr(zz_total2[x][y] >= zz_total2[x][y-1])
                    m.addConstr(zz_total2[x][y] <= zz_total1[x][y]+zz_total2[x][y-1])

                else:

                    m.addConstr(zz_total2[x][y] == zz_total1[x][y])

            if y==HORIZON-1:

                m.addConstr(z_curr[x] == (1-zz_total2[x][HORIZON-1]))
    
        return m

   