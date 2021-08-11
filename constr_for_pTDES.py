
"""
    原子命題　0　は、Trueを表す
"""

HORIZON = 20

def get_hard_constraint():
    
    
    hard_constraint = ['2', 'F', [0, HORIZON]]

    return hard_constraint

def get_soft_constraint():

    soft_constraint = [(['4', '!', 'G', [5, 8]], 3), 
                       (['1', 'F', [0, HORIZON]], 1), 
                       (['3', 'G', [0, 4], 'F', [0, HORIZON]], 1),
                       (['2', '!', '1', 'U', [0, HORIZON]], 2)]
    
    return soft_constraint
