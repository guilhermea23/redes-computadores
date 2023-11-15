def multi(*x:float)->float:
    res = 1
    for args in x:
        res*=args
    return res