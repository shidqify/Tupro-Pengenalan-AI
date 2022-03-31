import numpy as np

h = lambda x, y: ((np.cos(x) + np.sin(y))**2) / x**2 + y**2

def fitness(x, y):
    return 1/(h(x, y) + 1)

def decode(kromosom, limit):
    kali, pembagi