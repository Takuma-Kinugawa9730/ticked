
"""
    原子命題　0　は、Trueを表す
"""

HORIZON = 15

def get_hard_constraint():
    
    
    hard_constraint = ['d', 'F', [0, HORIZON]]

    return hard_constraint

def get_soft_constraint():

    soft_constraint = [(['c', 'F', [0, HORIZON]], 2), 
                       (['d', 'F', [0, 5]], 3),
                       (['b', '!', 'c', 'U', [0, HORIZON]], 2)]
    
    return soft_constraint
