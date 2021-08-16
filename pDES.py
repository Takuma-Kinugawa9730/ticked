
import class_des
        
def get_DES():
    
    
    SIZE_OF_H = 6
    SIZE_OF_V = 6
    
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
    des.ap_act = ['0', '1', '2', '3', '4', '5'] 
    
    for i in range(SIZE_OF_H* SIZE_OF_V): 
        des.label_act[des.s_act[i]]=['0']
        
    
    des.label_act[des.s_act[-1]].append('5')
            
    if SIZE_OF_H == 6:
        target_place = [[10,19], [3,4,5,10,11,17], [31,34] ] # 6×6のグリッドの時  del;
        des.AP_R =["1", "2", "3"]
    
    else:
        target_place = [[2,5], [6],  [2]] # 3×3のグリッドの時
        des.AP_R =["1"]
    
    for number_tp in range(len(target_place)):
        for tp in target_place[number_tp]:
            des.label_act[des.s_act[tp]].append(des.ap_act[number_tp])
    
    for v in range(SIZE_OF_V):
        des.label_act[des.s_act[2 + v*SIZE_OF_H]].append('4')
    
    
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
