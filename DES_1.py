
import class_des
        
def get_DES():

    des = class_des.DES()
    
    des.name = "1"
    des.have_refined_state = 0
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
    des.ap_act = ['1_1', '1_2', '1_3', '1_4', '1_5'] 
    des.AP_R = ["1_1"]
    des.label_act = {   
                des.s_act[0]:[des.ap_act[1]],
                des.s_act[1]:[des.ap_act[2], des.ap_act[0]],
                des.s_act[2]:[des.ap_act[3], des.ap_act[0]],
                
                des.s_act[3]:[des.ap_act[-1]]
        }
    
    des.timed_event = {    
                des.event_act[0]:[1,-1],
                des.event_act[1]:[2,-1],
                des.event_act[2]:[3, -1],
                des.event_act[3]:[1,4],
                des.event_act[4]:[1,4],
                des.event_act[5]:[0,0]
                    }
    
    
    """
    上位TDESとの単位時間のずれ
    0以上1以下の数になる
    """
    des.time_ratio = 0.8
    return des