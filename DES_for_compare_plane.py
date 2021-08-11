
import class_des
        
def get_DES():

    des = class_des.DES()
    
    des.name = "3_2"
    des.have_refined_state = -1
    #des.s_act = ['0', '1', '2']
    des.s_act = ['0', '1']
    
    #des.event_act =['01', '02', '10', '12', '20', '21']
    des.event_act =['01',  '10']
    
    """
    des.trans_act={
            des.s_act[0]:[[des.s_act[1],des.event_act[0]],
                          [des.s_act[2],des.event_act[1]]],
            des.s_act[1]:[[des.s_act[0],des.event_act[2]],
                          [des.s_act[2],des.event_act[3]]],
            des.s_act[2]:[[des.s_act[0],des.event_act[4]],
                          [des.s_act[1],des.event_act[5]]]
            }
    """
    des.trans_act={
            des.s_act[0]:[[des.s_act[1],des.event_act[0]]],
            des.s_act[1]:[[des.s_act[0],des.event_act[1]]]
            }
    
    for event in des.event_act:
        
        des.timed_event[event] = [4, -1]
    
    N = 3 #各階層の状態数
    
    
    
    for s in des.s_act:
        add_states = []
        for i1 in range(N-1):
            
            add_states.append( s + "_{}".format(i1))
            des.s_act.append(add_states[-1])
            
            
            des.event_act.append(s + "-" + add_states[-1])
            des.trans_act[s].append([add_states[-1], des.event_act[-1]])
            des.timed_event[des.event_act[-1]] = [0, -1]
            
            des.event_act.append(add_states[-1] + "-" + s)
            des.trans_act[add_states[-1]] = [s, des.event_act[-1]]
            des.timed_event[des.event_act[-1]] = [0, -1]
            
            for i2 in range(N-1):
                des.s_act.append(add_states[-1] + "_{}".format(i2))
                    
                des.event_act.append(add_states[-1] + "-" + des.s_act[-1])
                des.trans_act[add_states[-1]].append([s, des.event_act[-1]])
            
                des.event_act.append(des.s_act[-1] + "-" + add_states[-1])
                des.trans_act[des.s_act[-1]] = [add_states[-1], des.event_act[-1]]
                des.timed_event[des.event_act[-1]] = [0, -1]
            
            des.event_act.append(des.s_act[-1] + "-" + des.s_act[-2])
            des.trans_act[des.s_act[-1]].append([des.s_act[-2],des.event_act[-1]])
            des.timed_event[des.event_act[-1]] = [1, -1]
            
            des.event_act.append(des.s_act[-2] + "-" + des.s_act[-1])
            des.trans_act[des.s_act[-2]].append([des.s_act[-1],des.event_act[-1]])
            des.timed_event[des.event_act[-1]] = [1, -1]
            
        if len(add_states) == N-1:
            des.event_act.append(add_states[0] + "-" + add_states[1])
            des.trans_act[add_states[0]].append([add_states[1],des.event_act[-1]])
            des.timed_event[des.event_act[-1]] = [2, -1]
            
            des.event_act.append(add_states[1] + "-" + add_states[0])
            des.trans_act[add_states[1]].append([add_states[0],des.event_act[-1]])
            des.timed_event[des.event_act[-1]] = [2, -1]
            
        else:
            print("*\nERROR\n*\n")




    des.istate_act = des.s_act[0]
    des.fin_state_act = des.s_act[-1]
    des.ap_act = list(range(len(des.s_act)))
    
    for state in des.s_act:
        des.label_act[state] = [des.ap_act[des.ap_act[ des.s_act.index(state) ]]]
    
    
    """
    上位TDESとの単位時間のずれ
    0以上1以下の数になる
    """
    des.time_ratio = 0.75
    return des