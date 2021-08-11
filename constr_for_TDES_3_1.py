
"""
    原子命題　0　は、Trueを表す
"""

HORIZON = 20

def get_hard_constraint():
    
    
    hard_constraint = ['3_1_5', 'F', [0, HORIZON]]

    return hard_constraint

def get_soft_constraint():

    soft_constraint = [(['3_1_1', 'G', [0, 4], 'F', [0, HORIZON]], 2), 
                       (['3_1_4', '3_1_2', 'F', [0, 4], '&', 'F', [0, HORIZON]], 3), 
                       (['3_1_3', 'F', [0, HORIZON]], 2),
                       (['3_1_2', '!', 'G', [3, 6]], 3)]
    
    return soft_constraint
