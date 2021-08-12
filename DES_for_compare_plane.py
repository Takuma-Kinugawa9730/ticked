
import class_des
        
def get_DES():

    des = class_des.DES()
    
    des.name = "plain"
    des.have_refined_state = -1
    
    
    all_states = [['0', '1', '2', '3']]
    
    all_states.append(['10', '11', '12', '13'])
    list_connected_states = [['1','10']]
    list_connected_states.append(['13','1'])
    
    all_states.append(['110', '111', '112', '113'])
    list_connected_states.append(['11','110'])
    list_connected_states.append(['113','11'])
    
    
    all_states.append(['120', '121', '122', '123'])
    list_connected_states.append(['12','120'])
    list_connected_states.append(['123','12'])
    
    
    all_states.append(['20', '21', '22', '23'])
    list_connected_states.append(['2','20'])
    list_connected_states.append(['23','2'])
    
    all_states.append(['210', '211', '212', '213'])
    list_connected_states.append(['21','210'])
    list_connected_states.append(['213','21'])
    """HORIZON
    all_states.append(['220', '221', '222', '223'])
    list_connected_states.append(['22','220'])
    list_connected_states.append(['223','22'])
    """
    for states in all_states:
        
        if len(states[0]) == 1: 
            lower_time = 2
        elif len(states[0]) == 2: 
            lower_time = 1
        elif len(states[0]) == 3: 
            lower_time = 1
        else:
            print("*\n error at lower time: {}\n*\n".format(states[0]))
            
        for from_s in states:
            
            des.s_act.append(from_s)
            
            if from_s[-1] == '3':
                des.event_act.append(from_s + "-" + from_s)    
                if from_s in des.trans_act:
                    print("*\n error at final state: {}\n*\n".format(states[0]))
                else :
                    des.trans_act[from_s] = [[from_s, des.event_act[-1]]]
                
                des.timed_event[des.event_act[-1]] = [0, -1]
            
            for to_s in states:
                if from_s == to_s:
                    continue
                
                des.event_act.append(from_s + "-" + to_s)    
                if from_s in des.trans_act:
                    des.trans_act[from_s].append([to_s, des.event_act[-1]])
                else :
                    des.trans_act[from_s] = [[to_s, des.event_act[-1]]]
                
                des.timed_event[des.event_act[-1]] = [lower_time, -1]
              
    for connected_states in list_connected_states:
        from_s = connected_states[0]
        to_s = connected_states[1]
        
        des.event_act.append(from_s + "-" + to_s)    
        if from_s in des.trans_act:
            des.trans_act[from_s].append([to_s, des.event_act[-1]])
        else :
            print("*\n error at connected_states\n*\n")
        
        des.timed_event[des.event_act[-1]] = [0, -1]
      
    
    """
    
    
    top_states = ['0', '1', '2']
    des.s_act = ['0', '1', '2']
    des.event_act =['01', '02', '10', '12', '20', '21']
    
    des.trans_act={
            des.s_act[0]:[[des.s_act[1],des.event_act[0]],
                          [des.s_act[2],des.event_act[1]]],
            des.s_act[1]:[[des.s_act[0],des.event_act[2]],
                          [des.s_act[2],des.event_act[3]]],
            des.s_act[2]:[[des.s_act[0],des.event_act[4]],
                          [des.s_act[1],des.event_act[5]]]
            }
    
    
    """
    """
    top_states = ['0', '1']
    des.s_act = ['0', '1']
    des.event_act =['01',  '10']
    des.trans_act={
            des.s_act[0]:[[des.s_act[1],des.event_act[0]]],
            des.s_act[1]:[[des.s_act[0],des.event_act[1]]]
            }
    """
    
    
    """
    for event in des.event_act:
        
        des.timed_event[event] = [4, -1]
    
    N = 3 #各階層の状態数
    for s in top_states:
        add_states = []
        for i1 in range(N-1):
            
            add_states.append( s + "_{}".format(i1))
            des.s_act.append(add_states[-1])
            
            
            des.event_act.append(s + "-" + add_states[-1])
            des.trans_act[s].append([add_states[-1], des.event_act[-1]])
            des.timed_event[des.event_act[-1]] = [2, -1]
            
            des.event_act.append(add_states[-1] + "-" + s)
            if add_states[-1] in des.trans_act:
                des.trans_act[add_states[-1]].append([s, des.event_act[-1]])
            else :
                des.trans_act[add_states[-1]] = [s, des.event_act[-1]]
            des.timed_event[des.event_act[-1]] = [2, -1]
            
            for i2 in range(N-1):
                des.s_act.append(add_states[-1] + "_{}".format(i2))
                    
                des.event_act.append(add_states[-1] + "-" + des.s_act[-1])
                if add_states[-1] in des.trans_act:
                    des.trans_act[add_states[-1]].append([des.s_act[-1], des.event_act[-1]])
                else:
                    des.trans_act[add_states[-1]] = [des.s_act[-1], des.event_act[-1]]
                
                des.timed_event[des.event_act[-1]] = [1, -1]
            
                des.event_act.append(des.s_act[-1] + "-" + add_states[-1])
                if des.s_act[-1] in des.trans_act:
                    print("*\nERROR at {0}\n*\n".format(des.s_act[-1]))
                else:
                    des.trans_act[des.s_act[-1]] = [add_states[-1], des.event_act[-1]]
                
                des.timed_event[des.event_act[-1]] = [1, -1]
            
            des.event_act.append(des.s_act[-1] + "-" + des.s_act[-2])
            if des.s_act[-1] in des.trans_act:
                des.trans_act[des.s_act[-1]].append([des.s_act[-2],des.event_act[-1]])
            else:
                print("*\nERROR at {0}\n*\n".format(des.s_act[-1]))
                
            des.timed_event[des.event_act[-1]] = [1, -1]
            
            des.event_act.append(des.s_act[-2] + "-" + des.s_act[-1])
            if des.s_act[-2] in des.trans_act:
                des.trans_act[des.s_act[-2]].append([des.s_act[-1],des.event_act[-1]])
            else:
                print("*\nERROR at {0}\n*\n".format(des.s_act[-2]))
                
            des.timed_event[des.event_act[-1]] = [1, -1]
            
        if len(add_states) == N-1:
            des.event_act.append(add_states[0] + "-" + add_states[1])
            if add_states[0] in des.trans_act:
                des.trans_act[add_states[0]].append([add_states[1],des.event_act[-1]])
            else:
                print("*\nERROR at {0}\n*\n".format(add_states[0]))
                
            des.timed_event[des.event_act[-1]] = [2, -1]
            
            des.event_act.append(add_states[1] + "-" + add_states[0])
            if add_states[1] in des.trans_act:
                des.trans_act[add_states[1]].append([add_states[0],des.event_act[-1]])
            else:
                print("*\nERROR at {0}\n*\n".format(add_states[1]))
                
            des.timed_event[des.event_act[-1]] = [2, -1]
            
        else:
            print("*\nERROR\n*\n")

    """


    des.istate_act = des.s_act[0]
    des.fin_state_act = des.s_act[-1]
    for i in range(len(des.s_act)):
        des.ap_act.append("{}".format(i))
        des.label_act[des.s_act[i]] = ["{}".format(i)]
    
    """
    上位TDESとの単位時間のずれ
    0以上1以下の数になる
    """
    des.time_ratio = 0.75
    return des