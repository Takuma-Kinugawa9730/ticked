# -*- coding: utf-8 -*-
"""
Created on Fri Jul  2 08:44:34 2021

@author: takuma
"""

from collections import defaultdict
import copy

class TDES():
    
    def __init__(self):
        
        self.name = ''
        self.s = []
        self.event = []
        self.delta = defaultdict(list)
        self.istate = []
        self.fin_state_act = 'hoge'
        self.ap = []
        self.label = defaultdict(list)
        self.time_ratio = 0
            
    
    def get_label_matrix(self):
    
        Mlabel_func =[[0 for i in range(len(self.s))] for j in range(len(self.ap))] 
        
        for k in range( len(self.s)):
            li = self.s[k]
    
            set_ap = self.label[li[0]]
            
            for j in range(len(set_ap)):
    
                for i in range(len(self.ap)):
                
                    li = self.ap[i]
    
                    if set_ap[j] == li:
    
                        Mlabel_func[i][k] = 1     
                
        return Mlabel_func
        
    
    
    def get_transition_matrix(self):
    
        Mtrans_func = [[0 for i in range(len(self.s))] for j in range(len(self.s))]
        alpha = [0 for j in range(len(self.s))]
        beta = [0 for j in range(len(self.s))]
        #M_event =  [[0 for j in range(len(self.s))]for j in range(len(self.s))]
    
        for i in range( len(self.s)):
    
            trans_from_i = self.delta['{}'.format(i)]
            for j in range( len(trans_from_i) ):
    
                list1 = copy.copy(trans_from_i[j])
                next_state = int(list1[0])
                event = list1[1]
                
                Mtrans_func[i][next_state] = 1
                if event == 'tick':
                    #M_event[i][next_state] = 1
                    if alpha[i] == 0:
                        alpha[i] = 1
                    if beta[next_state] == 0:
                        beta[next_state] = 1
                    
    
        return (Mtrans_func, alpha, beta)        
        
       
    def output(self, dir_path):
        file1 = open(dir_path + 'DATA_TDES-{}.txt'.format(self.name), 'w')
        file1.write('s:[state, clock for 1st event(clock1), clock for 2nd event(clock2), ...]\n')
        file1.write('{}\n\n'.format(self.s))
        file1.write('event\n')
        file1.write('{}\n\n'.format(self.event))
        file1.write('istate\n')
        file1.write('{}\n\n'.format(self.istate))
        file1.write('label:{atomic proposition:[states which satisfy the atomic proposition]}\n')
        file1.write('{}\n\n'.format(self.label))
        file1.write('ap\n')
        file1.write('{}\n\n'.format(self.ap))
        
        file1.close()
    
        file1 = open(dir_path+ 'DATA_TDES-{}_delta.txt'.format(self.name), 'w')
        file1.write('length of trans:{}'.format(len(self.delta)))
        
        file1.write('trans:{state of departure:[clock1,...,state of termination, event]}\n')
        for i in range(len(self.delta)):
            file1.write('{0}:{1}\n'.format(i,self.delta['{}'.format(i)]))
        
    
        return
    
        
