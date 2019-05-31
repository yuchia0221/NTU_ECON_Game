# import matplotlib
from math import pi, atan, log


def trade_function(d, s):
    return (1.2) * (2 / pi) * atan((d - s) * (1 / 10000)) + 1.2


for i in range(0, 30001, 1000):
    print(i, trade_function(0, i))
