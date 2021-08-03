
"""
    原子命題　0　は、Trueを表す
"""

HORIZON = 10

def get_hard_constraint():
    
    
    hard_constraint = ['FIN', 'F', [0, HORIZON],
                      ]

    return hard_constraint

def get_soft_constraint():

    soft_constraint = [(['c', 'F', [0,HORIZON]], 3), 
                       (['b', 'G', [0,2], 'F', [0,HORIZON]], 2),
                       (['c', 'G', [0,3], 'F', [0,HORIZON]], 1), 
                       (['c', '!', 'b', 'U', [0, HORIZON]], 2)]
    
    return soft_constraint