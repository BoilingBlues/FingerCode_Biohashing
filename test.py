
import os
from fingercode import fingercode
from fingercode import dist
from biohashing import BioCode
from cv2 import cv2 as cv
from GUI import interactive
import time
import statistics
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

def main():
    tezhengtiqu = []
    tezhengjiami = []
    flag = 0
    while 1:
        if flag==101:
            break
        img = interactive.GetIMG()
        try:
            preTime = time.time()
            finger = fingercode.fingercode(img)
            tezhengtiqu.append(time.time()-preTime)
            preTime = time.time()
            finger = BioCode.BioCode(123456,finger)
            tezhengjiami.append(time.time()-preTime)

            flag += 1
            print("特征提取均值",statistics.mean(tezhengtiqu),"特征加密平均值",statistics.mean(tezhengjiami),flag)
        except:
            print("失败")
    print("特征提取均值",statistics.mean(tezhengtiqu),"特征加密平均值",statistics.mean(tezhengjiami))

def compare():
    preTime = time.time()
    for i in range(640):
        h = 1+1
        b = 1^0
    print(time.time()-preTime)

def biocodeDemo():
    img = interactive.GetIMG()
    finger = fingercode.fingercode(img)
    finger = BioCode.BioCode(123456,finger)
    result = ""
    for i in finger:
        result += str(i)
    print(result)
if __name__ == "__main__":
    biocodeDemo()