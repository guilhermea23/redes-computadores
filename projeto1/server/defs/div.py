def div(args:list[int]) -> int:
    res = args[0]
    for i in args[1:]:
        res = res // i
    return res