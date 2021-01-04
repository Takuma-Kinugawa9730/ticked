
#from INFO import DATA_G_base_6_0 as G_base_0
#from INFO import DATA_G_base_6_1 as G_base_1

#from INFO_for_multi import Gact_0 as tMAP_act_0
#from INFO_for_multi import Gact_1 as tMAP_act_1
from Function import timedMAP_G
"""
from INFO_for_multi import R1
from INFO_for_multi import R2
from INFO_for_multi import R3
from INFO_for_multi import R4
from INFO_for_multi import R5
from INFO_for_multi import R6
from INFO_for_multi import R7
from INFO_for_multi import R8
"""
from INFO_for_multi import ClassRobot

from z3 import*
#import tickedLTL2SMT_hard 
#import tickedLTL2SMT_soft
from Function import Variable
#import AfterSolve
from Function import AfterSolve_G
from Function import write_data_G_G_act
#import inputFormula
from INFO_for_multi import formula_multi_4 as inputFormula_counting
from tickedLTL2SMT import outer as outer
#import Cordinate
import time
import datetime
import os
now = datetime.datetime.today()
DATE = '{0}-{1}-{2}'.format(now.year,now.month,now.day)
DATETIME = '{0}:{1}'.format(now.hour,now.minute)
def exe_z3(solver):
	
	print("start to solve")
	"""
##################on going#######################
	for i in range(10):

		string = '{}'.format(solver.check())

		print(string)

#############################################
	"""
	
	start = time.time()

	print(solver.check())

	t = time.time() - start

	print("solving time: {}".format(t))
	file1 = open('DATA/multi/'+DATE+'/'+DATETIME+'/'+'data.txt', 'a')
	file1.write("solving time: {}\n".format(t))
	file1.close()
	li = []
	li2 = []
	m = solver.model()
	#print(m)
	li = m.decls()	
	file1 = open('DATA/multi/'+DATE+'/'+DATETIME+'/'+'not_sort_output.txt', 'w')
	
	for i in range(len(li)):

		file1.write('{}'.format(li[i])) 
		file1.write('\n')

	file1.close()

	#print(s.sexpr())
	return m

###  group control  ###
if	__name__ == '__main__':

	os.makedirs('DATA/multi/'+DATE+'/'+DATETIME,exist_ok=True)


	start = time.time()
	#define horizon
	H = inputFormula_counting.H			#実行列の長さ
	overT=inputFormula_counting.overT	#終了時刻（便宜上定義）
	N = inputFormula_counting.N			#エージェントの数
	#print("horizon: {}".format(H))
	file1 = open('DATA/multi/'+DATE+'/'+DATETIME+'/'+'data.txt', 'a')
	file1.write("horizon: {}\n".format(H))
	file1.write("over T: {}\n".format(overT))
	file1.write("The number of agents: {}\n".format(N))
	file1.close()
	"""
	#エージェントが活動するマップをsize×sizeの行列で表現
	size=8

	#初期位置
	NumInit=[2*size+3,2*size+2,3*size+2,7*4+5,7*5+5,7*5+4,7,7*8]
	"""
	size=4

	#初期位置
	NumInit=[1,1,2,2]
	G_act=[]
	for i in range(N):
		
		G_act.append(
			ClassRobot.ROBOT(H,0,3,0,3, i+1,NumInit[i],size)
		)
	
	Map = []
	Mlabel = []
	MtransFunc = []
	M_event = []
	AP = G_act[0].ap_act
	size = []

	#DESからTDESを取得し，N体のエージェント分をリストに保存する
	for i in range(N):

		tMap = timedMAP_G.create_G(G_act[i],H)
		write_data_G_G_act.writeData(G_act[i],tMap,'No{}'.format(i), 'multi')
		#print("get {}th matrix of label".format(i))	
		#Mlabel_0 = tMap.label2Matrix()
		(MtransFunc_0, M_event_0) = tMap.trans2Matrix()
		#AP.extend(tMap.ap)

		Map.append(tMap)
		#Mlabel.append(Mlabel_0)
		MtransFunc.append(MtransFunc_0)
		M_event.append(M_event_0)
		size.append(len(tMap.s_with_clock))
	#print(AP)
	for i in range(N):
		Map[i].ap = copy.copy(AP)
		#print("get {}th matrix of label".format(i))	
		Mlabel_0 = Map[i].label2Matrix()
		Mlabel.append(Mlabel_0)

	formula_o = []
	set_formula_soft_o= []

	(formula_o, set_formula_soft_o) = inputFormula_counting.inputF(AP)
	file1 = open('DATA/multi/'+DATE+'/'+DATETIME+'/'+'data.txt', 'a')
	file1.write("outer (hard): {}\n".format(formula_o))
	file1.write("outer (soft): {}\n".format(set_formula_soft_o))
	file1.close()

	#s = Solver()
	s = Optimize()

	#create boolean variable
	#W is a matrix whose scale is (len(state) * H)
	print('translate into ILP constraints\n')
	W = [0 for n in range(N)]
	for i in range(N):
		W[i]=Variable.createVariable_G(len(Map[i].s_with_clock), H, i)
		s.add(W[i][0][Map[i].s_with_clock.index(Map[i].istate)] == 1)  
	
	#print(W)

	#print(Map.s_with_clock.index(Map.istate))


	#Since I define W[i][j] as integer 
	#and I want treate W as boolean , 
	#I must add the condition, 0 <= W[i][j], W[i][j] <= 1
	for n in range(N):
		
		for i in range(H):
			
			for j in range(len(Map[n].s_with_clock)):

				s.add(0 <= W[n][i][j], W[n][i][j] <= 1)
			
			#print(sum(W[i]))
			s.add(sum(W[n][i]) == 1)
	print("1")
	#converse label function to matrix 
	#Mlabel = Map.label_func2Matrix()

	#converse transition function to matrix
	#MtransFunc = Map.trans2Matrix()

	#add condition about the variable of state 
	#0 <= W[i][j], W[i][j] <= 1
	for i in range(N):
		s = Variable.addTransCondition(s, MtransFunc[i], W[i], len(Map[i].s_with_clock), H)
	print("2")
	E = [0 for k in range(N)]
	for i in range(N):

		E[i] = Variable.createVariable_event_G(H,i)


	for i in range(N):
		s = Variable.addCondition_event(s, W[i], H, E[i], M_event[i], len(Map[i].s_with_clock))
	print("3")
	#translate ltl to integer linear program

	### hard ###
	y = Variable.createVariable_subF_o(len(formula_o), H, "y")
	num_subformula = len(formula_o)
	for a in range(num_subformula):
			
		for b in range(H):

			s.add(0 <= y[a][b], y[a][b] <= 1)
	if len(formula_o) !=0:
		s.add( y[len(formula_o)-1][0]==1 )
	
	Out = outer.outerLogic2smt(formula_o, AP, W, Mlabel, y, size, E, 0, 'hard')
	s = Out.check(s,H,N)
	print("4")
	### soft ###
	y_soft = []
	softFormula = []
	for i in range(len(set_formula_soft_o)):
		
		y_s = Variable.createVariable_subF_o(len(formula_o), H, "y_soft_i{0}".format(i))

		li_with_point = set_formula_soft_o[i]
		li_cLTL = li_with_point[0]
		point = li_with_point[1]
		print(i,li_cLTL,point)
		num_subformula = len(li_cLTL)
		y_s = Variable.createVariable_subF_o(num_subformula, H, "y_soft_i{0}".format(i))

		for a in range(num_subformula):
		
			for b in range(H):

				s.add(0 <= y_s[a][b], y_s[a][b] <= 1)

		if len(li_cLTL) != 0:
			s.add_soft(y_s[len(li_cLTL)-1][0]==1, point)
		
		#In = outer.outerLogic2smt(li_cLTL, Map.ap, W, Mlabel, y_s, len(Map.s_with_clock), E, i, 'soft')
		In = outer.outerLogic2smt(li_cLTL, AP, W, Mlabel, y_s, len(Map.s_with_clock), E, i, 'soft')
			
		s = In.check(s,H,N)
	print("5")

	#s = inputFormula.set_soft_constrain(s, set_formula_soft, Map.ap, W, Mlabel, len(Map.s_with_clock), E,H)

	t = time.time() - start

	file1 = open('DATA/multi/'+DATE+'/'+DATETIME+'/'+'data.txt', 'a')
	file1.write("start -> before solve time: {}\n".format(t))
	file1.close()

	model = exe_z3(s)
	
	# we use s_with_clock for size
	#(sort_E,sort_W) = AfterSolve_G.Sort(model, H, [Map[0].s_with_clock, Map[1].s_with_clock], formula_o, N)
	(sort_E,sort_W) = AfterSolve_G.Sort(model, H, Map, formula_o, N)
	
	"""
	Cordinate.cordinate(sort_E,sort_W,Map,N,H)

	sort_E_0 = sort_E[0]
	sort_E_1 = sort_E[1]

	sort_W_0 = sort_W[0]
	sort_W_1 = sort_W[1]
	"""
	#sort_E = AfterSolve.Sort(model, H, Map.s_with_clock, formula_o, set_formula_soft)
	#AfterSolve.createGraph(tMap_act.s_act, tMap_act.trans_act, tMap_act.timed_event, H, sort_E)









