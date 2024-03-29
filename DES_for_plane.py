
import class_des
        
def get_DES():

    des = class_des.DES()
    
    des.name = "c_4"
    des.s_act = ['0', '1', '2', '3', '4', '5']

    des.event_act =['01', '03', '04', '12', '25', '34', '35', '40', '45', 'finish']

    des.trans_act={
            des.s_act[0]:[[des.s_act[1],des.event_act[0]],
                          [des.s_act[3],des.event_act[1]],
                          [des.s_act[4],des.event_act[2]]],
            des.s_act[1]:[[des.s_act[2],des.event_act[3]]],
            des.s_act[2]:[[des.s_act[5],des.event_act[4]]],
            
            des.s_act[3]:[[des.s_act[4],des.event_act[5]],
                          [des.s_act[5],des.event_act[6]]],
            des.s_act[4]:[[des.s_act[0],des.event_act[7]],
                          [des.s_act[5],des.event_act[8]]],
            des.s_act[5]:[[des.s_act[5],des.event_act[-1]]]
            }


    des.istate_act = des.s_act[0]
    des.fin_state_act = des.s_act[-1]
    des.ap_act = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'FIN'] 
    des.label_act = {   
                des.s_act[0]:[des.ap_act[0]],
                des.s_act[1]:[des.ap_act[1], des.ap_act[8]],
                des.s_act[2]:[des.ap_act[2], des.ap_act[8]],
                
                des.s_act[3]:[des.ap_act[3]],
                des.s_act[4]:[des.ap_act[4]],
                des.s_act[5]:[des.ap_act[-1]]
        }
    
    des.timed_event = {    
                des.event_act[0]:[0,-1],
                des.event_act[1]:[2,-1],
                des.event_act[2]:[2, 3],
                des.event_act[3]:[1,-1],
                des.event_act[4]:[1,-1],
                des.event_act[5]:[2,2],
                des.event_act[6]:[2,-1],
                des.event_act[7]:[1,-1],
                des.event_act[8]:[3,-1],
                des.event_act[9]:[0,0]
                    }
    
    """
    タスクを終了したことを表す状態des.fin_state_actにおける挙動を追加（上書き）
    """
    des.trans_act[des.fin_state_act].append([des.fin_state_act, des.event_act[-1]])
    des.label_act[des.fin_state_act].append(des.ap_act[-1])
    des.timed_event[des.event_act[-1]] = [0,0]
    
    """
    上位TDESとの単位時間のずれ
    0以上1以下の数になる
    """
    des.time_ratio = 0.75
    return des