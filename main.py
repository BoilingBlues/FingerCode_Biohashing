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



if __name__=="__main__":
    app = multiple_page.Application()
    app.mainloop()