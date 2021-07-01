#you write LTL(ticked LTL) by postfix notation(後置記法)
#this program understand only the formula written by postfix notation
#
#e.x.1
#G_[m,n] F_[s,t] (ap) --> ['ap', 'F', [s,t], 'G', [m,n ]]  i.e. as it is
#
#e.x.2
#G_[m,n] { G_[a,b] (ap1) & G_[c,d] F_[e,f] ( (not ap3) U_[m,n] ap4 ) }
#   -->['ap3', '!', 'ap4', 'U', [m,n], 'F', [e,f], 'G', [c,d], 'ap1', 'G', [a,b], '&', 'G', [m,n] ]  
#
#e.x.3
#()
#
#the basic strategy : until we find operator(boolean or temporal), 
#                     we stack atomic propositions or subformulas.
#


from Function import Variable


class ltl2smt:


# string is the formula which we translate into smt(ILP)
# type of formula is list
	def __init__(self, Formula, ap, w, Label, Z, size):     
                                
    	
		self.w = w		#list the set of unknown number(Matrix)
		self.label = Label	#Matrix　
		self.formula = Formula	#list
		self.AP = ap		#list
		self.stack = []
		self.z = Z		#list
		self.size = size	#the scall of set of state
		
#this function checks formula from begining of this formula.
#solver is a object of the class in z3

	def check(self, solver, h):    

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
					print(i)
					print("error!(1st in ltl2smt)")
					break
		
		if len(self.stack) != 1 :

			

			print('error(11th in ltl2smt)')	
			print(len(self.stack),self.stack)		
		
		return 	solver


	def ap2smt(self, i, s, h):


		T_w= [[0 for i in range(self.size)] for j in range(self.size)] 

		T_w = list(map(list, zip(*self.w)))


		index = self.AP.index(self.formula[i])
	
		for num in range(h):	#h is horizon

			Sum = 0

			for j in range(self.size):

				  Sum += self.label[index][j]*T_w[j][num]

			s.add(self.z[i][num] <= Sum )
			s.add(self.z[i][num] + 1 > Sum)


		self.set_stack(i)

		return s


	def negation2smt(self,i, s, h):

		if self.stack == False :

			print ("error(2nd in ltl2smt)")

		else :

			stack2 = self.stack[-1]
			for num in range(h):

				s.add(self.z[i][num] == 1 - self.z[stack2][num])

			self.del_stack(stack2)
			self.set_stack(i)

		return s

	

	def and2smt(self,i, s, h):

		if len(self.stack) <= 1:

			print('error(10th in ltl2smt)')


		stack1 = self.stack[-1]
		stack2 = self.stack[-2]


		for num in range(h):

			if stack1 != stack2:
				s.add(self.z[i][num] <= self.z[stack1][num])	

				s.add(self.z[i][num] <= self.z[stack2][num])	

				s.add(self.z[i][num] >= -1 + self.z[stack1][num] + self.z[stack2][num])
  			
			else :

				print("error(3rd in ltl2smt)")

		self.del_stack(stack1)
		self.del_stack(stack2)
		self.set_stack(i)


		return s


	def or2smt(self,i, s, h):


		if len(self.stack) <= 1:

			print('error(10th in ltl2smt)')



		stack1 = self.stack[-1]
		stack2 = self.stack[-2]


		for num in range(h):
			if stack1 != stack2:
				s.add(self.z[i][num] >= self.z[stack1][num])	

				s.add(self.z[i][num] >= self.z[stack2][num])	

				s.add(self.z[i][num] <= self.z[stack1][num] + self.z[stack2][num])
			
			else :

				print("error(4th in ltl2smt)")

		self.del_stack(stack1)
		self.del_stack(stack2)
		self.set_stack(i)

		return s



	def until2smt(self,i, s, h):


		if len(self.stack) <= 1:

			print('error(10th in ltl2smt)')


		zz = Variable.create_auxiliaryV('zz', h)		#list

		for j in range(h):

			s.add(0 <= zz[j], zz[j] <= 1)

		stack1 = self.stack[-2]
		stack2 = self.stack[-1]


		for num in range(h):

			if num == h-1:

				s.add(self.z[i][num] == self.z[stack2][num])

			else:
				s.add(self.z[i][num] >= self.z[stack2][num])
		
				s.add(zz[num] <= self.z[stack1][num])
				s.add(zz[num] <= self.z[i][num+1])
				s.add(zz[num] >= -1 + self.z[stack1][num] + self.z[i][num+1])

				s.add(self.z[i][num] >= zz[num])

				s.add(self.z[i][num] <= self.z[stack2][num] + zz[num]) 

  
		self.del_stack(stack2)
		self.del_stack(stack1)
		self.set_stack(i)

		return s


	def grobal2smt(self,i, s, h):

		flag = 1

		interval = self.formula[i+1]

		j = self.stack[-1]
		self.del_stack(j)

		if interval[0] > interval[1]:

			print("error(6th in ltl2smt)")

		r = interval[1]
		l = interval[0]

		if interval[1] > h:
			r = h 	#ここは要検討

		if interval[0] > h:
			s.add(self.z[i][0] == 0)		#もう論外
			
		Sum = 0
		for num2 in range(l, r+1):

			s.add(self.z[i][0] <= self.z[j][num2])
			
			Sum += self.z[j][num2]
			
		#print(Sum)
		#print(r-l+1)
		s.add(self.z[i][0] >= 1- (r-l+1) +Sum)

		self.set_stack(i)

		return s


	def eventually2smt(self,i, s, h):

		flag = 0

		interval = self.formula[i+1]

		r = interval[1]
		l = interval[0]
		
		j = self.stack[-1]
		self.del_stack(j)

		if interval[0] > interval[1]:

			print("error(7th in ltl2smt)")

		if interval[1] > h:
			r = h 	#ここは要検討

			
		if interval[0] > h:
			s.add(self.z[i][0] == 0)		#もう論外
			
		Sum = 0
		for num2 in range(l, r+1):

			s.add(self.z[i][0] >= self.z[j][num2])
			Sum += self.z[j][num2]
			
		s.add(self.z[i][0] <= Sum)

		self.set_stack(i)

		return s


	def set_stack(self, i):

		if i in self.stack == True:
			print("error(8th in ltl2smt)")

		else:

			self.stack.append(i)
	
	def del_stack(self, j):
		
		if self.stack[ len(self.stack) -1 ] == j:
		
			del self.stack[ len(self.stack) -1 ]

		else :

			print("error(9th in ltl2smt)")


#2019/9/16
#I finish making the rough program. I haven't consider around horizon.

#
#
		





