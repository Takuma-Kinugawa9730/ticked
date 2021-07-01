# -*- coding: utf-8 -*-
"""
Created on Thu Jul  1 10:31:31 2021

@author: takuma
"""
import encoder_base

class EncoderBool(encoder_base.EncoderBasis):

    def ap2smt(self, m, target_ap, HORIZON, z_curr):
        T_w= [[0 for k in range(self.size)] for j in range(self.size)] 
        T_w = list(map(list, zip(*self.w)))
        index = self.AP.index(target_ap)
        for num in range(HORIZON):	#h is horizon
            Sum = 0
            for j in range(self.size):
                Sum += self.label[index][j]*T_w[j][num]
            m.add(z_curr <= Sum )
            m.add(z_curr + 1 > Sum)
        
        return m

    def negation2milp(self, m, HORIZON,z_curr,z_target, len_L):
    
        m.addConstrs(z_curr[t,ell] == 1- z_target[t,ell] 
            for t in range(HORIZON) for ell in range(len_L))
        
        return m
    
    
    def and2smt(self, m, HORIZON,
                     z_curr, z_target_list,
                     len_L):
        
        for z_target in z_target_list:
            m.addConstrs(z_curr[t,ell] <= z_target[t,ell] for t in range(HORIZON) for ell in range(len_L))
        
        for t in range(HORIZON):
            for ell in range(len_L):
                sum_z = 0 
                for z_target in z_target_list:
                    sum_z = sum_z + z_target[t,ell]
                m.addConstr(z_curr[t,ell] >= 1 - len(z_target_list) + sum_z)
        return m
    
    def or2smt(self, m, HORIZON,
                     z_curr, z_target_list,
                     len_L):
        
        for z_target in z_target_list:
            m.addConstrs(z_curr[t,ell] >= z_target[t,ell] for t in range(HORIZON) for ell in range(len_L))
        
        for t in range(HORIZON):
            for ell in range(len_L):
                sum_z = 0 
                for z_target in z_target_list:
                    sum_z = sum_z + z_target[t,ell]
                m.addConstr(z_curr[t,ell] <= sum_z)
        return m



    def until2smt(self, m, HORIZON,
                  z_curr,z_target1,z_target2,
                  interval, position_in_formula, len_L):

        l = interval[0]
        r = interval[1]
		
        at_location = "_i{}".format(i)
        
        zz_l = m.addMVar((HORIZON,HORIZON),vtype=gp.GRB.BINARY, name ="zz_psi1"+at_location)
        zz_r1 = m.addMVar((HORIZON,HORIZON),vtype=gp.GRB.BINARY, name ="zz_r1"+at_location)
        zz_and = m.addMVar((HORIZON,HORIZON),vtype=gp.GRB.BINARY, name ="zz_and"+at_location)
        zz_total1 = m.addMVar((HORIZON,HORIZON),vtype=gp.GRB.BINARY, name ="zz_total1"+at_location)
        zz_total2 = m.addMVar((HORIZON,HORIZON),vtype=gp.GRB.BINARY, name ="zz_total2"+at_location)
        zz_psi1 = m.addMVar((HORIZON,HORIZON),vtype=gp.GRB.BINARY, name ="zz_psi1"+at_location)
		
		stack1 = self.stack[-2]
		stack2 = self.stack[-1]

		Sum = [0 for z in range(h)]
	
		for x in range(h):


			for y in range(x, h):
	
				if y > x :

					Sum[x] += self.e[y-1]
			
					s.add(zz_psi1[x][y] <= self.z[stack1][y-1])
					s.add(zz_psi1[x][y] <= zz_psi1[x][y-1])
					
					s.add(zz_psi1[x][y] >= -1 + self.z[stack1][y-1] + zz_psi1[x][y-1])

					
				else :

					s.add(zz_psi1[x][y] == 1)

				
				s.add(zz_l[x][y] == (l <= Sum[x]))
				s.add(zz_r1[x][y] == (Sum[x] <= r))
				s.add(zz_and[x][y] <= zz_l[x][y])
				s.add(zz_and[x][y] <= zz_r1[x][y])
				s.add(zz_and[x][y] >= -1 + zz_r1[x][y] + zz_l[x][y])
	
				s.add(zz_total1[x][y] <= zz_psi1[x][y])
				s.add(zz_total1[x][y] <= zz_and[x][y])
				s.add(zz_total1[x][y] <= self.z[stack2][y])
				s.add(zz_total1[x][y] >= 1-3+zz_psi1[x][y]+zz_and[x][y]+self.z[stack2][y])
	
				if y > x :

					s.add(zz_total2[x][y] >= zz_total1[x][y])
					s.add(zz_total2[x][y] >= zz_total2[x][y-1])
					s.add(zz_total2[x][y] <= zz_total1[x][y]+zz_total2[x][y-1])

				else:

					s.add(zz_total2[x][y] == zz_total1[x][y])

			if y==h-1:

				s.add(self.z[i][x] == zz_total2[x][h-1])
	
		return s

	def eventually2smt(self, m, HORIZON,z_curr,z_target1,
                       interval, len_L):


		if type(self.formula[i+1]) is list:
			interval = self.formula[i+1]
			
			l = interval[0]
			r = interval[1]
			#print(i,l,r)
		else:
			print("error")


		zz_l = Variable.create_auxiliaryM(self.type + 'zz_l_i{}'.format(i), h, h)
		
		zz_r1 = Variable.create_auxiliaryM(self.type + 'zz_r1_i{}'.format(i), h, h)
		zz_and = Variable.create_auxiliaryM(self.type + 'zz_and_i{}'.format(i), h, h)	
		zz_total1 = Variable.create_auxiliaryM(self.type + 'zz_total1_i{}'.format(i), h, h)
		zz_total2 = Variable.create_auxiliaryM(self.type + 'zz_total2_i{}'.format(i), h, h)
		zz_psi1 = Variable.create_auxiliaryM(self.type + 'zz_psi1_i{}'.format(i), h, h)

		for j in range(h):

			for k in range(h):
				s.add(0 <= zz_total1[j][k], zz_total1[j][k] <= 1)
				s.add(0 <= zz_total2[j][k], zz_total2[j][k] <= 1)

				s.add(0 <= zz_psi1[j][k], zz_psi1[j][k] <= 1)
				s.add(0 <= zz_l[j][k], zz_l[j][k] <= 1)
				s.add(0 <= zz_r1[j][k], zz_r1[j][k] <= 1)
		
				s.add(0 <= zz_and[j][k], zz_and[j][k] <= 1)

		stack2 = self.stack[-1]

		Sum = [0 for z in range(h)]
	
		for x in range(h):

			#print("\n\n{}".format(x))

			#if l > h-1-x:

			#	s.add(self.z[i][x] == 0)
			#	continue


			for y in range(x, h):
	

				s.add(zz_psi1[x][y] == 1)

				if y > x :

					Sum[x] += self.e[y-1]
			
					
				s.add(zz_l[x][y] == (l <= Sum[x]))
				s.add(zz_r1[x][y] == (Sum[x] <= r))
				s.add(zz_and[x][y] <= zz_l[x][y])
				s.add(zz_and[x][y] <= zz_r1[x][y])
				s.add(zz_and[x][y] >= -1 + zz_r1[x][y] + zz_l[x][y])
	
				s.add(zz_total1[x][y] <= zz_psi1[x][y])
				s.add(zz_total1[x][y] <= zz_and[x][y])
				s.add(zz_total1[x][y] <= self.z[stack2][y])
				s.add(zz_total1[x][y] >= 1-3+zz_psi1[x][y]+zz_and[x][y]+self.z[stack2][y])
	
				if y > x :

					s.add(zz_total2[x][y] >= zz_total1[x][y])
					s.add(zz_total2[x][y] >= zz_total2[x][y-1])
					s.add(zz_total2[x][y] <= zz_total1[x][y]+zz_total2[x][y-1])

				else:

					s.add(zz_total2[x][y] == zz_total1[x][y])

			if y==h-1:

				s.add(self.z[i][x] == zz_total2[x][h-1])
	
		self.del_stack(stack2)
		
		self.set_stack(i)

		return s

	def grobal2smt(self, m, HORIZON,z_curr,z_target1,
                       interval, len_L):

		if type(self.formula[i+1]) is list:
			interval = self.formula[i+1]
			
			l = interval[0]
			r = interval[1]

		else:
			print("error")


		
		zz_l = Variable.create_auxiliaryM(self.type + 'zz_l_i{}'.format(i), h, h)
		
		zz_r1 = Variable.create_auxiliaryM(self.type + 'zz_r1_i{}'.format(i), h, h)
		zz_and = Variable.create_auxiliaryM(self.type + 'zz_and_i{}'.format(i), h, h)	
		zz_total1 = Variable.create_auxiliaryM(self.type + 'zz_total1_i{}'.format(i), h, h)
		zz_total2 = Variable.create_auxiliaryM(self.type + 'zz_total2_i{}'.format(i), h, h)
		zz_psi1 = Variable.create_auxiliaryM(self.type + 'zz_psi1_i{}'.format(i), h, h)


		for j in range(h):

			for k in range(h):
				s.add(0 <= zz_total1[j][k], zz_total1[j][k] <= 1)
				s.add(0 <= zz_total2[j][k], zz_total2[j][k] <= 1)

				s.add(0 <= zz_psi1[j][k], zz_psi1[j][k] <= 1)
				s.add(0 <= zz_l[j][k], zz_l[j][k] <= 1)
				s.add(0 <= zz_r1[j][k], zz_r1[j][k] <= 1)
		
				s.add(0 <= zz_and[j][k], zz_and[j][k] <= 1)

		stack2 = self.stack[-1]

		Sum = [0 for z in range(h)]
	
		for x in range(h):

			#print("\n\n{}".format(x))

			if l > h-1-x:

				s.add(self.z[i][x] == 0)
				continue

			for y in range(x, h):
	

				s.add(zz_psi1[x][y] == 1)

				if y > x :

					Sum[x] += self.e[y-1]
			
					
				s.add(zz_l[x][y] == (l <= Sum[x]))
				s.add(zz_r1[x][y] == (Sum[x] <= r))
				s.add(zz_and[x][y] <= zz_l[x][y])
				s.add(zz_and[x][y] <= zz_r1[x][y])
				s.add(zz_and[x][y] >= -1 + zz_r1[x][y] + zz_l[x][y])
	
				s.add(zz_total1[x][y] <= zz_psi1[x][y])
				s.add(zz_total1[x][y] <= zz_and[x][y])
				s.add(zz_total1[x][y] <= (1-self.z[stack2][y]))
				s.add(zz_total1[x][y] >= 1-3+zz_psi1[x][y]+zz_and[x][y]+ (1-self.z[stack2][y]))
	
				if y > x :

					s.add(zz_total2[x][y] >= zz_total1[x][y])
					s.add(zz_total2[x][y] >= zz_total2[x][y-1])
					s.add(zz_total2[x][y] <= zz_total1[x][y]+zz_total2[x][y-1])

				else:

					s.add(zz_total2[x][y] == zz_total1[x][y])

			if y==h-1:

				s.add(self.z[i][x] == (1-zz_total2[x][h-1]))
	
		self.del_stack(stack2)
		
		self.set_stack(i)

		return s

