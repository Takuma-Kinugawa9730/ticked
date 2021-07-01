
from Function import LTL2SMT
from Function import Variable
#from Function import *
class tickedltl2smt(LTL2SMT.ltl2smt):

	def __init__(self, Formula, ap, w, Label, Z, size, e, g_type):

		#super(tickedltl2smt, self).__init__(Formula, ap, w, Label, Z, size) 
		self.w = w		#list the set of unknown number(Matrix)
		self.label = Label	#Matrix　
		self.formula = Formula	#list
		self.AP = ap		#list
		self.stack = []
		self.z = Z		#list
		self.size = size	#the scall of set of state

		self.e = e
	
		self.type = g_type

	def check(self, solver, h):    
		print("formula:{}".format(self.formula))
		for i in range(len(self.formula)):	#i represent subfomula
	    	
			if self.formula[i] in self.AP:
                
				solver = self.ap2smt(i, solver, h)

			elif self.formula[i] == '!':

				solver = self.negation2smt(i, solver, h)

			elif self.formula[i] == '&':

				solver = self.and2smt(i, solver, h)

			elif self.formula[i] == '|':

				solver = self.or2smt(i, solver, h)

			elif self.formula[i] == 'U':
                    
				solver = self.until2smt(i, solver, h)
				i+=1
				if i >= len(self.formula):
					break

			elif self.formula[i] == 'G':

				solver = self.grobal2smt(i, solver, h)
				i+=1
				if i >= len(self.formula):
					break

			elif self.formula[i] == 'F':

				solver = self.eventually2smt(i, solver, h)
				i+=1
				if i >= len(self.formula):
					break


			else:

				if type(self.formula[i]) == list:

					continue

				else:
					print(i,self.formula[i])
					print("error!(1st in ltl2smt)")
					break
		
		if len(self.stack) != 1 :

			

			print('error(11th in ltl2smt)')	
			print(len(self.stack),self.stack)		
		
		return 	solver



	def until2smt(self,i, s, h):

		if type(self.formula[i+1]) is list:
			interval = self.formula[i+1]
			
			l = interval[0]
			r = interval[1]

		else:
			print("error")



		if len(self.stack) <= 1:

			print('error(10th in ltl2smt)')


		
		zz_l = Variable.create_auxiliaryM(self.type + 'zz_l_i{}'.format(i), h, h)
		
		zz_r1 = Variable.create_auxiliaryM(self.type + 'zz_r1_i{}'.format(i), h, h)
		zz_and = Variable.create_auxiliaryM(self.type + 'zz_and_i{}'.format(i), h, h)	
		zz_total1 = Variable.create_auxiliaryM(self.type + 'zz_total1_i{}'.format(i), h, h)
		zz_total2 = Variable.create_auxiliaryM(self.type + 'zz_total2_i{}'.format(i), h, h)
		zz_psi1 = Variable.create_auxiliaryM(self.type + 'zz_psi1_i{}'.format(i), h, h)

		for j in range(h):

			for k in range(h):

				s.add(0 <= zz_total1[j][k], zz_total1[j][k] <= 1)
				s.add(0 <= zz_psi1[j][k], zz_psi1[j][k] <= 1)
				s.add(0 <= zz_l[j][k], zz_l[j][k] <= 1)
				s.add(0 <= zz_r1[j][k], zz_r1[j][k] <= 1)
				s.add(0 <= zz_total2[j][k], zz_total2[j][k] <= 1)
		
				s.add(0 <= zz_and[j][k], zz_and[j][k] <= 1)


		stack1 = self.stack[-2]
		stack2 = self.stack[-1]

		Sum = [0 for z in range(h)]
	
		for x in range(h):

			#print("\n\n{}".format(x))

			#if l > h-1-x:

			#	s.add(self.z[i][x] == 0)
			#	continue


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
	
		self.del_stack(stack2)
		self.del_stack(stack1)
		self.set_stack(i)

		return s

	def eventually2smt(self,i, s, h):


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

	def grobal2smt(self,i, s, h):

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


		"""
		zz_l = Variable.create_auxiliaryM('soft{0}_zz_l_i{1}'.format(self.n, i), h, h)
		
		zz_r1 = Variable.create_auxiliaryM('soft{0}_zz_r1_i{1}'.format(self.n, i), h, h)
		zz_and = Variable.create_auxiliaryM('soft{0}_zz_and_i{1}'.format(self.n, i), h, h)	
		zz_total1 = Variable.create_auxiliaryM('soft{0}_zz_total1_i{1}'.format(self.n, i), h, h)
		zz_total2 = Variable.create_auxiliaryM('soft{0}_zz_total2_i{1}'.format(self.n, i), h, h)
		zz_psi1 = Variable.create_auxiliaryM('soft{0}_zz_psi1_i{1}'.format(self.n, i), h, h)
		"""

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



	"""
	def grobal2smt(self,i, s, h):

		if type(self.formula[i+1]) is list:
			interval = self.formula[i+1]
			
			l = interval[0]
			r = interval[1]

		else:
			print("error")



		#if len(self.stack) <= 1:

		#	print('error(10th in ltl2smt)')


		zz = Variable.create_auxiliaryM('zz_i{}'.format(i), h, h)		#list
		zz12 = Variable.create_auxiliaryV('zz12_i{}'.format(i), h)
		
		zz_l = Variable.create_auxiliaryM('zz_l_i{}'.format(i), h, h)
		
		zz_r1 = Variable.create_auxiliaryM('zz_r1_i{}'.format(i), h, h)
		zz_r2 = Variable.create_auxiliaryM('zz_r2_i{}'.format(i), h, h)		#list
		zz_r3 = Variable.create_auxiliaryM('zz_r3_i{}'.format(i), h, h)	
	
		zz_and = Variable.create_auxiliaryM('zz_and_i{}'.format(i), h, h)		#list
		zz_req = Variable.create_auxiliaryV('zz_req_i{}'.format(i), h)
		zzz = Variable.create_auxiliaryM('zzz_i{}'.format(i), h, h)		#list
		zz_total1 = Variable.create_auxiliaryM('zz_total1_i{}'.format(i), h, h)
		zz_psi2 = Variable.create_auxiliaryM('zz_total2_i{}'.format(i), h, h)

		zz_1 = Variable.create_auxiliaryM('zz_1_i{}'.format(i), h, h)
		zz_2 = Variable.create_auxiliaryV('zz_2_i{}'.format(i), h)		#list
		zz_3 = Variable.create_auxiliaryV('zz_3_i{}'.format(i), h)	

		zz_x = Variable.create_auxiliaryM('zz_x_i{}'.format(i), h, h)		#list


		for j in range(h):

			s.add(0 <= zz_req[j], zz_req[j] <= 1)
			s.add(0 <= zz_3[j], zz_3[j] <= 1)
			#s.add(0 <= zz_1[j], zz_1[j] <= 1)
			s.add(0 <= zz_2[j], zz_2[j] <= 1)
			s.add(0 <= zz12[j], zz12[j] <= 1)
			#s.add(0 <= zz_x[j], zz_x[j] <= 1)

			for k in range(h):

				s.add(0 <= zz[j][k], zz[j][k] <= 1)
				

				s.add(0 <= zz_total1[j][k], zz_total1[j][k] <= 1)
				s.add(0 <= zzz[j][k], zzz[j][k] <= 1)

				s.add(0 <= zz_psi2[j][k], zz_psi2[j][k] <= 1)
				s.add(0 <= zz_l[j][k], zz_l[j][k] <= 1)
				s.add(0 <= zz_r1[j][k], zz_r1[j][k] <= 1)
				s.add(0 <= zz_r2[j][k], zz_r2[j][k] <= 1)
				s.add(0 <= zz_r3[j][k], zz_r3[j][k] <= 1)
			
				s.add(0 <= zz_and[j][k], zz_and[j][k] <= 1)
				s.add(0 <= zz_1[j][k], zz_1[j][k] <= 1)
				#s.add(0 <= zz_2[j][k], zz_2[j][k] <= 1)
				s.add(0 <= zz_x[j][k], zz_x[j][k] <= 1)
	

		#stack1 = self.stack[-2]
		stack2 = self.stack[-1]

		Sum = [0 for z in range(h)]
		Sum_zz_total1= [0 for z in range(h)]
		#Sum_zz_12= [0 for z in range(h)]
	

		for x in range(h):

			#print("\n\n{}".format(x))

			#if l > h-1-x:

			#	s.add(self.z[i][x] == 0)
			#	continue


			for y in range(x, h):
				#print(y)

				if y != x :

					Sum[x] += self.e[y-1]


				s.add(zz_l[x][y] == (l <= Sum[x]))
				s.add(zz_r1[x][y] == (Sum[x] <= r))
				s.add(zz_and[x][y] <= zz_l[x][y])
				s.add(zz_and[x][y] <= zz_r1[x][y])
				s.add(zz_and[x][y] >= -1 + zz_r1[x][y] + zz_l[x][y])
	

				s.add(zz_total1[x][y] >= 1 - zz_and[x][y])
				s.add(zz_total1[x][y] >= self.z[stack2][y])
				s.add(zz_total1[x][y] <= 1 - zz_and[x][y] + self.z[stack2][y])
			
				s.add(zz_2[x] <= zz_total1[x][y])

				Sum_zz_total1[x] += zz_total1[x][y]

			s.add(zz_2[x] >= 1 - (h-x) + Sum_zz_total1[x])
			s.add(zz_req[x] == (l <= Sum[x]))

			s.add(self.z[i][x] <= zz_req[x])
			s.add(self.z[i][x] <= zz_2[x])
			s.add(self.z[i][x] >= 1 - 2 + zz_req[x] + zz_2[x] )

		self.del_stack(stack2)
		#self.del_stack(stack1)
		self.set_stack(i)


		return s

	"""


