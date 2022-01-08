import numpy as np

WIDTH = 600
HEIGHT = 600
dTime = 0.001
GRID_SIZE = 20

def normalize(arr):
    return arr / np.sqrt(np.sum(arr**2))
