
import class_des
        
def get_DES():

    des = class_des.DES()
    
    des.name = "c_1"
    des.s_act = [    'a0', 'ab', 'ac',
            'b0', 'bc', 'ba',
            'c0', 'ca', 'cb'    ]

    des.event_act =['move_ab', 'reach_ab', 'move_ac', 'reach_ac', 
            'move_bc', 'reach_bc', 'move_ba', 'reach_ba', 
            'move_ca', 'reach_ca', 'move_cb', 'reach_cb'
            ]

    des.trans_act={
            des.s_act[0]:[[des.s_act[1],des.event_act[0]],
                    [des.s_act[2],des.event_act[2]]],
            des.s_act[1]:[[des.s_act[3],des.event_act[1]]],
            des.s_act[2]:[[des.s_act[6],des.event_act[3]]],
            
            des.s_act[3]:[[des.s_act[4],des.event_act[4]],
                    [des.s_act[5],des.event_act[6]]],
            des.s_act[4]:[[des.s_act[6],des.event_act[5]]],
            des.s_act[5]:[[des.s_act[0],des.event_act[7]]],
            
            des.s_act[6]:[[des.s_act[7],des.event_act[8]],
                    [des.s_act[8],des.event_act[10]]],
            des.s_act[7]:[[des.s_act[0],des.event_act[9]]],
            des.s_act[8]:[[des.s_act[3],des.event_act[11]]] }


    des.istate_act = des.s_act[0]
    des.ap_act = [    'A', 
            'B', 
            'C',                
            'm_ab', 'm_ac', 'm_bc', 'm_ba', 'm_ca', 'm_cb', '1', '2', '3', '5'] 
    des.label_act = {    des.s_act[0]:[des.ap_act[0]],
                des.s_act[1]:[des.ap_act[3]],
                des.s_act[2]:[des.ap_act[4]],
                
                des.s_act[3]:[des.ap_act[1]],
                des.s_act[4]:[des.ap_act[5]],
                des.s_act[5]:[des.ap_act[6]],

                des.s_act[6]:[des.ap_act[2]],
                des.s_act[7]:[des.ap_act[7]],
                des.s_act[8]:[des.ap_act[8]],
                
        }
 
    des.timed_event = {    des.event_act[0]:[1,-1],
                des.event_act[1]:[1,2],
                des.event_act[2]:[1, -1],
                des.event_act[3]:[1,2],
                des.event_act[4]:[1,-1],
                des.event_act[5]:[1,2],
                des.event_act[6]:[1,-1],
                des.event_act[7]:[1,2],
                des.event_act[8]:[1,-1],
                des.event_act[9]:[1,2],
                des.event_act[10]:[1,-1],
                des.event_act[11]:[1,2]
                    }

    
    """
    上位TDESとの単位時間のずれ
    0以上1以下の数になる
    """
    des.time_ratio = 0.25
    return des