from fingercode import fingercode
from fingercode import dist
from biohashing import BioCode
from cv2 import cv2 as cv
import datetime
import os
from GUI import multiple_page
def traverseFingerDB():
    # preTime = datetime.datetime.now()
    # image = cv.imread("/mnt/e/graduation_design/fingerprint_database/DB1_B/101_4.tif",0)
    # #创建窗口并显示图像

    # finger1 = fingercode.fingercode(image)
    # print(datetime.datetime.now()-preTime,"总用时")
    # preTime = datetime.datetime.now()
    # image = cv.imread("/mnt/e/graduation_design/fingerprint_database/DB1_B/101_8.tif",0)
    # #创建窗口并显示图像

    # finger2 = fingercode.fingercode(image)
    # print(datetime.datetime.now()-preTime,"总用时")

    # #print(dist.HammingDistance(finger1,finger2))
    # print(dist.EulerDistance(finger1,finger2))



    path = "/mnt/e/code/github/test/fingercode-master/1/"
    files = os.listdir(path)
    images = [x for x in files]
    finger = []
    for i in images:
        preTime = datetime.datetime.now()
        finger.append(fingercode.fingercode(path+i))
        print(datetime.datetime.now()-preTime,"总用时")
    for i in range(80):
        if finger[i]==None:
            print(images[i],"提取失败")
        else:
            for j in range(i,80):
                if finger[j]==None or i==j:
                    #print(images[j],"提取失败")
                    pass
                else:
                    result = dist.EulerDistance(finger[i],finger[j])
                    # if result<200000:
                    print(images[i],images[j],result)

def extractOne(path):
    finger = fingercode.fingercode(path)
    finger = BioCode.BioCode(123456,finger)
    result = ""
    for i in finger:
        for j in i:
            result += str(j)
    return result
def compare(path1,seed1,path2,seed2):
    finger1 = fingercode.fingercode(path1)
    finger1 = BioCode.BioCode(seed1,finger1)
    result1 = ""
    for i in finger1:
        for j in i:
            result1 += str(j)
    result2 = ""
    finger2 = fingercode.fingercode(path2)
    finger2 = BioCode.BioCode(seed2,finger2)
    for i in finger2:
        for j in i:
            result2 += str(j)
    dist = 0
    result1 = list(result1)
    result2 = list(result2)
    for i in range(len(result1)):
        if result1[i]!=result2[i]:
            dist += 1
    return dist

def traverseFingerDBByBioHashing(seed):
    path = "/mnt/e/code/github/test/fingercode-master/1/"
    files = os.listdir(path)
    images = [x for x in files]
    finger = []
    for i in images:
        preTime = datetime.datetime.now()
        finger.append(fingercode.fingercode(path+i))
        print(datetime.datetime.now()-preTime,"总用时")
    for i in range(80):
        if finger[i]==None:
            print(images[i],"提取失败")
        else:
            for j in range(i,80):
                if finger[j]==None or i==j:
                    #print(images[j],"提取失败")
                    pass
                else:
                    result = dist.HammingDistance(BioCode.BioCode(seed,finger[i]),BioCode.BioCode(seed,finger[j]))
                    if result<145:
                        print(images[i],images[j],result)


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

if __name__=="__main__":
    app = multiple_page.Application()
    app.mainloop()
    #print(compare("/mnt/e/code/github/test/fingercode-master/1/102_1.tif",123451,"/mnt/e/code/github/test/fingercode-master/1/102_3.tif",123451))