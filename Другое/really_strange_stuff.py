var = 99

def loc():
    var = 0
    
def glob2():
    var = 0
    import really_strange_stuff
    test4.var += 1

glob2()
print(var)
