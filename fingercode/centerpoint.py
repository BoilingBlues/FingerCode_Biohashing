from cv2 import cv2 as cv
import numpy as np
from . import walking

width = 50

# get the reference frame
def GetCentralPoint(img):
    '''
        指纹奇异点提取
    '''
    rows, cols = img.shape[:2]
    result = walking.walking(img)
    if min(result['core'].shape)!=0:
        row,col = int(result['core'][0][0]),int(result['core'][0][1])
        if row != 0:
            if (col + width < cols) & (row + width < rows) & (col - width > 0) & (row - width > 0):
                print("success")
                return row,col
            else:
                row = 0
                col = 0
                print("failed")
    return 0,0

# copy the reference frame
def GetCoreIMG(img, core_x, core_y):
    '''
        获得切分扇形区域图像
    '''
    radius = width

    core_img = img[core_y-radius:core_y+radius, core_x-radius:core_x+radius]

    return core_img
