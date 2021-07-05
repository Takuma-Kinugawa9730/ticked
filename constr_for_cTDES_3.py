
"""
    原子命題　0　は、Trueを表す
"""
HORIZON = 20

def get_hard_constraint():
    
    
    hard_constraint = ['FIN', 'F', [0, HORIZON],
                       'i', 'F', [0, HORIZON],'&']

    return hard_constraint

def get_soft_constraint():

    soft_constraint = [(['b', 'F', [0, HORIZON]], 2), (['i', 'F', [3, 5]], 2)]
    
    return soft_constraint