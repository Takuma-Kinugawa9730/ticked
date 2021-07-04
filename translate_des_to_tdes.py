from collections import defaultdict

import copy
import itertools
import time
import class_tdes


MaxEvent = 5


def refine(TDES, DES):

    OpenList = []
    ClosedList = []
    EventCheck = []
    index_istate = TDES.s.index(TDES.istate)

    OpenList.append('{}'.format(index_istate))
    #print(OpenList)
    #print("start to search reachablity of TDES\n")
    start = time.time()
    while(1):
        if len(OpenList) == 0:

            break

        now = OpenList[0]
        OpenList.pop(0)
        ClosedList.append(now)
        
        for i in range(len(TDES.delta[now])):
            
            if TDES.delta[now][i][0] not in ClosedList:
                OpenList.append(TDES.delta[now][i][0])

            if TDES.delta[now][i][1] not in EventCheck:
                EventCheck.append(TDES.delta[now][i][1])

    #t = time.time() - start
    #print('finish refining, time={}'.format(t))

    #ClosedList.sort()

    list1 = list(range(len(TDES.s)))
    list1.reverse()
    for i in list1:

        if str(i) not in ClosedList:

            TDES.s.pop(i)
            
    TDES.delta = defaultdict(list)
    TDES.delta = get_transition_func_of_tdes(TDES.s, DES.trans_act, DES.timed_event)

    #print('size of s={}'.format(len( TDES.s)))
    #print('size of trans={}'.format(len( TDES.delta)))

    #print(TDES.event)
    list2 = list(range(len(TDES.event)))
    list2.reverse()
    for j in list2:

        if TDES.event[j] not in EventCheck:
            TDES.event.pop(j)

    return TDES




def get_state_of_tdes(s_act, trans_act, timed_event, initial_state_act):
    
    s_for_tdes=[]
    initial_s = [initial_state_act]

    for i in range(len(s_act)):
        
        s = s_act[i]
        
        trans_from_s = copy.copy(trans_act[s])
        flag4istate=0
        if s == initial_s[0]:
            flag4istate = 1
            
        T_sigma = []
        for j in range( len(trans_from_s) ):
            list1 = trans_from_s[j]
            
            if timed_event[list1[1]][1] == -1:    #if remote event
                T_sigma.append(list(range(timed_event[list1[1]][0]+1)))
                
                if flag4istate==1:
                    initial_s.append(timed_event[list1[1]][0])

            elif timed_event[list1[1]][1] != -1:    #if prospective event
                T_sigma.append(list(range(timed_event[list1[1]][1]+1)))

                if flag4istate==1:
                    initial_s.append(timed_event[list1[1]][1])

        if len(T_sigma)==1:
            timer0 = T_sigma[0]

            for t in timer0:
                list_new=[]
                list_new.append(s)
                list_new.append(timer0[t])
                s_for_tdes.append(list_new)
                
        elif len(T_sigma)==2:
            timer0 = T_sigma[0]    
            timer1 = T_sigma[1]    
            product = list(itertools.product(timer0,timer1))
            
            for k in range(len(product)):
                timer = list(product[k])
                list_new=[]
                list_new.append(s)
                list_new.extend(timer)
                s_for_tdes.append(list_new)
                
        elif len(T_sigma)==3:
            timer0 = T_sigma[0]    
            timer1 = T_sigma[1]    
            timer2 = T_sigma[2]    
            product = list(itertools.product(timer0,timer1,timer2))
            
            for k in range(len(product)):
                timer = list(product[k])
                list_new=[]
                list_new.append(s)
                list_new.extend(timer)
                s_for_tdes.append(list_new)
                
        elif len(T_sigma)==4:
            timer0 = T_sigma[0]    
            timer1 = T_sigma[1]    
            timer2 = T_sigma[2]    
            timer3 = T_sigma[3]    
            product = list(itertools.product(timer0,timer1,timer2,timer3))
            
            for k in range(len(product)):
                timer = list(product[k])
                list_new=[]
                list_new.append(s)
                list_new.extend(timer)
                s_for_tdes.append(list_new)
                
        elif len(T_sigma)==5:
            timer0 = T_sigma[0]    
            timer1 = T_sigma[1]    
            timer2 = T_sigma[2]    
            timer3 = T_sigma[3]    
            timer4 = T_sigma[4]    
            product = list(itertools.product(timer0,timer1,timer2,timer3,timer4))
            
            for k in range(len(product)):
                timer = list(product[k])
                list_new=[]
                list_new.append(s)
                list_new.extend(timer)
                s_for_tdes.append(list_new)
                #print('s_with_clock <-{}'.format(s[-1]))
        
        else:
            print("error. there are too many event occurred in a state")

    if initial_s not in s_for_tdes:
        print('\nistate:{}'.format(initial_s))
        print("there is no istate")
    
    return (s_for_tdes, initial_s)

def get_transition_func_of_tdes(s, trans_act, timed_event):
    
    delta = defaultdict(list)
    
    #print('trans_act2trans')
    for i in range(len(s)):
        occurable_event_at_s = []
        
        s1 = copy.copy(s[i])
        
        s_act = s1[0]
        s_clock = []
        
        for j in range(1,len(s1)):
            s_clock.append(s1[j])
        trans_from_s = copy.deepcopy(trans_act[ s1[0] ])

        # transition s.t., s[0] -> trans_from_s[j][0] by trans[j][1] (in G_act)
        for j in range( len(trans_from_s) ):
            
            occurable_event_at_s.append(trans_from_s[j][1])


        # add the transition by tick
        next_clock = copy.copy(s_clock)
        flag = 0
        for j in range( len(next_clock) ):
            
            if s_clock[j] == 0:
                u_sigma = timed_event[occurable_event_at_s[j]][1]
                # if prospective event
                if u_sigma == -1:# if remote event
                    next_clock[j] = 0
                else:            
                    
                    flag = 1
                    break
            else:
                next_clock[j] = next_clock[j]-1

        if flag == 0:
            destination_tick = [s_act]
            destination_tick.extend(next_clock)
            str_destination_tick = '{}'.format(s.index(destination_tick))
            delta['{}'.format(i)].append([str_destination_tick,'tick'])

        else:
            pass



        # add transitons by other than tick
        for j in range( len(trans_from_s) ):
            # list1 mean list of [destination state from j, event] in G_act
            list1 = copy.deepcopy(trans_act[trans_from_s[j][0]])

            index1 = occurable_event_at_s.index(trans_from_s[j][1])
            clock = s_clock[index1]
            if timed_event[trans_from_s[j][1]][1] == -1: #remote event
                if clock != 0:
                    continue

            else:  #prospective event

                if (0 <= clock) and (clock <= timed_event[trans_from_s[j][1]][1]-timed_event[trans_from_s[j][1]][0]):
                    pass
                else:
                    continue

            #print('trans_from_s[j][0]={0},\nlist1={1}'.format(trans_from_s[j][0],list1))
            # decide timer of j
            destinate_clock = []
            for k in range( len(list1) ):
                
                #print('{}'.format(list1[k][1]))
                # if there is a share event in s_i and s_j (in G_act)
                if list1[k][1] in occurable_event_at_s:
                    index = occurable_event_at_s.index(list1[k][1])
                    destinate_clock.append(s_clock[index])

                else:
                    # list[k][1] (occurable event at j) is remote event
                    if timed_event[list1[k][1]][1] == -1:
                        destinate_clock.append(timed_event[list1[k][1]][0])

                    # list[k][1] (occurable event at j) is prospective event
                    else :
                        destinate_clock.append(timed_event[list1[k][1]][1])

            destination = copy.copy([trans_from_s[j][0]])
            destination.extend(destinate_clock)
            #print('')
            str_destination = '{}'.format(s.index(destination))
            str_event = '{}'.format(trans_from_s[j][1])
            delta['{}'.format(i)].append([str_destination,str_event])


    return delta





def get_TDES(DES):
    
    TDES = class_tdes.TDES()
    TDES.name = DES.name
    (TDES.s, TDES.istate) = get_state_of_tdes(DES.s_act, DES.trans_act, DES.timed_event, DES.istate_act)
    #print(TDES.event)
    #print(DES.event_act)
    TDES.event = DES.event_act + ['tick']    
    #print(TDES.event)
    TDES.delta = get_transition_func_of_tdes(TDES.s, DES.trans_act, DES.timed_event)
    TDES = refine(TDES, DES)
    TDES.ap = copy.copy(DES.ap_act)
    TDES.label = copy.copy(DES.label_act)
   
    TDES.time_ratio = DES.time_ratio #pTDESは-1の値を持つ
    return TDES
