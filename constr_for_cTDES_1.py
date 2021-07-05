
"""
    原子命題　0　は、Trueを表す
"""

HORIZON = 10

def get_hard_constraint():
    
    
    hard_constraint = ['FIN', 'F', [0, HORIZON],
                       'c', '!', 'b', 'U', [0, HORIZON]]

    return hard_constraint

def get_soft_constraint():

    soft_constraint = [(['e', 'G', [1,3]], 2)]
    
    return soft_constraint