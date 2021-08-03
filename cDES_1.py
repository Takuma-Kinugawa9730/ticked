
import class_des
        
def get_DES():

    des = class_des.DES()
    
    des.name = "c_1"
    des.s_act = ['0', '1', '2', '3']

    des.event_act =['01', '02', '12', '13', '23', 'finish']

    des.trans_act={
            des.s_act[0]:[[des.s_act[1],des.event_act[0]],
                          [des.s_act[2],des.event_act[1]]],
            des.s_act[1]:[[des.s_act[2],des.event_act[2]],
                          [des.s_act[3],des.event_act[3]]],
            des.s_act[2]:[[des.s_act[3],des.event_act[4]]],
            
            des.s_act[3]:[[des.s_act[3],des.event_act[-1]]]
            }


    des.istate_act = des.s_act[0]
    des.fin_state_act = des.s_act[-1]
    des.ap_act = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'FIN'] 
    des.label_act = {   
                des.s_act[0]:[des.ap_act[0]],
                des.s_act[1]:[des.ap_act[1], des.ap_act[4]],
                des.s_act[2]:[des.ap_act[2], des.ap_act[4]],
                
                des.s_act[3]:[des.ap_act[-1]]
        }
    
    des.timed_event = {    
                des.event_act[0]:[1,-1],
                des.event_act[1]:[1,2],
                des.event_act[2]:[1, -1],
                des.event_act[3]:[1,4],
                des.event_act[4]:[1,4],
                des.event_act[5]:[0,0]
                    }
    
    """
    タスクを終了したことを表す状態des.fin_state_actにおける挙動を追加（上書き）
    もし忘れていたときのために
    """
    des.trans_act[des.fin_state_act].append([des.fin_state_act, des.event_act[-1]])
    des.label_act[des.fin_state_act].append(des.ap_act[-1])
    des.timed_event[des.event_act[-1]] = [0,0]
    
    """
    上位TDESとの単位時間のずれ
    0以上1以下の数になる
    """
    des.time_ratio = 0.5
    return des