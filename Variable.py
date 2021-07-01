
from z3 import*

#W is variables of state
def createVariable(size, h, g_type):

	W = [[0 for i in range(size)] for j in range(h)]

	for i in range(h):

		
		for j in range(size):

			w = Int(g_type + 'w{0}_{1}'.format(i,j))
			W[i][j] = w
			
	return W

def createVariable_G(size, h, n):

	W = [[0 for i in range(size)] for j in range(h)]

	for i in range(h):
	
		for j in range(size):

			w = Int('No{0}_w{1}_{2}'.format(n, i,j))
			W[i][j] = w
			
	return W

def createVariable_C(size, h, mode):

	W = [[0 for i in range(size)] for j in range(h)]

	for i in range(h):
	
		for j in range(size):

			name = mode + 'w{0}_{1}'.format(i,j)

			w = Int(name)
			W[i][j] = w
			
	return W


#Z is variable which represent whether sat or unsat the subformula in the time:t.
def createVariable_subF(num_subformula, h, g_type):

	Z = [[0 for i in range(h)] for j in range(num_subformula)] 

	for i in range(num_subformula):

		for j in range(h):

			z = Int(g_type + 'z{0}_{1}'.format(i,j))
			Z[i][j] = z
	
	return Z	

def createVariable_subF_o(num_subformula, h, string):

	X = [[0 for i in range(h)] for j in range(num_subformula)] 

	for i in range(num_subformula):

		for j in range(h):

			x = Int(string + '{0}_{1}'.format(i,j))
			X[i][j] = x
	
	return X	

def createVariable_subF_soft(number, num_subformula, h, g_type):


	Z = [[0 for i in range(h)] for j in range(num_subformula)] 

	for i in range(num_subformula):

		for j in range(h):

			z = Int(g_type + 'soft_z_{0}_{1}_{2}'.format(number, i, j))
			Z[i][j] = z
	
	return Z	



#zz is variable for until operator
def create_auxiliaryV(string, h):

	
	z = [0 for i in range(h)] 

	for i in range(h):

		Z = Int(string + '{}'.format(i))
		z[i] = Z

	return z

def create_auxiliaryM(string, line, row):

	
	z = [[0 for j in range(row)] for i in range(line)]

	for i in range(line):
		for j in range(row):

			str_l = '_l{}'.format(i)
			str_r = '_r{}'.format(j)
			STR = str_l + str_r
			Z = Int(string + STR)
			z[i][j] = Z

	return z

def create_auxiliaryV_G(string, h, num):

	
	z = [0 for i in range(h)] 
	str_num = 'No{}_'.format(num)

	for i in range(h):

		Z = Int(str_num + string + '{}'.format(i))
		z[i] = Z

	return z

def create_auxiliaryM_G(string, line, row, num):

	
	z = [[0 for j in range(row)] for i in range(line)]
	str_num = 'No{}_'.format(num)

	for i in range(line):
		for j in range(row):

			str_l = '_l{}'.format(i)
			str_r = '_r{}'.format(j)
			
			STR = str_l + str_r
			Z = Int(str_num + string + STR)
			z[i][j] = Z

	return z


def addCondition(s, W, Z, size, h, formula):

	
	for i in range(h):

		
		for j in range(size):


			s.add(0 <= W[i][j], W[i][j] <= 1)

		
		#print(sum(W[i]))
		s.add(sum(W[i]) == 1)


	#for c in range(n):
	num_subformula = len(formula)
	for a in range(num_subformula):
		
		for b in range(h):

			s.add(0 <= Z[a][b], Z[a][b] <= 1)

	return s


def addTransCondition(s, Mtrans, W, size, h):

	T_Mtrans = [[0 for i in range(size)] for j in range(size)] 

	T_Mtrans = list(map(list, zip(*Mtrans)))

	Sum = 0
	for i in range(h-1):

		for j in range(size):

			Sum = 0

			for k in range(size):

				Sum += W[i][k]*Mtrans[k][j]
			
			s.add(W[i+1][j] <= Sum)
			
	return s


def createVariable_event(h, g_type):

	E = [1 for i in range(h-1)]

	for j in range(h-1):
		e = Int(g_type + "e{}".format(j))
		E[j] = e

	return E

def createVariable_event_G(h, num):

	E = [1 for i in range(h-1)]

	for j in range(h-1):
		e = Int("No{0}_e{1}".format(num,j))
		E[j] = e

	return E


def addCondition_event(s, W, h, E, M_event, size):

	for a in range(h-1):

		s.add( 0 <= E[a], E[a] <= 1 )



	for i in range(h-1):

		Sum2 = 0

		for j in range(size):
		

			Sum1 = 0
			for k in range(size):

				Sum1 += W[i][k]*M_event[k][j]


			Sum2 += Sum1*W[i+1][j]

		

		s.add(E[i] <= Sum2, Sum2 < E[i] + 1 )

	return s

def addCondition_loop(s,W,z_loop,h,size,Mtrans):


	sum_loop=0
	for i in range(h):
		sum_loop += z_loop[i]
		for j in range(size):
			s.add(0 <= W[h][j], W[h][j] <= 1)

			s.add(W[h][j] <= W[i][j]+(1-z_loop[i]))
			s.add(W[h][j] >= W[i][j]-(1-z_loop[i]))


	s.add(sum_loop==1)



	T_Mtrans = [[0 for i in range(size)] for j in range(size)] 

	T_Mtrans = list(map(list, zip(*Mtrans)))

	Sum = 0

	for j in range(size):

		Sum = 0

		for k in range(size):

			Sum += W[h-1][k]*Mtrans[k][j]
		
		s.add(W[h][j] <= Sum)


	return s


