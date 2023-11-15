def sub(*x:float) -> float:
    res = 0
    for args in x:
        res-=args
    return res