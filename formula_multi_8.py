
from z3 import*
#import tickedLTL2SMT_hard 
#import tickedLTL2SMT_soft
#import outer_hard

H=30
overT=15
N=8
def inputF(M_ap):

	subformula = []	

	####################################
	# input formulas (hard constarain) #
	####################################

	#subformula.extend([(['A_0', 'A_1', '|', 'F', [0,3]], 2), (['B_0', 'B_1', '|', 'F', [3,10]], 2), "&"])
	
	#subformula.extend([(['H1', 'H2', '|', 'F', [0,10], 'G',[0,H]], 8), ([,"|"], 8), 'F', "!", "&"])
	"""
	subformula.extend( [ (['H1', 'H2', '|', 'F', [0,5], 'G', [0,H]], N) ] )
	subformula.extend( [ (['P0'],N-4), 'G'] )
	subformula.extend( [ (['P1'],N-5), 'G'] )
	subformula.extend( [ (['P2'],N-5), 'G'] )
	subformula.extend( [ (['P0', 'G', [0,5]],1), 'G'] )
	subformula.extend( [ (['H1', 'H2', '|', 'F', [overT-1,overT]], N) ] )
	"""
	#subformula.extend( [ ([M_ap[1],'!',M_ap[2],'F',[2,3],'|','G',[2,4]],2) ] )
	#subformula.extend( [ ([M_ap[1]],2),'!',([M_ap[2],'F',[3,4]],2),'|','G' ] )
	#subformula.extend( [ ([M_ap[2],'F',[3,4]],2)] )

	formula=[ 
		(['H1', 'H2', '|', 'F', [0,5], 'G', [0,H]], 8), (['P0'],3), 'G', '&',
		(['P1'],2), 'G', '&', (['P2'],2), 'G', '&', (['P0', 'G', [0,5]],1), 'G','&',
		(['H1', 'H2', '|', 'F', [overT-1,overT]], 8), '&'	
	]

	"""
	formula = []
	for i in range(len(subformula)):

		formula.append(subformula[i])

		if i != 0 :
			formula = formula + ["&"]
	"""
	
	print('hard constraints')
	#print(subformula)
	print(formula)
	
	print('\n')
	
	####################################
	# input formulas (soft constarain) #
	####################################

	set_formula_soft = []

	#set_formula_soft.append( [[([M_ap[2], 'F', [3, 6]], 2)], 8] )	
	#set_formula_soft.append( [[([M_ap[0], 'F', [3, 6]], 2)], 2] )
	
	#set_formula_soft.append( [[([M_ap[1], 'F', [2, 3]], 2)], 2] )
	#set_formula_soft.append( [[([M_ap[1]], 2),'F'], 2] )

	#set_formula_soft.append( [[([M_ap[1], 'F', [7, 9]], 2)], 2] )
	#set_formula_soft.append( [[([M_ap[2]], 2),'F'], 1] )
	#set_formula_soft.append( [ [([M_ap[1]], 2), 'F', "!"],4])
	print('soft constraints')
	print(set_formula_soft)
	print('\n')

	return (formula, set_formula_soft)
#	return (subformula, set_formula_soft)
