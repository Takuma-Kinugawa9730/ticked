
"""
    原子命題　0　は、Trueを表す
"""

HORIZON = 18

def get_hard_constraint():
    
    hard_constraint = ['2_4', 'F', [0, HORIZON]]

    return hard_constraint

def get_soft_constraint():

    soft_constraint = [(['2_3', 'G', [0,4], 'F', [0, HORIZON]], 4), 
                       (['2_1', '!', 'G', [0,4], 'F', [0, HORIZON]], 3)]
    
    return soft_constraint