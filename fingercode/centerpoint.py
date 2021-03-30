from cv2 import cv2 as cv
import numpy as np
from . import walking

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
            if (col + 75 < cols) & (row + 75 < rows)&(col-75>0)&(row-75>0):
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
    radius = 75
    # crop the image 80*80
    #core_img = np.zeros((radius, radius, 3), np.uint8)
    core_img = img[core_y-radius:core_y+radius, core_x-radius:core_x+radius]

    return core_img
