x = [5, 10, 15, 20, 25]
p = 1./5
def f(x):
    pass

def mean(p,x):
    return sum([p*y for y in x])


def variance(p,x):
    return sum([(int((y-mean(p,x)))**2) * (p) for y in x])


print("mean {0}".format(mean(p, x)))
print("variance {0}".format(variance(p,x)))
