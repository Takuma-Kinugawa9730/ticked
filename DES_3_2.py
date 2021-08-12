
import class_des
        
def get_DES():

    des = class_des.DES()
    
    des.name = "3_2"
    des.have_refined_state = -1
    des.s_act = ['0', '1', '2', '3', '4']

    des.event_act =['01', '02', '13', '21', '32', '34', 'finish']

    des.trans_act={
            des.s_act[0]:[[des.s_act[1],des.event_act[0]],
                          [des.s_act[2],des.event_act[1]]],
            des.s_act[1]:[[des.s_act[3],des.event_act[2]]],
            des.s_act[2]:[[des.s_act[1],des.event_act[3]]],
            des.s_act[3]:[[des.s_act[2],des.event_act[4]],
                          [des.s_act[4],des.event_act[5]]],
            des.s_act[4]:[[des.s_act[4],des.event_act[-1]]]
            }


    des.istate_act = des.s_act[0]
    des.fin_state_act = des.s_act[-1]
    des.ap_act = ["3_2_1", "3_2_2", "3_2_3", "3_2_4", "3_2_5"] 
    des.label_act = {   
                des.s_act[0]:[des.ap_act[0]],
                des.s_act[1]:[des.ap_act[1]],
                des.s_act[2]:[des.ap_act[2]],
                des.s_act[3]:[des.ap_act[3]],
                des.s_act[4]:[des.ap_act[4]]

        }
    
    des.timed_event = {    
                des.event_act[0]:[1,-1],
                des.event_act[1]:[1,-1],
                des.event_act[2]:[0,-1],
                des.event_act[3]:[3,-1],
                des.event_act[4]:[1,-1],
                des.event_act[5]:[1, -1],
                des.event_act[6]:[0,0]
                    }
    
    
    
    """
    上位TDESとの単位時間のずれ
    0以上1以下の数になる
    """
    des.time_ratio = 0.625
    return des