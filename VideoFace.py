# coding: UTF-8

#引入dlib和opencv这两个库

import dlib
import cv2
import numpy as np


def rect_to_bb(rect):
    x = rect.left()
    y = rect.top()
    w = rect.right() - x
    h = rect.bottom() - y
    return (x, y, w, h)


def shape_to_np(shape, dtype="int"):
    coords = np.zeros((68, 2), dtype=dtype)
    for i in range(0, 68):
        coords[i] = (shape.part(i).x, shape.part(i).y)
    return coords


def resize(image, width=1200):
    r = width * 1.0 / image.shape[1]
    dim = (width, int(image.shape[0] * r))
    resized = cv2.resize(image, dim, interpolation=cv2.INTER_AREA)
    return resized





#t第一个函数，功能是从图像中检测人脸部分
def detectFact(img):
    #利用自带的检测器

    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")
    #对目标图像进行采样，貌似是第二个参数越大识别精度越高。

    dects = detector(img,1)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    #对检测出的模型进行计算

    for i,rect in enumerate(dects):
    #读取人脸区域坐标

        shape = predictor(gray, rect)
        shape = shape_to_np(shape)
        (x, y, w, h) = rect_to_bb(rect)
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.putText(img, "Face #{}".format(i + 1), (x - 10, y - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        for (x, y) in shape:
            cv2.circle(img, (x, y), 2, (0, 0, 255), -1)

        # cv2.imshow("Output", img)
        # key = cv2.waitKey(10)





        # left,right,top,bottom = rect.left(),rect.right(),rect.top(),rect.bottom()
        # print ('脸部坐标：(%d,%d),(%d,%d)'%(left,top,right,bottom))
        # #利用opencv中的函数进行画出人脸方框。（另：dlib库中有自带的方法可以画出人脸）
        # cv2.rectangle(img,(left,top),(right,bottom),(0,0,255),2)
        # cv2.putText(img,str(i),((left+right)/2,bottom+20),cv2.FONT_HERSHEY_PLAIN,1,(0,255,0),2)
        #返回检测出人脸的图像
    return img
    #从摄像头中获取目标图像   

def getVideoFrame():
    capture = cv2.VideoCapture("3333.mp4")
    cnt = 0
    while True:
        ret,frame = capture.read()
        #这里我设定的是每隔20帧进行一次人脸检测   ，正常情况下的视频中1秒钟是24～30帧。  

        if cnt%20==0:
            frame = detectFact(frame)
            cv2.imshow('Video',frame)
            if cv2.waitKey(10)&0xff == ord('q'):
                break
        cnt += 1
    capture.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    getVideoFrame()