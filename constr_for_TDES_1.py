
"""
    原子命題　0　は、Trueを表す
"""

HORIZON = 15

def get_hard_constraint():
    
    
    hard_constraint = ['1_5', 'F', [0, HORIZON],
                      ]

    return hard_constraint

def get_soft_constraint():

    soft_constraint = [(['1_4', 'F', [0,HORIZON]], 3), 
                       (['1_3', 'G', [0,2], 'F', [0,HORIZON]], 2),
                       (['1_4', 'G', [0,3], 'F', [0,HORIZON]], 1), 
                       (['1_4', '!', '1_3', 'U', [0, HORIZON]], 2)]
    
    return soft_constraint