
"""
    原子命題　0　は、Trueを表す
"""

HORIZON = 20

def get_hard_constraint():
    
    
    hard_constraint = ['3_2_5', 'F', [0, HORIZON]]

    return hard_constraint

def get_soft_constraint():

    soft_constraint = [(['3_2_3', 'G', [0, 5], 'F', [0, HORIZON]], 3), 
                       (['3_2_2', '!', '3_2_3', '!', 'F', [0, HORIZON], '|', 'G', [0, HORIZON]], 2), 
                       (['3_2_3', 'F', [0, HORIZON]], 1),
                       (['3_2_4', '!', 'G', [2, 5]], 2)]
    
    return soft_constraint
