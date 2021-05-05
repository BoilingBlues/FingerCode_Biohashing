from . import Sector
from . import Gabor
from . import centerpoint
import numpy as np
import math
from cv2 import cv2 as cv
import datetime
from . import pre
def fingercode_unidirectional(img):
    '''计算fingercode'''
    # divide the sectors
    sectors = Sector.DivideSector(img)


    result = []
    Mean = []
    Variance = []
    for i in range(len(sectors)):
        Mean.append(Sector.cal_mean(sectors[i]))
        Variance.append(cal_standar(sectors[i], Mean[i]))
        temp = round(Variance[i], 0)
        #print temp
        result.append(int(temp))
    return result

def cal_standar(points, mean):
    total = 0
    for i in range(len(points)):
        point = points[i]
        total += abs(point.Gray - mean)
    if len(points) != 0:
        return total / len(points)
    else:
        return 0

def fingercode(img):
    #img = pre.delete_gasuss_noise(img)
    # img = pre.connect(img)
    # img = pre.open_close(img)
    #rows,cols = img.shape[:2]
    core_x,core_y = centerpoint.GetCentralPoint(img)
    print(core_x,core_y)
    if core_x != 0:
        #img = cv.cvtColor(img,cv.COLOR_RGB2GRAY)
        #裁剪区域
        core_img = centerpoint.GetCoreIMG(img,core_x,core_y)


        #划分扇区
        sectors = Sector.DivideSector(core_img)

        #归一化处理
        core_img = Sector.NormalizeIMG(core_img,sectors)


        #对特征区域进行8方向滤波
        result = Gabor.GetGabor(core_img)
        temp = []

        for i in result:
            #提取单方向滤波的指纹特征
            fingercodetemp = fingercode_unidirectional(i)
            temp.append(fingercodetemp)
        # convert tht array to string
        return temp


def draw(image):
    cv.namedWindow("Image")
    #显示图片，窗口自适应图片大小，可以指定多个窗口名称，显示多个图片
    print('图片尺寸：', image.shape)
    print('图片数据：', type(image), image)

    cv.imshow("Image",image)
    #等待键盘事件，如果为0则一直等待
    cv.waitKey(0)
    #释放窗口
    cv.destroyAllWindows()