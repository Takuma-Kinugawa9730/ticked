
#from INFO import DATA_G_base_5 as DATA_G_base
from collections import defaultdict


class create_G_act():

	def __init__(self,horizon):

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
		
		self.input_data()

		self.tick = 100 # 1 tick is defined by 100
		
		#self.base2act(trans_base)

	def input_data(self):

		self.s_act = [	'a0', 'ab',
				'b0',  'ba'
					]

		self.event_act =['move_ab', 'reach_ab', 
				 'move_ba', 'reach_ba', 
				]

		self.trans_act={
				self.s_act[0]:[[self.s_act[1],self.event_act[0]]],
				self.s_act[1]:[[self.s_act[2],self.event_act[1]]],
				self.s_act[2]:[[self.s_act[3],self.event_act[2]]],
				self.s_act[3]:[[self.s_act[0],self.event_act[3]]],
				 }


		"""
		self.trans_act={self.s_act[0]:[[self.s_act[1],self.event_act[12]]],
				self.s_act[1]:[[self.s_act[2],self.event_act[0]],
						[self.s_act[3],self.event_act[2]]],
				self.s_act[2]:[[self.s_act[4],self.event_act[1]],],
				self.s_act[3]:[[self.s_act[8],self.event_act[3]]],

				self.s_act[4]:[[self.s_act[5],self.event_act[12]]],
				self.s_act[5]:[[self.s_act[6],self.event_act[4]],
						[self.s_act[7],self.event_act[6]]],
				self.s_act[6]:[[self.s_act[7],self.event_act[5]],],
				self.s_act[7]:[[self.s_act[0],self.event_act[7]]],

				self.s_act[8]:[[self.s_act[9],self.event_act[12]]],
				self.s_act[9]:[[self.s_act[10],self.event_act[8]],
						[self.s_act[11],self.event_act[10]]],
				self.s_act[10]:[[self.s_act[0],self.event_act[9]],],
				self.s_act[11]:[[self.s_act[4],self.event_act[11]]] }
		"""		
		self.istate_act = self.s_act[0]
		self.ap_act = [	'A','m_ab','B', 'm_ba'] 
		self.label_act = {	self.s_act[0]:[self.ap_act[0]],
					self.s_act[1]:[self.ap_act[1]],
					self.s_act[2]:[self.ap_act[2]],
					self.s_act[3]:[self.ap_act[3]]
					
					
			}
		"""
		self.ap_act = [	'A', 'UnSearchedState_A', 'SearchedState_A', 
				'B', 'UnSearchedState_B', 'SearchedState_B', 
				'C', 'UnSearchedState_C', 'SearchedState_C', 
				
				'm_ab', 'm_ac', 'm_bc', 'm_ba', 'm_ca', 'm_cb'] 
		
		self.label_act = {	self.s_act[0]:[self.ap_act[0],self.ap_act[1]],
					self.s_act[1]:[self.ap_act[0],self.ap_act[2]],
					self.s_act[2]:[self.ap_act[9]],
					self.s_act[3]:[self.ap_act[10]],

					self.s_act[4]:[self.ap_act[3],self.ap_act[4]],
					self.s_act[5]:[self.ap_act[3],self.ap_act[5]],
					self.s_act[6]:[self.ap_act[11]],
					self.s_act[7]:[self.ap_act[12]],

					self.s_act[8]:[self.ap_act[6],self.ap_act[7]],
					self.s_act[9]:[self.ap_act[6],self.ap_act[8]],
					self.s_act[10]:[self.ap_act[13]],
					self.s_act[11]:[self.ap_act[14]],

					}
										
		"""
		#self.cost = defaultdict(int)

		self.timed_event = {	self.event_act[0]:[1,self.h],
					self.event_act[1]:[1,2],
					self.event_act[2]:[1,self.h],
					self.event_act[3]:[1,2]
						}

		"""
		self.timed_event = {	self.event_act[0]:[0,self.h],
					self.event_act[1]:[1,2],
					self.event_act[2]:[0,self.h],
					self.event_act[3]:[1,2],
					self.event_act[4]:[0,self.h],
					self.event_act[5]:[1,2],
					self.event_act[6]:[0,self.h],
					self.event_act[7]:[1,2],
					self.event_act[8]:[0,self.h],
					self.event_act[9]:[1,2],
					self.event_act[10]:[0,self.h],
					self.event_act[11]:[1,2],
					self.event_act[12]:[2,3]
						}

		"""
		self.subGraphList.append(self.ap_act[0])
		self.subGraphList.append(self.ap_act[2])
		
	
