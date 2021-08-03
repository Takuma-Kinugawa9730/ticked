
"""
    原子命題　0　は、Trueを表す
"""
HORIZON = 20

def get_hard_constraint():
    
    
    hard_constraint = ['FIN', 'F', [0, HORIZON],
                       'f', 'F', [0, HORIZON],'&']

    return hard_constraint

def get_soft_constraint():

    soft_constraint = [(['f', 'F', [0, 4], 'FIN', 'F', [0, 4], '|', 'G', [0, HORIZON]], 2), (['b', 'F', [0, HORIZON]], 1)]
    
    return soft_constraint