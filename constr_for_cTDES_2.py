
"""
    原子命題　0　は、Trueを表す
"""

HORIZON = 15

def get_hard_constraint():
    
    hard_constraint = ['FIN', 'F', [0, HORIZON],
                       'c', '!', 'G', [0, HORIZON],'&']

    return hard_constraint

def get_soft_constraint():

    soft_constraint = [(['g', 'G', [0,2], 'F', [0, HORIZON]], 2), (['a', '!', 'G', [0, HORIZON]], 3)]
    
    return soft_constraint