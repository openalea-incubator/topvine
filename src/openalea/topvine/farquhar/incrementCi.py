def incrementCi(Ca, A, gs, gb):
    '''    increment Ci Value
    '''
    Ci_new=Ca-A*(1.6/gs+1.37/gb)
    return Ci_new
