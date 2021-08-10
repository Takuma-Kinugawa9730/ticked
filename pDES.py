
import class_des
        
def get_DES():
    
    
    SIZE_OF_H = 8
    SIZE_OF_V = 8
    
    des = class_des.DES()
    
    des.name = "p"
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
    des.ap_act = ['1', '2', '3', '4', 'goal', 'start', '0', '-1'] 
    
    for i in range(SIZE_OF_H* SIZE_OF_V):
        des.label_act[des.s_act[i]]=['0']
        
    
    des.label_act[des.s_act[0]].append('start')
    des.label_act[des.s_act[-1]].append('goal')
            
    
    target_place = [[34,14], [12,30], [33,50], [47,62]] # 8×8のグリッドの時
    #target_place = [[0], [1], [2], [3]] # 2×2のグリッドの時
    for number_tp in range(len(target_place)):
        for tp in target_place[number_tp]:
            des.label_act[des.s_act[tp]].append(des.ap_act[number_tp])
    
    for v in range(SIZE_OF_V):
        des.label_act[des.s_act[4 + v*8]].append(des.ap_act[-1])
    
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
