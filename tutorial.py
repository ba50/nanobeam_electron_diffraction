import numpy as np
import math
def f(x):
    print(x)
    y = [1]*10000000
    [math.exp(i) for i in y]
def g(x):
    print(x)
    y = np.ones(10000000)
    np.exp(y)

from handythread import foreach
from processing import Pool
from timings import f,g


def fornorm(f,l):
    for i in l:
        f(i)


time fornorm(g,range(100))
time fornorm(f,range(10))
time foreach(g,range(100),threads=2)
time foreach(f,range(10),threads=2)
p = Pool(2)
time p.map(g,range(100))
time p.map(f,range(100))