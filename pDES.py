
import class_des
        
def get_DES():
    
    
    SIZE_OF_H = 5 
    SIZE_OF_V = 5
    
    des = class_des.DES()
    
    des.name = "p"
    for i in range(SIZE_OF_H* SIZE_OF_V):
        des.s_act.append(str(i))
    """
    des.s_act = [    'a0', 'ab', 'ac',
            'b0', 'bc', 'ba',
            'c0', 'ca', 'cb'    ]
    """
    
    des.event_act =['up', 'down', 'right', 'left']

    for i in range(SIZE_OF_H* SIZE_OF_V):
        if i == 0:
            des.trans_act[des.s_act[0]] = [[des.s_act[1], 'right'], [des.s_act[ SIZE_OF_H],'down'] ]
            
        elif i == SIZE_OF_H:
            des.trans_act[des.s_act[i]] = [[des.s_act[i-1], 'left'], [des.s_act[i + SIZE_OF_H],'down'] ]
            
        elif i == SIZE_OF_H*(SIZE_OF_H-1):
            des.trans_act[des.s_act[i]] = [[des.s_act[i +1], 'right'], [des.s_act[i - SIZE_OF_H],'up'] ]
            
        elif i == SIZE_OF_H* SIZE_OF_V-1:
            des.trans_act[des.s_act[i]] = [[des.s_act[i -1], 'left'], [des.s_act[i - SIZE_OF_H],'up'] ]
            
            
        #上端
        elif i <= SIZE_OF_H-1:
            des.trans_act[des.s_act[i]] = [[des.s_act[i+1], 'right'], [des.s_act[i+SIZE_OF_H],'down'], [des.s_act[i-1],'left'] ]
            
        #下端
        elif i >= SIZE_OF_H*(SIZE_OF_H-1):
            des.trans_act[des.s_act[i]] = [[des.s_act[i+1], 'right'], [des.s_act[i -1], 'left'], [des.s_act[i - SIZE_OF_H],'up'] ]
            
        #左端
        elif i % SIZE_OF_H == 0:
            des.trans_act[des.s_act[i]] = [[des.s_act[i+1], 'right'], [des.s_act[i - SIZE_OF_H],'up'], [des.s_act[i+SIZE_OF_H],'down'] ]
           
        #右端
        elif i % SIZE_OF_H == SIZE_OF_H-1:
            des.trans_act[des.s_act[i]] = [[des.s_act[i-1], 'left'], [des.s_act[i - SIZE_OF_H],'up'], [des.s_act[i+SIZE_OF_H],'down'] ]
            
        else:
            des.trans_act[des.s_act[i]] = [[des.s_act[i+1], 'right'],[des.s_act[i - 1], 'left'],
                                           [des.s_act[i - SIZE_OF_H],'up'], [des.s_act[i+SIZE_OF_H],'down']
                                          ]
    """
    des.trans_act={
            des.s_act[0]:[[des.s_act[1],des.event_act[0]],
                    [des.s_act[2],des.event_act[2]]],
            des.s_act[1]:[[des.s_act[3],des.event_act[1]]],
            des.s_act[2]:[[des.s_act[6],des.event_act[3]]],
            
            des.s_act[3]:[[des.s_act[4],des.event_act[4]],
                    [des.s_act[5],des.event_act[6]]],
            des.s_act[4]:[[des.s_act[6],des.event_act[5]]],
            des.s_act[5]:[[des.s_act[0],des.event_act[7]]],
            
            des.s_act[6]:[[des.s_act[7],des.event_act[8]],
                    [des.s_act[8],des.event_act[10]]],
            des.s_act[7]:[[des.s_act[0],des.event_act[9]]],
            des.s_act[8]:[[des.s_act[3],des.event_act[11]]] }
    """

    des.istate_act = des.s_act[0]
    des.ap_act = ['1', '2', '3', '4', 'goal', 'start', '0'] 
    
    for i in range(SIZE_OF_H* SIZE_OF_V):
        des.label_act[des.s_act[i]]=['0']
        
    
    des.label_act[des.s_act[0]].append('start')
    des.label_act[des.s_act[-1]].append('goal')
            
    target_place = [2,8,15,21]
    for t in range(len(target_place)):
        des.label_act[des.s_act[target_place[t]]].append(des.ap_act[t])
        
        
    """
    des.label_act = {    des.s_act[0]:[des.ap_act[0]],
                des.s_act[1]:[des.ap_act[3]],
                des.s_act[2]:[des.ap_act[4]],
                
                des.s_act[3]:[des.ap_act[1]],
                des.s_act[4]:[des.ap_act[5]],
                des.s_act[5]:[des.ap_act[6]],

                des.s_act[6]:[des.ap_act[2]],
                des.s_act[7]:[des.ap_act[7]],
                des.s_act[8]:[des.ap_act[8]],
                
        }
    """
 
    des.timed_event = {    des.event_act[0]:[1,-1],
                des.event_act[1]:[1,2],
                des.event_act[2]:[1, -1],
                des.event_act[3]:[1,2],
                des.event_act[4]:[1,-1],
                des.event_act[5]:[1,2],
                des.event_act[6]:[1,-1],
                des.event_act[7]:[1,2],
                des.event_act[8]:[1,-1],
                des.event_act[9]:[1,2],
                des.event_act[10]:[1,-1],
                des.event_act[11]:[1,2]
                    }

    des.time_ratio = -1
    return des
