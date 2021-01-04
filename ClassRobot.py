
#from INFO import DATA_G_base_5 as DATA_G_base
from collections import defaultdict

#No = '_1'

class ROBOT():

	def __init__(self,horizon,LowerLimitI,UpperLimitI,LowerLimitJ,UpperLimitJ,
		number,NumInit,size):

		self.s_act = []
		self.event_act = []
		self.trans_act = defaultdict(list)
		self.istate_act = 'hoge'
		self.ap_act = []
		self.label_act = defaultdict(list)

		#self.cost = defaultdict(int)
		self.timed_event = defaultdict(list)
		self.subGraphList = []

		self.h = horizon
		
		self.input_data(LowerLimitI,UpperLimitI,LowerLimitJ,UpperLimitJ,number,NumInit,size)

		#self.base2act(trans_base)

	def input_data(self,LowerLimitI,UpperLimitI,LowerLimitJ,UpperLimitJ,number,NumInit,size):
		No='_{}'.format(number)
		"""
		size=8

		UpperLimitI=5
		UpperLimitJ=5
		LowerLimitI=0
		LowerLimitJ=0
		"""
		rangeI=range(size)
		rangeJ=range(size)
		for i in range(LowerLimitI,UpperLimitI+1):
			for j in range(LowerLimitJ,UpperLimitJ+1):
				state='s{0}{1}'.format(i,j)
				self.s_act.append(state+No)
		
		self.event_act =['up'+No,'down'+No,'left'+No,'right'+No]
		
		for i in range(size):
			for j in range(size):
				no=i*size+j
				if i==0:

					if j==0:
						self.trans_act[self.s_act[no]]=[
							[self.s_act[(i+1)*size+j],self.event_act[1]],
							[self.s_act[no+1],self.event_act[3]]
						]
					elif j==size-1:
						self.trans_act[self.s_act[no]]=[
							[self.s_act[(i-1)*size+j],self.event_act[1]],
							[self.s_act[no-1],self.event_act[2]]
						]
					else:
						self.trans_act[self.s_act[no]]=[
							[self.s_act[(i+1)*size+j],self.event_act[1]],
							[self.s_act[no-1],self.event_act[2]],
							[self.s_act[no+1],self.event_act[3]]
						]
				elif i==size-1:

					if j==0:
						self.trans_act[self.s_act[no]]=[
							[self.s_act[(i-1)*size+j],self.event_act[0]],
							[self.s_act[no+1],self.event_act[3]]
						]
					elif j==size-1:
						self.trans_act[self.s_act[no]]=[
							[self.s_act[(i-1)*size+j],self.event_act[0]],
							[self.s_act[no-1],self.event_act[2]]
						]
					else:
						self.trans_act[self.s_act[no]]=[
							[self.s_act[(i-1)*size+j],self.event_act[0]],
							[self.s_act[no-1],self.event_act[2]],
							[self.s_act[no+1],self.event_act[3]]
						]
				else:
					if j==0:
						self.trans_act[self.s_act[no]]=[
							[self.s_act[(i-1)*size+j],self.event_act[0]],
							[self.s_act[(i+1)*size+j],self.event_act[1]],
							[self.s_act[no+1],self.event_act[3]]
						]
					elif j==size-1:
						self.trans_act[self.s_act[no]]=[
							[self.s_act[(i-1)*size+j],self.event_act[0]],
							[self.s_act[(i+1)*size+j],self.event_act[1]],
							[self.s_act[no-1],self.event_act[2]]
						]
					else:
						self.trans_act[self.s_act[no]]=[
							[self.s_act[(i-1)*size+j],self.event_act[0]],
							[self.s_act[(i+1)*size+j],self.event_act[1]],
							[self.s_act[no-1],self.event_act[2]],
							[self.s_act[no+1],self.event_act[3]]
						]

		#2*size+3
		self.istate_act = self.s_act[NumInit]

		self.ap_act = ['H1','H2','P0','P1','P2','Other']

		for i in range(size):
			for j in range(size):
				no=i*size+j
				self.label_act[self.s_act[no]]='Other'

		for i in range(2):
			for j in range(2):
				no=i*size+j
				self.label_act[self.s_act[no]]='H1'

		if size==8:
			for i in range(2,6):
				for j in range(2,6):
					no=i*size+j
					self.label_act[self.s_act[no]]='P0'

			for i in range(6,8):
				for j in range(6,8):
					no=i*size+j
					self.label_act[self.s_act[no]]='H2'
		
			for i in range(6,8):
				for j in range(0,2):
					no=i*size+j
					self.label_act[self.s_act[no]]='P2'
		
			for i in range(0,2):
				for j in range(6,8):
					no=i*size+j
					self.label_act[self.s_act[no]]='P1'

		if number <=2:
			self.timed_event = {	
				self.event_act[0]:[1,3],
				self.event_act[1]:[1,3],
				self.event_act[2]:[1,3],
				self.event_act[3]:[1,3]
			}
		else:
			self.timed_event = {	
				self.event_act[0]:[2,3],
				self.event_act[1]:[2,3],
				self.event_act[2]:[2,3],
				self.event_act[3]:[2,3]
			}
