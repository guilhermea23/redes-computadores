def sub(args:list[int]) -> int:
    res = args[0]
    for i in args[1:]:
        res -= i
    return res