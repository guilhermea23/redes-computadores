def add_int(*x:int) -> int:
    res = 0
    for var in x:
        res+=x
    return res

def add_float(*x:float)->float:
    res = 0
    for var in x:
        res+=x
    return res