from . import RandomMatrix
import numpy as np

SetpSize = 5

def BioCode(seed,V):
    R = RandomMatrix.RandomMatrix(seed,80,80)
    m = Mapping(R,V)
    return Threshold(m)
def Mapping(R,V):
    """
    计算指纹特征向量到伪随机矩阵的映射
    """
    result = []

    for i in V:
        for j in range(len(R[0])):
            re = np.dot(R[:,j],i)
            result.append(re)

    return result

def Threshold(m):
    size = len(m)
    result = []
    for i in range(size):
        sums = 0
        for j in range(SetpSize):
            sums = sums + m[(j+i)%size]
        if m[i]<(sums/SetpSize):
            result.append(0)
        else:
            result.append(1)
    return result