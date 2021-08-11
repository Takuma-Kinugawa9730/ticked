
"""
    原子命題　0　は、Trueを表す
"""
HORIZON = 20

def get_hard_constraint():
    
    
    hard_constraint = ['3_6', 'F', [0, HORIZON],
                       '3_5',  '!', 'G', [4, 6],'&']

    return hard_constraint

def get_soft_constraint():

    soft_constraint = [(['3_4', 'F', [0, HORIZON]], 3),
                       (['3_2', 'G', [0, 3], 'F', [0, HORIZON]], 2),
                       (['3_5', "!", '3_4', 'U', [0, 5]], 1)]
    
    return soft_constraint