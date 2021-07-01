from collections import defaultdict
#import timedMAP_Gact
import copy
import itertools
import time
MaxEvent = 5

def refine(TDES):

	OpenList = []
	ClosedList = []
	EventCheck = []
	index_istate = TDES.s_with_clock.index(TDES.istate)

	OpenList.append('{}'.format(index_istate))
	#print(OpenList)
	print("start to search reachablity of TDES\n")
	start = time.time()
	while(1):
		if len(OpenList) == 0:

			break

		now = OpenList[0]
		OpenList.pop(0)
		ClosedList.append(now)
		
		for i in range(len(TDES.trans[now])):
			
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




class create_G():
	
	def __init__(self, tMap_G_act,H):

		self.s = []
		self.s_with_clock = []
		self.event = copy.copy(tMap_G_act.event_act)
		self.trans = defaultdict(list)
		self.istate = [tMap_G_act.istate_act]
		self.ap = copy.copy(tMap_G_act.ap_act)
		self.label_s = copy.copy(tMap_G_act.label_act)
		self.ref_timer = defaultdict(list)
		self.h=H
		self.G_act = tMap_G_act
        
        
		self.s_act2s(tMap_G_act.s_act, tMap_G_act.trans_act, tMap_G_act.timed_event)
		self.trans_act2trans()
	
	def s_act2s(self, s_act, trans_act, timed_event):
		
		self.event.append("tick")

		for i in range(len(s_act)):
			
			s = s_act[i]
			
			trans_from_s = copy.copy(trans_act[s])
			flag4istate=0
			if s == self.istate[0]:
				flag4istate=1
				
			T_sigma = []
			for j in range( len(trans_from_s) ):
				list1 = trans_from_s[j]
				
				if timed_event[list1[1]][1] == self.h:	#if remote event
					T_sigma.append(list(range(timed_event[list1[1]][0]+1)))
					
					if flag4istate==1:
						self.istate.append(timed_event[list1[1]][0])
	
				elif timed_event[list1[1]][1] < self.h:	#if prospective event
					T_sigma.append(list(range(timed_event[list1[1]][1]+1)))

					if flag4istate==1:
						self.istate.append(timed_event[list1[1]][1])
	
			if len(T_sigma)==1:
				timer0 = T_sigma[0]

				for t in timer0:
					list_new=[]
					list_new.append(s)
					list_new.append(timer0[t])
					self.s_with_clock.append(list_new)
					
			elif len(T_sigma)==2:
				timer0 = T_sigma[0]	
				timer1 = T_sigma[1]	
				product = list(itertools.product(timer0,timer1))
				
				for k in range(len(product)):
					timer = list(product[k])
					list_new=[]
					list_new.append(s)
					list_new.extend(timer)
					self.s_with_clock.append(list_new)
					
			elif len(T_sigma)==3:
				timer0 = T_sigma[0]	
				timer1 = T_sigma[1]	
				timer2 = T_sigma[2]	
				product = list(itertools.product(timer0,timer1,timer2))
				
				for k in range(len(product)):
					timer = list(product[k])
					list_new=[]
					list_new.append(s)
					list_new.extend(timer)
					self.s_with_clock.append(list_new)
					
			elif len(T_sigma)==4:
				timer0 = T_sigma[0]	
				timer1 = T_sigma[1]	
				timer2 = T_sigma[2]	
				timer3 = T_sigma[3]	
				product = list(itertools.product(timer0,timer1,timer2,timer3))
				
				for k in range(len(product)):
					timer = list(product[k])
					list_new=[]
					list_new.append(s)
					list_new.extend(timer)
					self.s_with_clock.append(list_new)
					
			elif len(T_sigma)==5:
				timer0 = T_sigma[0]	
				timer1 = T_sigma[1]	
				timer2 = T_sigma[2]	
				timer3 = T_sigma[3]	
				timer4 = T_sigma[4]	
				product = list(itertools.product(timer0,timer1,timer2,timer3,timer4))
				
				for k in range(len(product)):
					timer = list(product[k])
					list_new=[]
					list_new.append(s)
					list_new.extend(timer)
					self.s_with_clock.append(list_new)
					#print('s_with_clock <-{}'.format(self.s_with_clock[-1]))
			
			else:
				print("error. there are too many event occurred in a state")

		if self.istate not in self.s_with_clock:
			print('\nistate:{}'.format(self.istate))
			print("there is no istate")
		
		return
        
	def trans_act2trans(self):
		print('trans_act2trans')
		for i in range(len(self.s_with_clock)):
			occurable_event_at_s = []
			
			s1 = copy.copy(self.s_with_clock[i])
			
			s_act = s1[0]
			s_clock = []
			
			for j in range(1,len(s1)):
				s_clock.append(s1[j])
			trans_from_s = copy.deepcopy(self.G_act.trans_act[ s1[0] ])

			# transition s.t., s[0] -> trans_from_s[j][0] by trans[j][1] (in G_act)
			for j in range( len(trans_from_s) ):
				
				occurable_event_at_s.append(trans_from_s[j][1])


			# add the transition by tick
			next_clock = copy.copy(s_clock)
			flag = 0
			for j in range( len(next_clock) ):
				
				if s_clock[j] == 0:
					u_sigma = self.G_act.timed_event[occurable_event_at_s[j]][1]
					# if prospective event
					if u_sigma == self.h:# if remote event
						next_clock[j] = 0
					else:			
						
						flag = 1
						break
				else:
					next_clock[j] = next_clock[j]-1

			if flag == 0:
				destination_tick = [s_act]
				destination_tick.extend(next_clock)
				str_destination_tick = '{}'.format(self.s_with_clock.index(destination_tick))
				self.trans['{}'.format(i)].append([str_destination_tick,'tick'])

			else:
				pass



			# add transitons by other than tick
			for j in range( len(trans_from_s) ):
				# list1 mean list of [destination state from j, event] in G_act
				list1 = copy.deepcopy(self.G_act.trans_act[trans_from_s[j][0]])

				index1 = occurable_event_at_s.index(trans_from_s[j][1])
				clock = s_clock[index1]
				if self.G_act.timed_event[trans_from_s[j][1]][1] == self.h: #remote event
					if clock != 0:
						continue

				else:  #prospective event

					if (0 <= clock) and (clock <= self.G_act.timed_event[trans_from_s[j][1]][1]-self.G_act.timed_event[trans_from_s[j][1]][0]):
						pass
					else:
						continue

				#print('trans_from_s[j][0]={0},\nlist1={1}'.format(trans_from_s[j][0],list1))
				# decide timer of j
				destinate_clock = []
				for k in range( len(list1) ):
					
					#print('{}'.format(list1[k][1]))
					# if there is a share event in s_i and s_j (in G_act)
					if list1[k][1] in occurable_event_at_s:
						index = occurable_event_at_s.index(list1[k][1])
						destinate_clock.append(s_clock[index])

					else:
						# list[k][1] (occurable event at j) is remote event
						if self.G_act.timed_event[list1[k][1]][1] == self.h:
							destinate_clock.append(self.G_act.timed_event[list1[k][1]][0])

						# list[k][1] (occurable event at j) is prospective event
						else :
							destinate_clock.append(self.G_act.timed_event[list1[k][1]][1])

				destination = copy.copy([trans_from_s[j][0]])
				destination.extend(destinate_clock)
				#print('')
				str_destination = '{}'.format(self.s_with_clock.index(destination))
				str_event = '{}'.format(trans_from_s[j][1])
				self.trans['{}'.format(i)].append([str_destination,str_event])

	
		return


	def label2Matrix(self):

		Mlabel_func =[[0 for i in range(len(self.s_with_clock))] for j in range(len(self.ap))] 
		
		for k in range( len(self.s_with_clock)):
			li = self.s_with_clock[k]

			set_ap = self.label_s[li[0]]
			
			for j in range(len(set_ap)):

				for i in range(len(self.ap)):
				
					li = self.ap[i]

					if set_ap[j] == li:

						Mlabel_func[i][k] = 1 	
				
		return Mlabel_func
		


	def trans2Matrix(self):

		Mtrans_func = [[0 for i in range(len(self.s_with_clock))] for j in range(len(self.s_with_clock))]

		#num_state = len(self.s_with_clock)
		M_event =  [[0 for j in range(len(self.s_with_clock))]for j in range(len(self.s_with_clock))]

		for i in range( len(self.s_with_clock)):

			trans_from_i = self.trans['{}'.format(i)]
			for j in range( len(trans_from_i) ):

				# list1 is [next state from i, event]
				list1 = copy.copy(trans_from_i[j])
				next_state = int(list1[0])
				event = list1[1]
				
				Mtrans_func[i][next_state] = 1
				if event == 'tick':
					M_event[i][next_state] = 1
					

		return (Mtrans_func, M_event)		
	

