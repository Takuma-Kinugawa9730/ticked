
import class_des
        
def get_DES():
    
    
    SIZE_OF_H = 3
    SIZE_OF_V = 3
    
    des = class_des.DES()
    
    des.name = "p"
    des.have_refined_state = 1
    for i in range(SIZE_OF_H* SIZE_OF_V):
        des.s_act.append(str(i))
   
    des.event_act =['up', 'down', 'right', 'left']

    for i in range(SIZE_OF_H* SIZE_OF_V):
        des.event_act.append('up'    + "_at:{}".format(i))
        des.event_act.append('down'  + "_at:{}".format(i))
        des.event_act.append('right' + "_at:{}".format(i))
        des.event_act.append('left'  + "_at:{}".format(i))
            
        if i == 0:
            des.trans_act[des.s_act[0]] = [[des.s_act[1], des.event_act[2] + "_at:{}".format(i)], [des.s_act[ SIZE_OF_H], des.event_act[1] + "_at:{}".format(i)] ]
            
        elif i == SIZE_OF_H-1:
            des.trans_act[des.s_act[i]] = [[des.s_act[i-1], des.event_act[3] + "_at:{}".format(i)], [des.s_act[i + SIZE_OF_H],des.event_act[1] + "_at:{}".format(i)] ]
           
            
        elif i == SIZE_OF_H*(SIZE_OF_H-1):
            des.trans_act[des.s_act[i]] = [[des.s_act[i +1], des.event_act[2] + "_at:{}".format(i)], [des.s_act[i - SIZE_OF_H], des.event_act[0] + "_at:{}".format(i)] ]
           
            
            
        elif i == SIZE_OF_H* SIZE_OF_V-1:
            des.trans_act[des.s_act[i]] = [[des.s_act[i -1], des.event_act[3] + "_at:{}".format(i)], [des.s_act[i - SIZE_OF_H], des.event_act[0] + "_at:{}".format(i) ]]
            
        #上端
        elif i <= SIZE_OF_H-1:
            des.trans_act[des.s_act[i]] = [[des.s_act[i+1], des.event_act[2] + "_at:{}".format(i)], [des.s_act[i+SIZE_OF_H], des.event_act[1] + "_at:{}".format(i)],
                                           [des.s_act[i-1],des.event_act[3] + "_at:{}".format(i)] ]
            
        #下端
        elif i >= SIZE_OF_H*(SIZE_OF_H-1):
            des.trans_act[des.s_act[i]] = [[des.s_act[i+1], des.event_act[2] + "_at:{}".format(i)], [des.s_act[i -1], des.event_act[3] + "_at:{}".format(i)],
                                           [des.s_act[i - SIZE_OF_H],des.event_act[0] + "_at:{}".format(i)] ]
            
        #左端
        elif i % SIZE_OF_H == 0:
            des.trans_act[des.s_act[i]] = [[des.s_act[i+1], des.event_act[2] + "_at:{}".format(i)], [des.s_act[i - SIZE_OF_H],des.event_act[0] + "_at:{}".format(i)],
                                           [des.s_act[i+SIZE_OF_H],des.event_act[1] + "_at:{}".format(i)] ]
            
        #右端
        elif i % SIZE_OF_H == SIZE_OF_H-1:
            des.trans_act[des.s_act[i]] = [[des.s_act[i-1], des.event_act[3] + "_at:{}".format(i)], [des.s_act[i - SIZE_OF_H], des.event_act[0] + "_at:{}".format(i)],
                                           [des.s_act[i+SIZE_OF_H], des.event_act[1] + "_at:{}".format(i)] ]
            
        else:
            des.trans_act[des.s_act[i]] = [[des.s_act[i+1], des.event_act[2] + "_at:{}".format(i)], [des.s_act[i - 1], des.event_act[3] + "_at:{}".format(i)],
                                           [des.s_act[i - SIZE_OF_H],des.event_act[0] + "_at:{}".format(i)], [des.s_act[i+SIZE_OF_H],des.event_act[1] + "_at:{}".format(i)]
                                          ]
           
    des.istate_act = des.s_act[0]
    
    #ラベル0はダミーラベル
    des.ap_act = ['1', '2', '3', '4', '5'] 
    des.AP_R =["1", "2"]
    
    for i in range(SIZE_OF_H* SIZE_OF_V):
        
        des.label_act[des.s_act[i]]=['5']
        
    
    des.label_act[des.s_act[0]].append('start')
    des.label_act[des.s_act[-1]].append('goal')
            
    if SIZE_OF_H == 6:
        target_place = [[4,16,31], [19,33], [3,4,5,10,11,17]] # 6×6のグリッドの時
        des.AP_R =["1", "2"]
    
    else:
        target_place = [[2,5], [6],  [2]] # 3×3のグリッドの時
        des.AP_R =["1"]
    
    for number_tp in range(len(target_place)):
        for tp in target_place[number_tp]:
            des.label_act[des.s_act[tp]].append(des.ap_act[number_tp])
    
    for v in range(SIZE_OF_V):
        des.label_act[des.s_act[1 + v*SIZE_OF_H]].append(des.ap_act[-2])
    
    
    for e in range(len(des.event_act)):
        des.timed_event[des.event_act[e]].extend([1,-1])
    
    """
    des.timed_event = {    des.event_act[0]:[0,1],
                des.event_act[1]:[0,1],
                des.event_act[2]:[0,1],
                des.event_act[3]:[0,1]
                    }
    """
    des.time_ratio = -1
    return des
