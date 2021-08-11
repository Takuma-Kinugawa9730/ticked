
import class_des
        
def get_DES():

    des = class_des.DES()
    
    des.name = "3_1"
    des.have_refined_state = -1
    des.s_act = ['0', '1', '2', '3']

    des.event_act =['01', '10', "11", '12', '20', '22', '23', '02', 'finish']

    des.trans_act={
            des.s_act[0]:[[des.s_act[1],des.event_act[0]],
                          [des.s_act[2],des.event_act[7]]],
            des.s_act[1]:[[des.s_act[0],des.event_act[1]],
                          [des.s_act[2],des.event_act[3]]],
            des.s_act[2]:[[des.s_act[0],des.event_act[4]],
                          [des.s_act[3],des.event_act[6]]],
            
            des.s_act[3]:[[des.s_act[3],des.event_act[-1]]]
            }


    des.istate_act = des.s_act[0]
    des.fin_state_act = des.s_act[-1]
    des.ap_act = ["3_1_1", "3_1_2", "3_1_3", "3_1_4", "3_1_5"] 
    des.label_act = {   
                des.s_act[0]:[des.ap_act[1]],
                des.s_act[1]:[des.ap_act[2], des.ap_act[0]],
                des.s_act[2]:[des.ap_act[3], des.ap_act[0]],
                
                des.s_act[3]:[des.ap_act[4]]
        }
    
    des.timed_event = {    
                des.event_act[0]:[0,-1],
                des.event_act[1]:[1,-1],
                des.event_act[2]:[1, 2],
                des.event_act[3]:[1,-1],
                des.event_act[4]:[1,-1],
                des.event_act[5]:[1,2],
                des.event_act[6]:[0, -1],
                des.event_act[7]:[0,-1],
                des.event_act[-1]:[0,0]
                    }
    
    
    """
    上位TDESとの単位時間のずれ
    0以上1以下の数になる
    """
    des.time_ratio = 0.75
    return des