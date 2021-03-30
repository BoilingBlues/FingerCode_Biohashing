# _*_ coding:utf-8 _*_



import math


class Point:

    # param: X: the pixel x, Y: the pixel y, Gray: the pixel gray value
    def __init__(self, x, y, gray):
        self.X = x
        self.Y = y
        self.Gray = gray
        self.Normal_value = None


# calculate the number of sector's point
def cal_num(points):
    return len(points)


# calculate the mean of sector's points gray value
def cal_mean(points):
    total = 0
    num = cal_num(points)
    for i in range(len(points)):
        point = points[i]
        total += point.Gray
    return total / num



# calculate the variance of the sector's points
def cal_variance(points, mean):
    total = 0
    for i in range(len(points)):
        point = points[i]
        total += math.pow(point.Gray - mean, 2)
    return total / (len(points)-1)


def DivideSector_PRE():
    '''划分扇区'''
    #计算图像的中间点
    rows, cols = 150,150
    k = 16
    b = 10
    T = []
    angle = []
    core_x = cols / 2
    core_y = rows / 2
    for i in range(81):
        T.append(int(i / k))
        angle.append((i % k) * (2 * 180.0 / k))

    sectors = []


    for i in range(80):
        x = 1
        y = 1
        sector = []
        #遍历图像中的每一个点
        for x in range(cols):
            #print x
            for y in range(rows):
                x0 = x - core_x
                y0 = y - core_y
                r = math.sqrt(pow(x0, 2) + pow(y0, 2))
                #print r
                if x0 == 0.0:
                    if y0 > 0:
                        point_angle = 270.0
                    else:
                        point_angle = 90.0

                if y0 == 0.0:
                    if x0 > 0:
                        point_angle = 0.0
                    else:
                        point_angle = 180.0
                # in 1 district
                if(y0 < 0.0)&(x0 > 0.0):
                    point_angle = abs(math.degrees(math.atan(y0 / x0)))
                # in 2 district
                if(y0 < 0.0)&(x0 < 0.0):
                    point_angle = abs(math.degrees(math.atan(x0 / y0))) + 90.0
                # in 3 district
                if(y0 > 0.0)&(x0 < 0.0):
                    point_angle = abs(math.degrees(math.atan(y0 / x0))) + 180.0
                # in 4 district
                if (y0 > 0.0)&(x0 > 0.0):
                    point_angle = abs(math.degrees(math.atan(x0 / y0))) + 270.0
                if (point_angle <= 337.5)&(b * (T[i] + 1) <= r)&(b * (T[i] + 2) > r)&(angle[i] <= point_angle)&(angle[i+1] > point_angle):
                    point = (y,x)
                    sector.append(point)
                if (point_angle > 337.5)&(b * (T[i] + 1) <= r)&(b * (T[i] + 2) > r)&(angle[i] <= point_angle)&(360.0 > point_angle):
                    point = (y,x)
                    sector.append(point)
        sectors.append(sector)

    return sectors



sectors = DivideSector_PRE()
def DivideSector_ONCE(img):
    '''划分扇区'''
    k = 16
    b = 10
    T = []
    angle = []
    rows, cols = img.shape[:2]
    core_x = cols / 2
    core_y = rows / 2
    for i in range(81):
        T.append(int(i / k))
        angle.append((i % k) * (2 * 180.0 / k))

    sectors = []

    for i in range(80):
        x = 1
        y = 1
        sector = []
        for x in range(cols):
            #print x
            for y in range(rows):
                x0 = x - core_x
                y0 = y - core_y
                r = math.sqrt(pow(x0, 2) + pow(y0, 2))
                #print r
                if x0 == 0.0:
                    if y0 > 0:
                        point_angle = 270.0
                    else:
                        point_angle = 90.0

                if y0 == 0.0:
                    if x0 > 0:
                        point_angle = 0.0
                    else:
                        point_angle = 180.0
                # in 1 district
                if(y0 < 0.0)&(x0 > 0.0):
                    point_angle = abs(math.degrees(math.atan(y0 / x0)))
                # in 2 district
                if(y0 < 0.0)&(x0 < 0.0):
                    point_angle = abs(math.degrees(math.atan(x0 / y0))) + 90.0
                # in 3 district
                if(y0 > 0.0)&(x0 < 0.0):
                    point_angle = abs(math.degrees(math.atan(y0 / x0))) + 180.0
                # in 4 district
                if (y0 > 0.0)&(x0 > 0.0):
                    point_angle = abs(math.degrees(math.atan(x0 / y0))) + 270.0
                #point_angle = math.degrees(math.atan((y - core_y) / (x - core_x)))
                #print point_angle, r
                if (point_angle <= 337.5)&(b * (T[i] + 1) <= r)&(b * (T[i] + 2) > r)&(angle[i] <= point_angle)&(angle[i+1] > point_angle):
                    point = Point(y, x, img[y][x])
                    sector.append(point)
                if (point_angle > 337.5)&(b * (T[i] + 1) <= r)&(b * (T[i] + 2) > r)&(angle[i] <= point_angle)&(360.0 > point_angle):
                    point = Point(y, x, img[y][x])
                    sector.append(point)
        #print len(sector)
        sectors.append(sector)

    return sectors

def NormalizeIMG(img, sectors):
    M0 = 100
    V0 = 100
    Mean = []
    Variance = []
    for i in range(len(sectors)):
        Mean.append(cal_mean(sectors[i]))
        Variance.append(cal_variance(sectors[i], Mean[i]))
        sector = sectors[i]
        for j in range(len(sector)):
            point = sector[j]
            if Variance[i] == 0:
                Variance[i] = 1
            temp = math.sqrt(V0 * math.pow((point.Gray - Mean[i]), 2) / Variance[i])
            temp = int(temp)
            if point.Gray > Mean[i]:
                img[point.X, point.Y] = M0 + temp
            else:
                img[point.X, point.Y] = M0 - temp
    return img

def DivideSector(img):
    result = []
    # rows,cols = img.shape[:2]
    # offset_y,offset_x = (150-rows)//2,(150-cols)//2
    # for i in sectors:
    #     sector = []
    #     for j in i:
    #         point = Point(j[0]-offset_y,j[1]-offset_x,img[j[0]-offset_y][j[1]-offset_x])
    #         sector.append(point)
    #     result.append(sector)

    for i in sectors:
        sector = []
        for j in i:
            point = Point(j[0],j[1],img[j[0],j[1]])
            sector.append(point)
        result.append(sector)


    #result = DivideSector_ONCE(img)
    return result


if __name__ =="__main__":
    result = DivideSector_PRE()
    print(result)