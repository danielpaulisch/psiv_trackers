import numpy as np


import tracker1


M = np.zeros((4,3))

for i in range(4):
    for J in range(3):
        M[i,J] = J

print(np.where(M == np.min(M))[0],np.where(M == np.min(M))[1] )
print(M)