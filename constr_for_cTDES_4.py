
"""
    原子命題　0　は、Trueを表す
"""

HORIZON = 20

def get_hard_constraint():
    
    
    hard_constraint = ['FIN', 'F', [0, HORIZON]]

    return hard_constraint

def get_soft_constraint():

    soft_constraint = [(['i', '!', 'G', [0, HORIZON]], 3), 
                       (['d', 'F', [0, HORIZON]], 1), 
                       (['e', 'F', [0, HORIZON]], 1),
                       (['e', '!', 'd', 'U', [0, HORIZON]], 2)]
    
    return soft_constraint
