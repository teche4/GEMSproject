import cv2
import numpy as np
from math import ceil

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
rec = cv2.createLBPHFaceRecognizer() 
rec.load('trainer.yml')
cap = cv2.VideoCapture(0)


font = cv2.cv.InitFont(cv2.cv.CV_FONT_HERSHEY_COMPLEX, 1, 1, 0, 2, 1)

while True:
    ind = 0
    txt = "Unknown"
    ret, img = cap.read()
    if ret is True:
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        for (x,y,w,h) in faces:
            cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)
            ind,conf = rec.predict(gray[y:y+h,x:x+w])
            
            
            if(ceil(conf)<=80):
                ##if(id==1):
                  ##  txt = "Shreyas"
                if(ind==2):
                    txt = 'VARUN'
                if(ind==3):
                    txt="nav"
                
            
            else:
                txt = "Unknown"

            cv2.cv.PutText(cv2.cv.fromarray(img),txt,(x+30,y+h+10),font,(0,0,255))
            print "Confidence of Prediction=",ceil(conf),"  ID= ",ind

        cv2.imshow('MyDetection',img)
        k = cv2.waitKey(30) & 0xff
        if k == 27:
            break
    #else:
        #print "Not able to connect Camera"
        #break

cap.release()
cv2.destroyAllWindows()
