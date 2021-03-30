from scipy import linalg
import numpy as np

def RandomMatrix(seed,m,n):
    rd = np.random.RandomState(seed)
    result = rd.randint(0,10,(m,n))
    return Schmidt(result)

def Schmidt(A):
    a = linalg.orth(A)
    return a
if __name__=="__main__":
    pre = RandomMatrix(123,80,8)
    print(pre)
    be = Schmidt(pre)
    print(be)
