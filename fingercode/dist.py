import math


def EulerDistance(result1,result2):
    '''
        计算两个指纹模板的欧氏距离
    '''
    distance = 0
    for i in range(len(result1)):
        temp1 = result1[i]
        temp2 = result2[i]
        #逐行比较
        for j in range(len(temp1)):
            #math.pow(x,y)获取x的y次方
            #距离为每个对应位置值差的平方的累加
            distance += math.pow(temp1[j] - temp2[j], 2)

    return distance

def HammingDistance(result1,result2):
    '''
        计算两个指纹模板的汉明距离
    '''
    distance = 0
    for i in range(len(result1)):
        temp1 = result1[i]
        temp2 = result2[i]
        for j in range(len(temp1)):
            distance += bin(temp1[j]^temp2[j]).count('1')
    return distance
