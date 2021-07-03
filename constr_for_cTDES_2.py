
"""
    原子命題　0　は、Trueを表す
"""

HORIZON = 10

def get_hard_constraint():
    
    
    hard_constraint = ['0', '1', 'U', [2,4], #== F_[M[2,4], M[2,4]+2] '1'
                       '2','&']

    return hard_constraint

def get_soft_constraint():

    soft_constraint = [(['0', '2', '!', 'U', [1,2], '!'], 2), # == G_[M[2,4], M[2,4]+2] '2'
                       (['3'], 3)]
    
    return soft_constraint