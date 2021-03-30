from cv2 import cv2 as cv

def delete_gasuss_noise(image):
    '''
        去除高斯噪声
    '''
    out = cv.GaussianBlur(image,(3,3),1)
    return out

def connect(image):
    '''
        断点连接
    '''
    h,w = image.shape
    for i in range(2,h-2):
        for j in range(2,w-2):
            #如果中心点位置为255 考虑八邻域
            if image[i,j] == 255:
                num = 0
                for k in range(-1,2):
                    for l in range(-1,2):
                        if k != 0 or l != 0 and image[i+k,i+l] == 255:
                            num += 1
                #如果八邻域中只有一个点是255，说明该中心点为端点，则考虑其他领域
                if num == 1:
                    for k in range(-2,3):
                        for l in range(-2,3):
                            #非八邻域
                            if not(k<2 and k>-2 and l<2 and l>-2) and image[i+k,i+l] == 255:
                                image[i+k,i+l] = 255
 
    return image

def open_close(image):
    '''
        形态学开闭操作
    '''
    out = cv.morphologyEx(image,cv.MORPH_OPEN,(10,200))
    return out