
import class_des
        
def get_DES():

    des = class_des.DES()
    
    des.name = "2"
    des.have_refined_state = 0
    des.s_act = ['0', '1', '2', '3']

    des.event_act =['01', '10', '12', '13', '20', '23', 'finish']

    des.trans_act={
            des.s_act[0]:[[des.s_act[1],des.event_act[0]]],
            des.s_act[1]:[[des.s_act[0],des.event_act[1]],
                          [des.s_act[2],des.event_act[2]],
                          [des.s_act[3],des.event_act[3]]],
            des.s_act[2]:[[des.s_act[0],des.event_act[4]],
                          [des.s_act[3],des.event_act[5]]],
            
            des.s_act[3]:[[des.s_act[3],des.event_act[-1]]]
            }


    des.istate_act = des.s_act[0]
    des.fin_state_act = des.s_act[-1]
    des.ap_act = ['2_1', '2_2', '2_3', '2_4'] 
    des.AP_R = ["2_1"]
    des.label_act = {   
                des.s_act[0]:[des.ap_act[1]],
                des.s_act[1]:[des.ap_act[0]],
                des.s_act[2]:[des.ap_act[2]],
                
                des.s_act[3]:[des.ap_act[3]]
        }
    
    des.timed_event = {    
                des.event_act[0]:[0,-1],
                des.event_act[1]:[0,-1],
                des.event_act[2]:[2, -1],
                des.event_act[3]:[2,-1],
                des.event_act[4]:[0,-1],
                des.event_act[5]:[3,5],
                des.event_act[6]:[0,0]
                    }
    
   
    """
    上位TDESとの単位時間のずれ
    0以上1以下の数になる
    """
    des.time_ratio = 0.7
    return des