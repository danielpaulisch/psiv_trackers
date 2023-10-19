import numpy as np


m = np.zeros((2,3))


for i in range(2):
    for j in range(3):
        m[i , j] = i + j
    

p = np.where(m == np.max(m) )
print(m.sum())
print(m)


