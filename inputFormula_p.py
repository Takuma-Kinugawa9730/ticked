
from z3 import*
#import tickedLTL2SMT_hard 
#import tickedLTL2SMT_soft
from tickedLTL2SMT import*
#H = 30


def inputF(M_ap,H):

	subformula = []	

	####################################
	# input formulas (hard constarain) #
	####################################
	
	
	subformula.append(['A', 'F', [0,H]])
	subformula.append(['B', 'F', [0,H]])
	subformula.append(['B', '!', 'B', '!', 'F', [3,3], '|', 'G', [0,H]])
	#subformula.append(['A', '!', 'G', [10,12]])
	"""
	subformula.append(['charged', 'F', [0,10],'G', [0, H]])
#	subformula.append(['end', '!', 'G', [0, H]])
#	subformula.append(['hold', 'A', '&', 'F', [0,10]])
	subformula.append(['hold', 'A', '&','!','sleep', 'B', '&', 'F', [0,5],'|','G', [0, 6]])
	subformula.append(['rechargeableState','A','&', 'F', [0,5], '!'])
	subformula.append(['rechargeableState','A','&', 'F', [10,15] ,'!'])
	subformula.append(['allset', 'm_ab', '&', 'F', [0, H], '!'])
	subformula.append(['allset', 'm_ba', '&', 'F', [0, H], '!'])
	"""
	formula = []
	for i in range(len(subformula)):

		formula = formula + subformula[i]

		if i != 0 :
			formula = formula + ["&"]

	print('hard constrain')
	print(formula)

	####################################
	# input formulas (soft constarain) #
	####################################

	set_formula_soft = []
	"""
	set_formula_soft.append( (['hold', 'A', '&', 'F', [0,6]], 2) )	
	"""
	set_formula_soft.append( (['A', 'G', [0,3], 'F', [5,10]], 1) )	
	set_formula_soft.append( (['A', 'F', [5,8], 'G', [0,H]], 1) )	
	set_formula_soft.append( (['B', 'F', [5,8], 'G', [0,H]], 1) )	

	#set_formula_soft.append( (['hold','A','&','!', 'sleep','B', '&', 'F', [3,5], '|', 'F', [0, H]], 1)  )	
	#set_formula_soft.append((['rechargeableState','A','&', 'F', [0,5], '!'], 2))
	#set_formula_soft.append((['rechargeableState','B','&', 'F', [5,10] ,'!'], 2))
	#set_formula_soft.append((['hold', 'A', '&','!','sleep', 'B', '&', 'F', [0,5],'|'], 2))
	#set_formula_soft.append((['rechargeableState','A','&',  'F','!', [15,20]], 2))

	print('soft constrain')
	print(set_formula_soft)

	return (formula, set_formula_soft)





