
"""
    原子命題　0　は、Trueを表す
"""

HORIZON = 25

def get_hard_constraint():
    
    hard_constraint = ['FIN', 'F', [0, HORIZON],
                       'g', '!', 'G', [0, 5],'&']

    return hard_constraint

def get_soft_constraint():

    soft_constraint = [(['g', 'G', [0,3], 'F', [0, HORIZON]], 2), 
                       (['g', 'G', [0,5], 'F', [0, HORIZON]], 4)]
    
    return soft_constraint