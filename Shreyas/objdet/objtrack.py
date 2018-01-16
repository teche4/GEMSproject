import cv2
import numpy as np
from time import sleep

def nothing(x):
    pass
'''
cv2.namedWindow('image')
cv2.createTrackbar('HMAX','image',0,255,nothing)
cv2.createTrackbar('HMIN','image',0,255,nothing)
cv2.createTrackbar('SMAX','image',0,255,nothing)
cv2.createTrackbar('SMIN','image',0,255,nothing)
cv2.createTrackbar('VMAX','image',0,255,nothing)
cv2.createTrackbar('VMIN','image',0,255,nothing)
'''
cap = cv2.VideoCapture(0)

while True:
    ret,frame = cap.read()
    '''
    HMAX = cv2.getTrackbarPos('HMAX','image')
    HMIN = cv2.getTrackbarPos('HMIN','image')
    SMAX = cv2.getTrackbarPos('SMAX','image')
    SMIN = cv2.getTrackbarPos('SMIN','image')
    VMAX = cv2.getTrackbarPos('VMAX','image')
    VMIN = cv2.getTrackbarPos('VMIN','image')
    
    MIN = np.array([HMIN,SMIN,VMIN])
    MAX = np.array([HMAX,SMAX,VMAX])
    '''
    MIN = np.array([14,134,97])
    MAX = np.array([124,255,175])
    if ret is True:
        hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv,MIN,MAX)
        #res = cv2.bitwise_and(frame,frame, mask=mask)
        kernel1 = np.ones((3,3),np.uint8)
        #kernel2 = np.ones((8,8),np.uint8)
        erosion = cv2.erode(mask,kernel1,iterations=1)
        #dilation = cv2.dilate(mask,kernel2,iterations=1)
        cv2.imshow('frame',frame)
        #cv2.imshow('HSV',hsv)
        cv2.imshow('mask',mask)
        #cv2.imshow('res',res)
        cv2.imshow('eroded',erosion)
        #cv2.imshow('dialated',dilation)
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break


cap.release()
cv2.destroyAllWindows()
