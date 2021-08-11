
"""
    原子命題　0　は、Trueを表す
"""

HORIZON = 15

def get_hard_constraint():
    
    
    hard_constraint = ['d', 'F', [0, HORIZON]]

    return hard_constraint

def get_soft_constraint():

    soft_constraint = [(['c', 'G', [0, 3], 'F', [0, HORIZON]], 2), 
                       (['c', '!', 'G', [0, 5], 'F', [0, HORIZON]], 2), 
                       (['b', '!', 'b', '!', 'F', [3, HORIZON], '|'], 1)]
    
    return soft_constraint
