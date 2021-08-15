
"""
    原子命題　0　は、Trueを表す
"""

HORIZON = 30

def get_hard_constraint():
    
    
    hard_constraint = ['1', 'G', [0, 2], 'F', [0, HORIZON], '3', 'G', [0, 3], 'F', [0, HORIZON] , '&', '3', '!', '1', 'U', [0, HORIZON], '&']

    return hard_constraint

def get_soft_constraint():

    soft_constraint = [(['4', '!', 'G', [1, 5]], 2), 
                       (['2', 'G', [0, 2], 'F', [0, HORIZON]], 1), 
                       (['2', 'G', [0, 4], 'F', [0, HORIZON]], 2), 
                       (['3', 'G', [0, 4], 'F', [0, HORIZON]], 3),
                       (['1', '2', '&', 'F', [0, HORIZON]], 1),
                       ]
    
    return soft_constraint
