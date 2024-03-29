
import class_des
        
def get_DES():

    des = class_des.DES()
    
    des.name = "2_1"
    des.have_refined_state = -1
    des.s_act = ['0', '1', '2', '3']

    des.event_act =['01', '12', '21', '22', '23', 'finish']

    des.trans_act={
            des.s_act[0]:[[des.s_act[1],des.event_act[0]]],
            des.s_act[1]:[[des.s_act[2],des.event_act[1]]],
            des.s_act[2]:[[des.s_act[1],des.event_act[2]],
                          [des.s_act[3],des.event_act[4]]],
            
            des.s_act[3]:[[des.s_act[3],des.event_act[-1]]]
            }


    des.istate_act = des.s_act[0]
    des.fin_state_act = des.s_act[-1]
    des.ap_act = ['a', 'b', 'c', 'd'] 
    des.label_act = {   
                des.s_act[0]:[des.ap_act[0]],
                des.s_act[1]:[des.ap_act[1]],
                des.s_act[2]:[des.ap_act[2]],
                
                des.s_act[3]:[des.ap_act[3]]
        }
    
    des.timed_event = {    
                des.event_act[0]:[0,-1],
                des.event_act[1]:[2,-1],
                des.event_act[2]:[0, -1],
                des.event_act[3]:[1,2],
                des.event_act[4]:[2,-1],
                des.event_act[5]:[0,0]
                    }
  
    """
    上位TDESとの単位時間のずれ
    0以上1以下の数になる
    """
    des.time_ratio = 0.666
    return des