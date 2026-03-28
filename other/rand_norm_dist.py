import math
import random
import numpy as np
import matplotlib.pyplot as plt
from decimal import Decimal

# Trying to find functions that transform random data to almost normal distribution
# #(not precise because it's just for a game)


def a(x, p):
    return 1 - (1 - x ** p) ** (1 / p)


# other function
def trans(x, p=1.5):
    if x < 0.5:
        return (-a(-2 * x + 1, p) + 1) / 2
    else:
        return (a(2 * x - 1, p) + 1) / 2


# other function
def trans2(x, p=1.4):
    if x < 0.5:
        return (1 - (1 - 2 * x) ** p) / 2
    else:
        return (1 + (2 * x - 1) ** p) / 2


# best function
def transform(x, p=0.1):
    '''
    Transforms uniform random data to an almost normal distribution.

    x ranges from [0, 1].

    if p is in range [0, 1], it will "push" the data towards 0.5 (similar to normal distribution with average on 0.5).

    if p is higher than 1, it will "push" the data away from 0.5.
    '''

    if x < 0.5:
        return ((2 * x) ** p) / 2
    else:
        return -((2 - 2 * x) ** p) / 2 + 1


NUM = 1000000

x = np.linspace(0, 1, 10000)
y1 = np.random.random_sample(NUM)
y2 = np.vectorize(lambda x: transform(x))(y1)
z = np.vectorize(lambda x: transform(x))(x)
# y1.sort()
# y2.sort()

h1 = np.histogram(y1, bins=np.arange(NUM) / NUM)
h2 = np.histogram(y2, bins=np.arange(NUM) / NUM)


# Plot the data
#plt.plot(x, z, label='linear transformed by function')
#plt.plot(x, y1, label='random sample')
#plt.plot(x, y2, label='random sample transformed')
#plt.plot(h1[1], label='histogram')
plt.plot(np.arange(NUM - 1) / NUM, h2[0], label='histogram transformed')

# Add a legend
plt.legend()

# Show the plot
plt.show()
