# -*- coding: utf-8 -*-
"""
Created on Fri Jul  2 17:27:39 2021

@author: takuma
"""
from collections import defaultdict


class DES():

    def __init__(self):

        self.name = ''
        self.s_act = []
        self.event_act = []
        self.trans_act = defaultdict(list)
        self.istate_act = 'hoge'
        self.ap_act = []
        self.label_act = defaultdict(list)
        self.timed_event = defaultdict(list)
        
        self.time_ratio = 0