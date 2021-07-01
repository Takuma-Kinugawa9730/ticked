from collections import defaultdict
#import timedMAP_G
import time
import copy
def refine(TDES):

	OpenList = []
	ClosedList = []
	EventCheck = []
	index_istate = TDES.s_with_clock.index(TDES.istate)

	OpenList.append('{}'.format(index_istate))
	#print(OpenList)
	print("strat to search reachablity of TDES\n")
	start = time.time()
	while(1):
		if len(OpenList) == 0:

			break

		now = OpenList[0]
		OpenList.pop(0)
		ClosedList.append(now)
		#print(now)
		#trans_from_now = copy.deepcopy(TDES.trans[now])
		#print('TDES.trans[now] ={}'.format(TDES.trans['{}'.format(now)]))
		#print('TDES.trans[] ={}'.format(TDES.trans))
		for i in range(len(TDES.trans[now])):
			#trans = copy.copy(trans_from_now[i])
			#print('int(trans[0])={}'.format(int(trans[0])))

			if TDES.trans[now][i][0] not in ClosedList:
				OpenList.append(TDES.trans[now][i][0])

			if TDES.trans[now][i][1] not in EventCheck:
				EventCheck.append(TDES.trans[now][i][1])

	t = time.time() - start
	print('finish refining, time={}'.format(t))

	#ClosedList.sort()

	list1 = list(range(len(TDES.s_with_clock)))
	list1.reverse()
	for i in list1:

		if str(i) not in ClosedList:

			TDES.s_with_clock.pop(i)
			#TDES.trans.pop('{}'.format(i))

	#print(TDES.s_with_clock.index(['s0_t0',0,5,0]))
	#print(TDES.s_with_clock)
	TDES.trans = defaultdict(list)
	TDES.trans_act2trans()

	print('size of s={}'.format(len( TDES.s_with_clock )))
	print('size of trans={}'.format(len( TDES.trans)))

	list2 = list(range(len(TDES.event)))
	list2.reverse()
	for j in list2:

		if TDES.event[j] not in EventCheck:
			TDES.event.pop(j)

	return TDES

