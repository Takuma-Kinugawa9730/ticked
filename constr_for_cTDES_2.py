
"""
    原子命題　0　は、Trueを表す
"""

HORIZON = 5

def get_hard_constraint():
    
    hard_constraint = ['A']

    return hard_constraint

def get_soft_constraint():

    soft_constraint = [(['A', 'G', [1,2]], 2), (['A'], 3)]
    
    return soft_constraint