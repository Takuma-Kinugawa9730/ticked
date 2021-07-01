
from z3 import*

from tickedLTL2SMT import *
from Function import Variable


#################################################################################
###############################      hard       #################################
#################################################################################

def set_hard_constrain(s, formula, M_ap, W, Mlabel, z, size_s, E, H, g_type):

	#add condition of satisfaction formula
	#s.add(z[len(formula[0])-1][0] == 1)
	#for n in range(len(formula)):
	for i in range(1, len(formula)+1):
	
		li = formula
		if type(li[len(formula)-i]) is str:
			s.add(z[len(formula)-i][0] == 1)
			#print("set:{}".format(len(formula)-i))
			break

		else:
			if i == len(formula)+1:
				print("error(1st in SetFormula)")
			
			else:
				continue


	tickedltl2SMT = tickedLTL2SMT_hard.tickedltl2smt(formula, M_ap, W, Mlabel, z, size_s, E, g_type)

	#Let's translation!
	print("hard constraints -> ILP")

	s = tickedltl2SMT.check(s, H)

	return s


def set_hard_constrain_inf(s, formula, M_ap, W, Mlabel, z, size_s, E, H, g_type,z_loop):

	#add condition of satisfaction formula
	#s.add(z[len(formula[0])-1][0] == 1)
	#for n in range(len(formula)):
	for i in range(1, len(formula)+1):
	
		li = formula
		if type(li[len(formula)-i]) is str:
			s.add(z[len(formula)-i][0] == 1)
			#print("set:{}".format(len(formula)-i))
			break

		else:
			if i == len(formula)+1:
				print("error(1st in SetFormula)")
			
			else:
				continue


	tickedltl2SMT_inf = tickedLTL2SMT_hard_inf.tickedltl2smt(formula, M_ap, W, Mlabel, z, size_s, E, g_type,z_loop)

	#Let's translation!
	print("hard constraints -> ILP")

	s = tickedltl2SMT_inf.check(s, H)

	return s


#################################################################################
###############################      soft       #################################
#################################################################################

def set_soft_constrain(s, set_formula_soft, M_ap, W, Mlabel, size_s, E, H, g_type):
	
	if len(set_formula_soft) != 0:

		print("soft constraints -> ILP")
		for i in range( len(set_formula_soft) ):

			li = set_formula_soft[i]

			soft_formula = li[0]
			point = li[1]

			soft_z=[[]]

			soft_z = Variable.createVariable_subF_soft(i, len(soft_formula), H, g_type)

			for a in range(len(soft_formula)):
		
				for b in range(H):

					s.add(0 <= soft_z[a][b], soft_z[a][b] <= 1)

			

			#print(i, soft_formula, point)

			for j in range(1, len(soft_formula)+1):
	
				li = soft_formula
				if type(li[len(soft_formula)-j]) is str:
					s.add_soft(soft_z[len(soft_formula)-j][0] == 1, point)
					#print("set:{}".format(len(soft_formula)-j))
					break

				else:
					if j == len(soft_formula)+1:
						print("error(1st in SetFormula)")
			
					else:
						continue

			tickedltl2SMT_soft = tickedLTL2SMT_soft.tickedltl2smt(soft_formula, M_ap, W, Mlabel, soft_z, size_s, E, i, g_type)

		#Let's translation!
			

			s = tickedltl2SMT_soft.check(s, H)

	
	else:
		print("no soft constrain")


	return s




