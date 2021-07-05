
"""
    原子命題　0　は、Trueを表す
"""

HORIZON = 20

def get_hard_constraint():
    
    
    hard_constraint = ['FIN', 'F', [0, HORIZON]]

    return hard_constraint

def get_soft_constraint():

    soft_constraint = [(['h', '!', 'd', 'U', [0, HORIZON]], 2), 
                       (['e', 'F', [0, HORIZON]], 1), 
                       (['h', 'F', [0, HORIZON]], 1),
                       (['FIN', 'F', [0,8]], 2)]
    
    return soft_constraint
