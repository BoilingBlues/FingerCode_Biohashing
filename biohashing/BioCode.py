from . import RandomMatrix
import numpy as np

def BioCode(seed,V):
    result = []
    R = RandomMatrix.RandomMatrix(seed,80,80)
    for i in V:
        temp = []
        for j in range(len(R[0])):
            re = np.dot(R[:,j],i)
            if re>0:
                re = 1
            else:
                re = 0
            temp.append(re)
        result.append(temp)
    return result